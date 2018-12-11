from django.contrib import admin
from dnaorder.models import SubmissionType, Submission, SubmissionStatus
# from dnaorder.forms import ValidatorForm


# class ValidatorAdmin(admin.ModelAdmin):
#     form = ValidatorForm

admin.site.register(SubmissionType)
admin.site.register(Submission)
admin.site.register(SubmissionStatus)
# admin.site.register(Validator,ValidatorAdmin)