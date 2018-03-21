from django import forms
from dnaorder.models import Submission, Validator, SubmissionStatus
from __builtin__ import file
import tablib
from dnaorder.spreadsheets import SRASampleSheet, CoreSampleSheet
import material
import re
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget

class SubmissionStatusForm(forms.ModelForm):
    send_email = forms.BooleanField(required=True,initial=True)
    class Meta:
        model = Submission
        fields = ['status','send_email']
    layout = material.base.Layout(
        material.base.Row('status', 'send_email')
    )
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        exclude = ['submitted','sample_data','sra_data','status','internal_id']
        help_texts = {
                      'sra_form':'If you are planning to submit sequences to SRA, please <a target="_blank" href="https://submit.ncbi.nlm.nih.gov/biosample/template/">download the appropriate template</a> and upload them here.',
                      'sample_form':'<span id="sample_form_help">Please select a submission type in order to generate a template.</span>',
                      'notes':'Please enter any additional notes necessary here'
                      }
        labels = {'name':'Submitter Name','email':'Submitter Email','phone':'Submitter Phone','pi_name':'PI Name','pi_email':'PI Email','biocore':'Do you want the Bioinformatics Core to analyze the data?'}
    layout = material.base.Layout(
        'name',
        material.base.Row('email', 'phone'),
        material.base.Row('pi_name', 'pi_email'),
        'institute',
        'notes',
        'type',
        'sample_form',
        'sra_form',
        'biocore',
    )
    def save(self, commit=True):
        submission = super(SubmissionForm, self).save(commit=commit)
        if hasattr(self, '_sample_data'):
            submission.sample_data = self._sample_data
        if hasattr(self, '_sra_data'):
            submission.sra_data = self._sra_data
        if not submission.status:
            submission.status = SubmissionStatus.objects.filter(default=True).order_by('order').first()
        if commit:
            submission.save()
        return submission
    def clean_sra_form(self):
        file = self.files.get('sra_form')
        if file:
    #         print file
    #         data = tablib.Dataset().load(file.read())
            if hasattr(self, 'samplesheet'):
                self.sra_samplesheet = SRASampleSheet(file,main_samplesheet=self.samplesheet)
#             missing = samplesheet.missing_values()
#             if len(missing) > 0:
#                 raise forms.ValidationError([
#                     forms.ValidationError('Required field "%s" missing values for: %s'%(col,', '.join(ids))) for col, ids in missing.items()
#                 ])
            self._sra_data = self.sra_samplesheet.data
    #         print self.sra_samplesheet.sample_ids()
            self._sra_samples = self.sra_samplesheet.sample_ids()
            _errors = self.sra_samplesheet.validate()
            print self.sra_samplesheet.error_lookup()
            if len(_errors):
                errors = []
                for e in _errors:
                    errors.append(forms.ValidationError(mark_safe("<b>Column:</b> {column} <b>IDs:</b> {ids} <b>Message:</b> {message}".format(message=e['message'],column=e['column'],ids=', '.join(e['ids'])))))
                if len(errors) > 0:
                    errors.append(forms.ValidationError(mark_safe('<a class="visualize_errors" href="#"><i class="material-icons tiny">grid_on</i> Visualize Errors</a>')))
                raise forms.ValidationError(errors)
        return file
#         raise forms.ValidationError("Is no good.")
    def clean_sample_form(self):
        file = self.files.get('sample_form')
        if not file and self.instance:
            file = self.instance.sample_form.file
        type = self.cleaned_data.get('type')
        errors = []
        if not type:
            raise forms.ValidationError("You must choose a submission type.")
        self.samplesheet = CoreSampleSheet(file,type)
        self._sample_data = self.samplesheet.data
        if self.samplesheet.headers_modified:
            errors.append(forms.ValidationError("Sample submission headers do not match the template headers.  Please ensure that you are using the selected submission template and that you have not modified the headers."))
        self._sample_ids = self.samplesheet.sample_ids()
        
        _errors = self.samplesheet.validate()
        print self.samplesheet.error_lookup()
        if len(_errors):
            for e in _errors:
                errors.append(forms.ValidationError(mark_safe("<b>Column:</b> {column} <b>IDs:</b> {ids} <b>Message:</b> {message}".format(message=e['message'],column=e['column'],ids=', '.join(e['ids'])))))
            if len(errors) > 0:
                errors.append(forms.ValidationError(mark_safe('<a class="visualize_errors" href="#"><i class="material-icons tiny">grid_on</i> Visualize Errors</a>')))
            raise forms.ValidationError(errors)
        return file
#     def clean(self):
#         cleaned_data = super(SubmissionForm, self).clean()
#         if hasattr(self, '_sample_ids') and hasattr(self, '_sra_samples'): 
#             sample_diff = set(self._sra_samples)-set(self._sample_ids)
#             if len(sample_diff) > 0:
#                 if len(self._errors.get('sra_form',[])) > 0:
#                     self._errors['sra_form'].insert(0,forms.ValidationError('The following sample ids in the SRA form do not match any samples from the submission form: '+', '.join(list(sample_diff))))
#                 else:
#                     raise forms.ValidationError({'sra_form':'The following sample ids in the SRA form do not match any samples from the submission form: '+', '.join(list(sample_diff))})


class ValidatorForm(forms.ModelForm):
    class Meta:
        model = Validator
        exclude = []
        help_texts = {
                      'regex':'Enter a valid regular expression to validate against. Example for matching values such as "20.3 ul": ^\d+(\.{1}\d+)? ul$',
                      'choices':'Enter comma delimited choices.',
                      'choices':'Enter a numeric range.  You may enter a min, max, or both.'
                      }
    def clean_regex(self):
        regex = self.cleaned_data.get('regex')
        if regex:
            try:
                re.compile(regex)
            except re.error:
                raise forms.ValidationError('Please enter a valid regular expression.')
        return regex
    def clean(self):
        cleaned_data = super(ValidatorForm, self).clean()
        if not cleaned_data.get('regex') and not cleaned_data.get('choices') and not cleaned_data.get('range'):
            raise forms.ValidationError('Please enter at least 1 validation method (regex, choices, range).')
        