from django.core.management.base import BaseCommand

from dnaorder.file_fields import PENDING_HOURS, pending_cutoff
from dnaorder.models import SubmissionFile


class Command(BaseCommand):
    help = 'Delete form file field uploads never attached to a submission within {} hours. Run it daily, e.g. from cron.'.format(PENDING_HOURS)

    def handle(self, *args, **options):
        stale = SubmissionFile.objects.filter(submission__isnull=True, uploaded_at__lt=pending_cutoff())
        count = 0
        for upload in stale:
            upload.file.delete(save=False)
            upload.delete()
            count += 1
        self.stdout.write('Deleted {} unattached upload(s).'.format(count))
