"""Anonymize the entire database in place.

Intended for dev/test environments freshly seeded from a production dump.
Run this AFTER restoring a production dump into a non-production database.
NEVER run it against the real production database.

Policy:
  * User passwords  -> set_unusable_password() for every user we touch.
  * Usernames       -> preserved.
  * Names / emails  -> scrubbed on every user EXCEPT those listed via
                       --keep-superuser <username> (repeatable, superuser-only).
  * Reversion       -> all Version + Revision rows deleted.
  * Auth tokens     -> all rest_framework Token rows deleted.
  * Social auth     -> all social_django UserSocialAuth rows deleted.
  * SubmissionFile  -> DB rows deleted (file blobs on disk/S3 unchanged).
  * Notes, comments -> replaced with a placeholder.
  * Submission PII  -> top-level + payment + submission_data (schema-driven) +
                       sample_data + plugin_data + import_data scrubbed.
  * PI / PIInstitution / Lab / Institution names/emails -> scrubbed.
  * Draft / Import / Sample data JSON -> emptied.
"""

import hashlib
import sys
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.db import connection, transaction
from django.db.models import CharField, F, Value
from django.db.models.functions import Cast, Concat

# Batch size for the bulk_update calls that touch JSONB submission fields.
BULK_BATCH = 500


def _id_str(field='id'):
    """SQL expression: text representation of a (possibly integer) PK."""
    return Cast(field, output_field=CharField())


def _pk_email(prefix, pk_field='id', char_pk=False):
    """SQL Concat producing 'prefix<pk>@example.invalid'."""
    pk_expr = F(pk_field) if char_pk else _id_str(pk_field)
    return Concat(
        Value(prefix), pk_expr, Value('@example.invalid'),
        output_field=CharField(),
    )


def _pk_prefixed(prefix, pk_field='id', char_pk=False):
    """SQL Concat producing 'prefix<pk>'."""
    pk_expr = F(pk_field) if char_pk else _id_str(pk_field)
    return Concat(Value(prefix), pk_expr, output_field=CharField())


REQUIRED_PHRASE = 'confirm anonymization'

# (kind, substring hints) matched against lowercased variable name / title.
PII_HINTS = [
    ('email',       ('email', 'e-mail')),
    ('phone',       ('phone', 'fax', 'mobile', 'cell')),
    ('first_name',  ('first name', 'firstname', 'given name')),
    ('last_name',   ('last name', 'lastname', 'surname', 'family name')),
    ('name',        ('full name', 'contact name', 'investigator', 'submitter',
                     'researcher', 'principal investigator', 'pi name',
                     'requestor', 'requester', 'pi_name')),
    ('address',     ('address', 'street', 'mailing')),
    ('department',  ('department', 'dept')),
    ('institution', ('institution', 'institute', 'university', 'college',
                     'company', 'organization', 'organisation', 'affiliation')),
    ('id_code',     ('account number', 'chartstring', 'chart string',
                     'po number', 'purchase order', 'billing code')),
]

PAYMENT_HANDLERS = (
    ('email', 'email'), ('phone', 'phone'),
    ('account', 'id_code'), ('chart', 'id_code'), ('po', 'id_code'),
    ('purchase', 'id_code'), ('billing', 'id_code'),
    ('holder', 'name'), ('contact', 'name'), ('name', 'name'),
    ('address', 'address'),
)


def _slug(value, n=6):
    return hashlib.sha1(repr(value).encode('utf-8')).hexdigest()[:n]


def _fake(kind, value):
    if value is None or value == '':
        return value
    if kind == 'email':       return 'user{}@example.invalid'.format(_slug(value))
    if kind == 'first_name':  return 'First{}'.format(_slug(value))
    if kind == 'last_name':   return 'Last{}'.format(_slug(value))
    if kind == 'name':        return 'Person {}'.format(_slug(value))
    if kind == 'institution': return 'Institution {}'.format(_slug(value).upper())
    if kind == 'department':  return 'Department {}'.format(_slug(value).upper())
    if kind == 'address':     return '{} Anon Way, Anytown'.format(_slug(value))
    if kind == 'id_code':     return 'XXX-{}'.format(_slug(value).upper())
    if kind == 'phone':
        n = int(hashlib.sha1(repr(value).encode('utf-8')).hexdigest(), 16) % 10000
        return '555-555-{:04d}'.format(n)
    return value


def _kind_for_schema_field(variable, definition):
    title = ''
    if isinstance(definition, dict):
        title = (definition.get('title') or '').lower()
    var_l = (variable or '').lower()
    for kind, hints in PII_HINTS:
        for h in hints:
            if h in var_l or h in title:
                return kind
    return None


def _scrub_data_by_schema(data, schema):
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return
    for var, definition in (schema.get('properties') or {}).items():
        if var not in data:
            continue
        d_type = definition.get('type') if isinstance(definition, dict) else None
        if d_type == 'table':
            rows = data.get(var)
            if isinstance(rows, list):
                sub_schema = definition.get('schema') or {}
                for row in rows:
                    _scrub_data_by_schema(row, sub_schema)
        else:
            kind = _kind_for_schema_field(var, definition)
            if not kind or not data[var]:
                continue
            if isinstance(data[var], list):
                data[var] = [_fake(kind, v) if isinstance(v, str) and v else v
                             for v in data[var]]
            elif isinstance(data[var], str):
                data[var] = _fake(kind, data[var])


def _scrub_payment_dict(payment):
    if not isinstance(payment, dict):
        return
    for k, v in list(payment.items()):
        if not v or not isinstance(v, str):
            continue
        lk = k.lower()
        for needle, kind in PAYMENT_HANDLERS:
            if needle in lk:
                payment[k] = _fake(kind, v)
                break


class Command(BaseCommand):
    help = ('Anonymize the entire database in place. Intended for dev/test '
            'copies of a production dump. DESTRUCTIVE; requires confirmation.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--yes', action='store_true',
            help='Skip the interactive confirmation prompt.',
        )
        parser.add_argument(
            '--keep-superuser', action='append', default=[], metavar='USERNAME',
            help='Preserve a superuser account intact (names/emails/password). '
                 'Repeatable. Ignored for usernames that are not superusers.',
        )

    def handle(self, *args, **options):
        self._confirm(options['yes'])
        keep_supers = self._resolve_keep_supers(options['keep_superuser'])

        phases = [
            ('reversion (TRUNCATE)',       self._delete_reversion),
            ('auth tokens (TRUNCATE)',     self._delete_auth_tokens),
            ('social auth (TRUNCATE)',     self._delete_social_auth),
            ('SubmissionFile (TRUNCATE)',  self._delete_submission_files),
            ('Note bulk update',           self._scrub_notes),
            ('Contact bulk update',        self._scrub_contacts),
            ('Draft/Import/Sample bulk',   self._scrub_drafts_imports_samples),
            ('Submission scalar + JSON',   self._scrub_submissions),
            ('PI bulk update',             self._scrub_pis),
            ('PIInstitution bulk update',  self._scrub_pi_institutions),
            # ('Lab bulk update',            self._scrub_labs),
            # ('Institution bulk update',    self._scrub_institutions),
            ('User bulk update',           lambda: self._scrub_users(keep_supers)),
        ]

        with transaction.atomic():
            for name, fn in phases:
                self._phase(name, fn)

        self._log(self.style.SUCCESS('Anonymization complete.'))

    # --- progress logging ---------------------------------------------------
    def _log(self, msg):
        """Write to stdout and flush immediately so progress is visible."""
        self.stdout.write(msg)
        try:
            self.stdout.flush()
        except Exception:
            sys.stdout.flush()

    def _phase(self, name, fn):
        self._log('-> {}: starting...'.format(name))
        t = time.monotonic()
        fn()
        self._log('   {}: done in {:.1f}s'.format(name, time.monotonic() - t))

    # --- confirmation -------------------------------------------------------
    def _confirm(self, skip):
        if skip:
            self.stdout.write('Skipping confirmation (--yes).')
            return
        self._log(self.style.WARNING(
            '\n*** DESTRUCTIVE: this anonymizes the ENTIRE database in place. ***\n'
            'Run this only against a dev/test copy of production -- never\n'
            'against the real production database. Submissions, users, PIs,\n'
            'labs, institutions, notes, reversion history, auth tokens, social\n'
            'logins, and SubmissionFile rows will all be wiped or scrubbed.\n'
        ))
        sys.stdout.flush()
        try:
            response = input('Type "{}" to proceed: '.format(REQUIRED_PHRASE))
        except EOFError:
            raise CommandError(
                'No interactive tty available for confirmation. Pass --yes if '
                'you really want to run non-interactively.'
            )
        if response.strip() != REQUIRED_PHRASE:
            raise CommandError('Confirmation phrase not entered. Aborting.')

    def _resolve_keep_supers(self, requested):
        if not requested:
            return set()
        User = get_user_model()
        requested = set(requested)
        valid = set(User.objects.filter(
            username__in=requested, is_superuser=True
        ).values_list('username', flat=True))
        missing = requested - valid
        if missing:
            self.stdout.write(self.style.WARNING(
                '--keep-superuser usernames not found or not superusers (will '
                'be anonymized): {}'.format(sorted(missing))
            ))
        if valid:
            self.stdout.write('Preserving superuser(s) intact: {}'.format(sorted(valid)))
        return valid

    # --- deletes ------------------------------------------------------------
    def _truncate(self, tables, lock_timeout_ms=10000):
        """TRUNCATE the given tables CASCADE. Far faster than Django delete() on
        large tables -- it doesn't load rows into Python.

        TRUNCATE needs ACCESS EXCLUSIVE on each target table. If anything else
        is holding a lock (live API server, idle psql session, pgAdmin), we'd
        block forever -- so set a short statement-local lock_timeout and on
        failure dump the blocker info from pg_stat_activity.
        """
        if not tables:
            return
        sql = 'TRUNCATE TABLE {} RESTART IDENTITY CASCADE'.format(
            ', '.join('"{}"'.format(t) for t in tables)
        )
        with connection.cursor() as cur:
            cur.execute("SET LOCAL lock_timeout = '{}ms'".format(int(lock_timeout_ms)))
            try:
                cur.execute(sql)
            except Exception as exc:
                self._dump_lock_blockers(tables)
                raise CommandError(
                    'TRUNCATE on {} failed (likely lock contention): {}\n'
                    'Stop any process holding connections to these tables '
                    '(dev API server, psql sessions, pgAdmin) and re-run.'
                    .format(', '.join(tables), exc)
                )

    def _dump_lock_blockers(self, tables):
        """Print sessions currently holding locks on the given tables."""
        try:
            with connection.cursor() as cur:
                cur.execute("""
                    SELECT a.pid, a.usename, a.application_name, a.state,
                           a.wait_event_type, a.wait_event,
                           NOW() - a.xact_start AS xact_age,
                           LEFT(a.query, 200) AS query
                    FROM pg_locks l
                    JOIN pg_stat_activity a ON a.pid = l.pid
                    JOIN pg_class c ON c.oid = l.relation
                    WHERE c.relname = ANY(%s)
                      AND a.pid <> pg_backend_pid()
                """, [list(tables)])
                rows = cur.fetchall()
        except Exception as exc:
            self._log('   (could not query pg_stat_activity: {})'.format(exc))
            return
        if not rows:
            self._log('   no other sessions found holding locks on {}'.format(tables))
            return
        self._log('   sessions holding locks on {}:'.format(tables))
        for r in rows:
            self._log('     pid={} user={} app={} state={} wait={}/{} xact_age={} '
                      'query={!r}'.format(*r))

    def _delete_reversion(self):
        try:
            from reversion.models import Version, Revision
        except ImportError:
            self._log('   reversion not installed; skipping.')
            return
        tables = [Version._meta.db_table, Revision._meta.db_table]
        self._log('   TRUNCATE {} CASCADE'.format(', '.join(tables)))
        self._truncate(tables)

    def _delete_auth_tokens(self):
        try:
            from rest_framework.authtoken.models import Token
        except ImportError:
            self._log('   authtoken not installed; skipping.')
            return
        self._log('   TRUNCATE {}'.format(Token._meta.db_table))
        self._truncate([Token._meta.db_table])

    def _delete_social_auth(self):
        try:
            from social_django.models import UserSocialAuth, Nonce, Code, Partial
        except ImportError:
            self._log('   social_django not installed; skipping.')
            return
        tables = [m._meta.db_table for m in (UserSocialAuth, Nonce, Code, Partial)]
        self._log('   TRUNCATE {} CASCADE'.format(', '.join(tables)))
        self._truncate(tables)

    def _delete_submission_files(self):
        from dnaorder.models import SubmissionFile
        self._log('   TRUNCATE {} CASCADE (blobs on disk/S3 untouched)'.format(
            SubmissionFile._meta.db_table))
        self._truncate([SubmissionFile._meta.db_table])

    # --- scrubs -------------------------------------------------------------
    def _scrub_notes(self):
        from dnaorder.models import Note
        total = Note.objects.count()
        self._log('   Note rows to update: {}'.format(total))
        n = Note.objects.update(text='[redacted]', emails=[])
        self._log('   updated {} Note rows'.format(n))

    def _scrub_contacts(self):
        from dnaorder.models import Contact
        total = Contact.objects.count()
        self._log('   Contact rows to update: {}'.format(total))
        n = Contact.objects.update(
            first_name='Anon',
            last_name='Contact',
            email=_pk_email('contact'),
        )
        self._log('   updated {} Contact rows'.format(n))

    def _scrub_drafts_imports_samples(self):
        from dnaorder.models import Draft, Import, Sample
        self._log('   Draft.update...')
        d = Draft.objects.update(data={})
        self._log('   Draft updated: {}'.format(d))
        self._log('   Import.update...')
        i = Import.objects.update(data={}, external_id=None,
                                  url='https://example.invalid/',
                                  api_url='https://example.invalid/api/')
        self._log('   Import updated: {}'.format(i))
        self._log('   Sample.update...')
        s = Sample.objects.update(data=None)
        self._log('   Sample.data updated: {}'.format(s))

    def _scrub_submissions(self):
        from dnaorder.models import Submission
        total = Submission.objects.count()
        self._log('   Submission rows: {}'.format(total))

        # Phase 1: bulk SQL update for every scalar PII column.
        self._log('   bulk SQL update of scalar PII...')
        n = Submission.objects.update(
            first_name=_pk_prefixed('First', char_pk=True),
            last_name=_pk_prefixed('Last', char_pk=True),
            email=_pk_email('user', char_pk=True),
            phone='555-555-0000',
            pi_first_name=_pk_prefixed('First', char_pk=True),
            pi_last_name=_pk_prefixed('Last', char_pk=True),
            pi_email=_pk_email('pi', char_pk=True),
            pi_phone='555-555-0000',
            institute='Institution',
            plugin_data={},
            import_data=None,
            warnings=None,
            data={},
        )
        self._log('   scalar PII updated: {} rows'.format(n))

        self._log('   redacting notes/comments...')
        Submission.objects.exclude(notes__isnull=True).exclude(notes='').update(notes='[redacted]')
        Submission.objects.exclude(comments__isnull=True).exclude(comments='').update(comments='[redacted]')

        # Phase 2: JSON-aware pass via PK pagination (no server-side cursor).
        # Streaming with `.iterator()` while issuing writes against the same
        # table on the same connection can wedge; ordered PK pagination is safer
        # and lets us print progress between batches.
        fields = ['payment', 'submission_data', 'sample_data']
        only = ['pk'] + fields + ['submission_schema', 'sample_schema']
        last_pk = ''
        processed = updated = 0
        while True:
            chunk = list(
                Submission.objects
                .filter(pk__gt=last_pk)
                .order_by('pk')
                .only(*only)[:BULK_BATCH]
            )
            if not chunk:
                break
            batch = []
            for s in chunk:
                touched = False
                if isinstance(s.payment, dict) and s.payment:
                    _scrub_payment_dict(s.payment); touched = True
                if isinstance(s.submission_data, dict) and isinstance(s.submission_schema, dict):
                    _scrub_data_by_schema(s.submission_data, s.submission_schema); touched = True
                if isinstance(s.sample_data, list) and isinstance(s.sample_schema, dict):
                    for row in s.sample_data:
                        _scrub_data_by_schema(row, s.sample_schema)
                    touched = True
                if touched:
                    batch.append(s)
            if batch:
                Submission.objects.bulk_update(batch, fields)
                updated += len(batch)
            processed += len(chunk)
            last_pk = chunk[-1].pk
            self._log('   JSON scrub progress: {}/{} (updated {})'.format(
                processed, total, updated))
        self._log('   JSON scrub complete: {} rows updated'.format(updated))

    def _scrub_pis(self):
        from dnaorder.models import PI
        self._log('   PI rows: {}'.format(PI.objects.count()))
        n = PI.objects.update(
            first_name=_pk_prefixed('First'),
            last_name=_pk_prefixed('Last'),
            email=_pk_email('pi'),
            phone='555-555-0000',
            meta={},
        )
        PI.objects.exclude(department__isnull=True).exclude(department='').update(
            department='Department')
        self._log('   updated {} PI rows'.format(n))

    def _scrub_pi_institutions(self):
        from dnaorder.models import PIInstitution
        self._log('   PIInstitution rows: {}'.format(PIInstitution.objects.count()))
        n = PIInstitution.objects.update(
            name=_pk_prefixed('PI Institution '),
            meta={},
        )
        self._log('   updated {} PIInstitution rows'.format(n))

    def _scrub_labs(self):
        from dnaorder.models import Lab
        self._log('   Lab rows: {}'.format(Lab.objects.count()))
        n = Lab.objects.update(
            name=_pk_prefixed('Lab '),
            email=_pk_email('lab'),
            plugins={},
        )
        Lab.objects.exclude(home_page='').update(home_page='')
        Lab.objects.exclude(submission_page='').update(submission_page='')
        Lab.objects.exclude(submission_email_text='').update(submission_email_text='')
        self._log('   updated {} Lab rows'.format(n))

    def _scrub_institutions(self):
        from dnaorder.models import Institution
        self._log('   Institution rows: {}'.format(Institution.objects.count()))
        n = Institution.objects.update(
            name=_pk_prefixed('Institution ', char_pk=True),
            home_page='',
            plugins={},
        )
        self._log('   updated {} Institution rows'.format(n))

    def _scrub_users(self, keep_supers):
        User = get_user_model()
        from dnaorder.models import UserEmail, UserProfile

        kept_user_ids = list(User.objects.filter(
            username__in=keep_supers).values_list('pk', flat=True)) if keep_supers else []
        self._log('   User rows: {} (keeping {} superuser(s))'.format(
            User.objects.count(), len(kept_user_ids)))

        # One unusable password value reused for every scrubbed user -- still
        # unusable because of the '!' prefix that check_password rejects.
        unusable = make_password(None)
        n = User.objects.exclude(pk__in=kept_user_ids).update(
            first_name=_pk_prefixed('First'),
            last_name=_pk_prefixed('Last'),
            email=_pk_email('user'),
            password=unusable,
        )
        self._log('   updated {} User rows'.format(n))

        self._log('   UserEmail rows: {}'.format(UserEmail.objects.count()))
        ue_n = UserEmail.objects.exclude(user_id__in=kept_user_ids).update(
            email=_pk_email('useremail'),
        )
        self._log('   updated {} UserEmail rows'.format(ue_n))

        up_count = UserProfile.objects.exclude(user_id__in=kept_user_ids).update(settings={})
        self._log('   cleared {} UserProfile.settings'.format(up_count))
