from django.contrib import admin
from dnaorder.models import SubmissionType, Submission, PrefixID,\
    Lab, Vocabulary, Term
# from dnaorder.forms import ValidatorForm


# class ValidatorAdmin(admin.ModelAdmin):
#     form = ValidatorForm

admin.site.register(Lab)
admin.site.register(SubmissionType)
admin.site.register(Submission)
# admin.site.register(SubmissionStatus)
admin.site.register(PrefixID)
admin.site.register(Vocabulary)
admin.site.register(Term)
# admin.site.register(Validator,ValidatorAdmin)