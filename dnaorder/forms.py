from django import forms
from dnaorder.models import Submission
from __builtin__ import file
import tablib
from dnaorder.spreadsheets import SRASampleSheet, CoreSampleSheet
import material

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submitted']
        help_texts = {
                      'sra_form':'If you are planning to submit sequences to SRA, please <a target="_blank" href="https://submit.ncbi.nlm.nih.gov/biosample/template/">download the appropriate templat</a>e and upload them here.',
                      'sample_form':'<span id="sample_form_help">Please select a submission type in order to generate a template.</span>'
                      }
    layout = material.base.Layout(
        'name',
        material.base.Row('email', 'phone'),
        material.base.Row('pi_name', 'pi_email'),
        'institute',
        'type',
        'sample_form',
        'sra_form',
    )
    def clean_sra_form(self):
        file = self.files.get('sra_form')
#         print file
#         data = tablib.Dataset().load(file.read())
        samplesheet = SRASampleSheet(file)
        print samplesheet.data
#         print samplesheet.sample_ids()
        self._sra_samples = samplesheet.sample_ids()
        print self._sra_samples 
        
        return file
#         raise forms.ValidationError("Is no good.")
    def clean_sample_form(self):
        file = self.files.get('sample_form')
        type = self.cleaned_data.get('type')
        if not type:
            raise forms.ValidationError("You must choose a submission type.")
        samplesheet = CoreSampleSheet(file,type)
        self._sample_ids = samplesheet.sample_ids()
        print samplesheet.data
        print self._sample_ids 
        return file
    def clean(self):
        cleaned_data = super(SubmissionForm, self).clean()
        if hasattr(self, '_sample_ids') and hasattr(self, '_sra_samples'): 
            sample_diff = set(self._sra_samples)-set(self._sample_ids)
            if len(sample_diff) > 0:
                raise forms.ValidationError('The following sample ids in the SRA form do not match any samples from the submission form: '+', '.join(list(sample_diff)))
