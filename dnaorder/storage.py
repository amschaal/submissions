import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class ProtectedStorage(FileSystemStorage):
    """Stores files under PROTECTED_MEDIA_ROOT, which nginx does not serve (unlike MEDIA_ROOT),
    so they can only be downloaded through a Django view that checks permissions."""
    @property
    def base_location(self):  # read lazily so override_settings works in tests
        return settings.PROTECTED_MEDIA_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)


protected_storage = ProtectedStorage()
