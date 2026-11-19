from collections import defaultdict

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from dnaorder.code_login.policy import is_privileged, normalize_email
from dnaorder.models import InstitutionPermission, LabPermission, UserEmail


class Command(BaseCommand):
    help = (
        'Report account data that gets in the way of signing in by email address: '
        'accounts sharing an address, addresses tied to more than one account, and '
        'staff flags without permissions. Read-only.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--fail-on-duplicates',
            action='store_true',
            help='Exit with an error when any address is tied to more than one account.',
        )

    def handle(self, *args, **options):
        # address -> {user id: how the address is tied to that account}
        owners = defaultdict(dict)
        users = {}
        for user in User.objects.exclude(email=''):
            users[user.pk] = user
            owners[normalize_email(user.email)][user.pk] = 'primary'
        for user_email in UserEmail.objects.select_related('user'):
            users[user_email.user_id] = user_email.user
            owners[normalize_email(user_email.email)].setdefault(user_email.user_id, 'secondary')

        shared = {email: tied for email, tied in owners.items() if email and len(tied) > 1}
        self.stdout.write('Addresses tied to more than one account: {}'.format(len(shared)))
        for email, tied in sorted(shared.items()):
            privileged = [pk for pk in tied if is_privileged(users[pk])]
            note = ''
            if privileged and len(privileged) < len(tied):
                note = '  <- shared between a staff and a non-staff account'
            self.stdout.write('  {}{}'.format(email, note))
            for pk, how in sorted(tied.items()):
                user = users[pk]
                self.stdout.write('    id={} username={} {}{}{}'.format(
                    pk, user.username, how,
                    '' if user.is_active else ' inactive',
                    ' staff' if pk in privileged else '',
                ))

        permitted = set(LabPermission.objects.values_list('user_id', flat=True))
        permitted.update(InstitutionPermission.objects.values_list('user_id', flat=True))
        stale = User.objects.filter(is_staff=True, is_superuser=False).exclude(pk__in=permitted)
        self.stdout.write('Staff accounts holding no lab or institution permission: {}'.format(stale.count()))
        for user in stale.order_by('username'):
            self.stdout.write('  id={} username={} email={}'.format(user.pk, user.username, user.email))
        if stale:
            self.stdout.write('  (these can only sign in with single sign-on until is_staff is cleared)')

        without_email = User.objects.filter(is_active=True, email='').count()
        self.stdout.write('Active accounts with no email address: {}'.format(without_email))

        if shared and options['fail_on_duplicates']:
            raise CommandError('{} address(es) are tied to more than one account.'.format(len(shared)))
