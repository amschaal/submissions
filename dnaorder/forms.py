from django import forms
from dnaorder.models import Submission
from __builtin__ import file
import tablib
from dnaorder.spreadsheets import SRASampleSheet

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submitted']
        help_texts = {
                      'sra_form':'If you are planning to submit sequences to SRA, please <a target="_blank" href="https://submit.ncbi.nlm.nih.gov/biosample/template/">download the appropriate templat</a>e and upload them here.',
                      'sample_form':'<span id="sample_form_help">Please select a submission type in order to generate a template.</span>'
                      }
    def clean_sra_form(self):
        file = self.files.get('sra_form')
#         print file
#         data = tablib.Dataset().load(file.read())
        samplesheet = SRASampleSheet(file)
        print 'validate'
        print samplesheet._header_index
        print samplesheet.data
        return file
#         raise forms.ValidationError("Is no good.")