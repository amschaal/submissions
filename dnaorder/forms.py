from django import forms
from dnaorder.models import Submission

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submitted']
        help_texts = {
                      'sra_form':'If you are planning to submit sequences to SRA, please <a target="_blank" href="https://submit.ncbi.nlm.nih.gov/biosample/template/">download the appropriate templat</a>e and upload them here.',
                      'sample_form':'<span id="sample_form_help">Please select a submission type in order to generate a template.</span>'
                      }