from django.contrib import admin
from dnaorder.models import SubmissionType, Submission, ProjectID,\
    Lab, Vocabulary, Term, Institution
from reversion.admin import VersionAdmin
# from dnaorder.forms import ValidatorForm


# class ValidatorAdmin(admin.ModelAdmin):
#     form = ValidatorForm

admin.site.register(Lab)
# admin.site.register(SubmissionType)
# admin.site.register(Submission)
admin.site.register(ProjectID)
admin.site.register(Vocabulary)
admin.site.register(Term)
admin.site.register(Institution)
# admin.site.register(Validator,ValidatorAdmin)

@admin.register(Submission)
class SubmissionAdmin(VersionAdmin):
    pass
@admin.register(SubmissionType)
class SubmissionTypeAdmin(VersionAdmin):
    pass