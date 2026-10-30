from django.contrib import admin

from webhooks.models import Webhook


@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):  # the secret is non-editable, so it never appears here
    list_display = ('lab', 'submission_type', 'url', 'enabled', 'last_status', 'last_sent')
