from django import forms
from dnaorder.models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submitted']