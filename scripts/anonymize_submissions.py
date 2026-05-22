"""Anonymize SubmissionSerializer / ListSubmissionSerializer JSON payloads.

Reads JSON from a file or stdin, writes anonymized JSON to a file or stdout.

Recognizes three shapes:
  1. A single submission object (detail view).
  2. A list of submission objects (raw list).
  3. A DRF paginated response with a `results` list.

Anonymization is stable within a single run: the same input value (email, name,
institution, etc.) maps to the same replacement everywhere in the document, so
relationships in the data are preserved.

Schema-aware fields inside `submission_data` are scrubbed using
`submission_schema` -- variable names and field titles are matched against PII
hint substrings (email, phone, first/last name, address, department,
institution, PI/investigator/submitter/contact name, etc.). Table-type fields
are descended into and each row scrubbed the same way. Free-text fields like
`notes` and `comments` get a regex pass to mask any embedded email addresses.

Usage:
    python anonymize_submissions.py -i submission.json -o anon.json
    cat list.json | python anonymize_submissions.py > anon.json
"""
import argparse
import hashlib
import json
import re
import sys
from copy import deepcopy

# Heuristic hints (kind, list of substrings) matched against lowercased
# variable name or schema title. First match wins.
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

EMAIL_RE = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')

_caches = {}


def _cache(kind):
    return _caches.setdefault(kind, {})


def _slug(value, n=6):
    return hashlib.sha1(repr(value).encode('utf-8')).hexdigest()[:n]


def _fake(kind, value, fmt):
    if value is None or value == '':
        return value
    cache = _cache(kind)
    if value in cache:
        return cache[value]
    cache[value] = fmt.format(slug=_slug(value), SLUG=_slug(value).upper())
    return cache[value]


def fake_submission_id(v):
    if v is None or v == '':
        return v
    cache = _cache('submission_id')
    if v in cache:
        return cache[v]
    # Matches dnaorder.models.generate_id: last 12 chars of a uuid4 (hex).
    import uuid
    cache[v] = uuid.uuid4().hex[-12:]
    return cache[v]


def fake_first_name(v):  return _fake('first_name', v, 'First{slug}')
def fake_last_name(v):   return _fake('last_name', v, 'Last{slug}')
def fake_full_name(v):   return _fake('name', v, 'Person {slug}')
def fake_email(v):       return _fake('email', v, 'user{slug}@example.invalid')
def fake_institution(v): return _fake('institution', v, 'Institution {SLUG}')
def fake_department(v):  return _fake('department', v, 'Department {SLUG}')
def fake_address(v):     return _fake('address', v, '{slug} Anon Way, Anytown')
def fake_username(v):    return _fake('username', v, 'user_{slug}')
def fake_lab(v):         return _fake('lab', v, 'Lab {SLUG}')
def fake_id_code(v):     return _fake('id_code', v, 'XXX-{SLUG}')


def fake_phone(v):
    if v is None or v == '':
        return v
    cache = _cache('phone')
    if v in cache:
        return cache[v]
    digits = int(hashlib.sha1(repr(v).encode('utf-8')).hexdigest(), 16) % 10000
    cache[v] = '555-555-{:04d}'.format(digits)
    return cache[v]


KIND_TO_FAKE = {
    'first_name':  fake_first_name,
    'last_name':   fake_last_name,
    'name':        fake_full_name,
    'email':       fake_email,
    'phone':       fake_phone,
    'institution': fake_institution,
    'department':  fake_department,
    'address':     fake_address,
    'username':    fake_username,
    'lab':         fake_lab,
    'id_code':     fake_id_code,
}


def anon(value, kind):
    if value is None:
        return None
    fake = KIND_TO_FAKE.get(kind)
    if not fake:
        return value
    if isinstance(value, list):
        return [fake(v) if isinstance(v, str) and v else v for v in value]
    if not isinstance(value, str):
        return value
    return fake(value)


def kind_for_schema_field(variable, definition):
    title = ''
    if isinstance(definition, dict):
        title = (definition.get('title') or '').lower()
    var_l = (variable or '').lower()
    for kind, hints in PII_HINTS:
        for h in hints:
            if h in var_l or h in title:
                return kind
    return None


def scrub_free_text(value):
    if not isinstance(value, str):
        return value
    return EMAIL_RE.sub(lambda m: fake_email(m.group(0)), value)


def anonymize_by_schema(data, schema):
    """Walk a data dict using its JSON schema and scrub PII-shaped fields."""
    if not isinstance(data, dict) or not isinstance(schema, dict):
        return data
    props = schema.get('properties') or {}
    for var, definition in props.items():
        if var not in data:
            continue
        d_type = definition.get('type') if isinstance(definition, dict) else None
        if d_type == 'table':
            sub_schema = definition.get('schema') or {}
            rows = data.get(var)
            if isinstance(rows, list):
                for row in rows:
                    anonymize_by_schema(row, sub_schema)
        else:
            kind = kind_for_schema_field(var, definition)
            if kind:
                data[var] = anon(data[var], kind)
    return data


def anonymize_user_block(user):
    if not isinstance(user, dict):
        return user
    if 'username' in user:
        user['username'] = anon(user.get('username'), 'username')
    if 'first_name' in user:
        user['first_name'] = anon(user.get('first_name'), 'first_name')
    if 'last_name' in user:
        user['last_name'] = anon(user.get('last_name'), 'last_name')
    if 'email' in user:
        user['email'] = anon(user.get('email'), 'email')
    if isinstance(user.get('emails'), list):
        user['emails'] = [anon(e, 'email') for e in user['emails']]
    if isinstance(user.get('labs'), list):
        for lab in user['labs']:
            anonymize_lab_block(lab)
    # Profile may include phone/department/etc.
    if isinstance(user.get('profile'), dict):
        anonymize_profile_block(user['profile'])
    return user


def anonymize_profile_block(profile):
    for k, v in list(profile.items()):
        lk = k.lower()
        if 'email' in lk:
            profile[k] = anon(v, 'email')
        elif 'phone' in lk:
            profile[k] = anon(v, 'phone')
        elif 'address' in lk:
            profile[k] = anon(v, 'address')
        elif 'department' in lk or lk == 'dept':
            profile[k] = anon(v, 'department')
        elif 'institut' in lk or 'affiliation' in lk:
            profile[k] = anon(v, 'institution')


def anonymize_lab_block(lab):
    if not isinstance(lab, dict):
        return lab
    if 'name' in lab:
        lab['name'] = anon(lab['name'], 'lab')
    if lab.get('lab_id'):
        lab['lab_id'] = anon(lab['lab_id'], 'lab')
    # plugin config may contain URLs / API keys / institution-identifying names
    lab.pop('plugins', None)
    return lab


def anonymize_pi_block(pi):
    if not isinstance(pi, dict):
        return pi
    if 'first_name' in pi:
        pi['first_name'] = anon(pi['first_name'], 'first_name')
    if 'last_name' in pi:
        pi['last_name'] = anon(pi['last_name'], 'last_name')
    if 'email' in pi:
        pi['email'] = anon(pi['email'], 'email')
    if 'phone' in pi:
        pi['phone'] = anon(pi['phone'], 'phone')
    if pi.get('department'):
        pi['department'] = anon(pi['department'], 'department')
    if 'institution' in pi and pi['institution'] is not None:
        if isinstance(pi['institution'], dict):
            if 'name' in pi['institution']:
                pi['institution']['name'] = anon(pi['institution']['name'], 'institution')
        elif isinstance(pi['institution'], str):
            pi['institution'] = anon(pi['institution'], 'institution')
    pi.pop('meta', None)
    return pi


PAYMENT_HANDLERS = (
    ('email',       'email'),
    ('phone',       'phone'),
    ('account',     'id_code'),
    ('chart',       'id_code'),
    ('po',          'id_code'),
    ('purchase',    'id_code'),
    ('billing',     'id_code'),
    ('holder',      'name'),
    ('contact',     'name'),
    ('name',        'name'),
    ('address',     'address'),
)


def anonymize_payment(payment):
    if not isinstance(payment, dict):
        return
    for k, v in list(payment.items()):
        lk = k.lower()
        for needle, kind in PAYMENT_HANDLERS:
            if needle in lk:
                payment[k] = anon(v, kind) if v else v
                break


def anonymize_submission(sub):
    if not isinstance(sub, dict):
        return sub

    # Randomize the submission id (12-char hex, matching generate_id()).
    original_id = sub.get('id')
    if isinstance(original_id, str) and original_id:
        sub['id'] = fake_submission_id(original_id)

    # Top-level scalar PII on the Submission model.
    for f, kind in (
        ('first_name', 'first_name'), ('last_name', 'last_name'),
        ('email', 'email'), ('phone', 'phone'),
        ('pi_first_name', 'first_name'), ('pi_last_name', 'last_name'),
        ('pi_email', 'email'), ('pi_phone', 'phone'),
        ('institute', 'institution'),
    ):
        if f in sub:
            sub[f] = anon(sub.get(f), kind)

    # `url` leaks the institution's domain; also swap the embedded id.
    if isinstance(sub.get('url'), str):
        url = re.sub(r'https?://[^/]+', 'https://example.invalid', sub['url'])
        if isinstance(original_id, str) and original_id:
            url = url.replace(original_id, sub['id'])
        sub['url'] = url

    # Free-text fields -- regex-strip any embedded emails.
    for ft in ('notes', 'comments', 'submission_email_text'):
        if sub.get(ft):
            sub[ft] = scrub_free_text(sub[ft])

    # Computed name fields from the serializer.
    if sub.get('received_by_name'):
        sub['received_by_name'] = anon(sub['received_by_name'], 'name')
    if isinstance(sub.get('participant_names'), list):
        sub['participant_names'] = [anon(n, 'name') for n in sub['participant_names']]

    # Nested blocks.
    if 'pi' in sub:
        anonymize_pi_block(sub['pi'])
    if 'lab' in sub:
        anonymize_lab_block(sub['lab'])
    if isinstance(sub.get('users'), list):
        for u in sub['users']:
            anonymize_user_block(u)
    if isinstance(sub.get('participants'), list):
        for p in sub['participants']:
            if isinstance(p, dict) and 'user' in p:
                anonymize_user_block(p['user'])
            else:
                anonymize_user_block(p)
    if isinstance(sub.get('contacts'), list):
        for c in sub['contacts']:
            if not isinstance(c, dict):
                continue
            if 'first_name' in c:
                c['first_name'] = anon(c['first_name'], 'first_name')
            if 'last_name' in c:
                c['last_name'] = anon(c['last_name'], 'last_name')
            if 'email' in c:
                c['email'] = anon(c['email'], 'email')

    # Schema-driven submission_data.
    schema = sub.get('submission_schema') or {}
    if isinstance(sub.get('submission_data'), dict):
        anonymize_by_schema(sub['submission_data'], schema)

    # Detail view may include sample_data + sample_schema (rows of one schema).
    sample_schema = sub.get('sample_schema') or {}
    if isinstance(sub.get('sample_data'), list) and sample_schema:
        for row in sub['sample_data']:
            anonymize_by_schema(row, sample_schema)

    # Payment can contain cardholder names, account #s, billing emails.
    if isinstance(sub.get('payment'), dict):
        anonymize_payment(sub['payment'])

    # Plugin and import payloads are arbitrary -- safer to drop.
    if 'plugin_data' in sub:
        sub['plugin_data'] = {}
    if 'import_data' in sub:
        sub['import_data'] = None

    return sub


def anonymize_payload(payload, limit=None):
    if isinstance(payload, list):
        if limit is not None:
            payload = payload[:limit]
        return [anonymize_submission(s) for s in payload]
    if isinstance(payload, dict):
        if isinstance(payload.get('results'), list):
            if limit is not None:
                payload['results'] = payload['results'][:limit]
                if 'count' in payload:
                    payload['count'] = len(payload['results'])
            # DRF pagination URLs embed the institution's host.
            for k in ('next', 'previous'):
                if k in payload:
                    payload[k] = None
            payload['results'] = [anonymize_submission(s) for s in payload['results']]
            return payload
        return anonymize_submission(payload)
    return payload


def main():
    ap = argparse.ArgumentParser(
        description='Anonymize CoreOmics submission JSON (detail or list).')
    ap.add_argument('-i', '--input', help='Input JSON file (default: stdin)')
    ap.add_argument('-o', '--output', help='Output JSON file (default: stdout)')
    ap.add_argument('-n', '--limit', type=int, default=None,
                    help='Truncate list/paginated payloads to the first N submissions. '
                         'Ignored for single-submission (detail) input.')
    ap.add_argument('--indent', type=int, default=2)
    args = ap.parse_args()

    if args.input:
        with open(args.input) as f:
            raw = f.read()
    else:
        raw = sys.stdin.read()

    payload = json.loads(raw)
    result = anonymize_payload(deepcopy(payload), limit=args.limit)
    out = json.dumps(result, indent=args.indent, default=str)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(out)
    else:
        sys.stdout.write(out + '\n')


if __name__ == '__main__':
    main()
