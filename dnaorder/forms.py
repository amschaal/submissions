from django import forms
from dnaorder.models import Submission, Validator, SubmissionStatus,\
    SubmissionType
from __builtin__ import file
import tablib
from dnaorder.spreadsheets import SRASampleSheet, CoreSampleSheet
import material
import re
from django.utils.safestring import mark_safe
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import ClearableFileInput

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
        exclude = ['submitted','sample_data','sra_data','status','internal_id','participants']
        help_texts = {
                      'sra_form':'If you are planning to submit sequences to <b class="tooltipped" data-position="bottom" data-delay="50" data-tooltip="A very informative description of SRA submissions will pop up in my place...">NCBI SRA <i class="material-icons tiny">help_outline</i></b>, please <a target="_blank" href="https://submit.ncbi.nlm.nih.gov/biosample/template/">download the appropriate template</a> and upload them here.',
                      'sample_form':'<span id="sample_form_help">Please select a submission type in order to generate a template.</span>',
                      'notes':'Please enter any additional notes necessary here'
                      }
        labels = {'name':'Submitter Name','email':'Submitter Email','phone':'Submitter Phone','pi_name':'PI Name','pi_email':'PI Email','biocore':'Will the Bioinformatics Core be analyzing the data?'}
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
#         if not submission.status:
#             submission.status = SubmissionStatus.objects.filter(default=True).order_by('order').first()
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
class AnonSubmissionFormUpdate(SubmissionForm):
    def __init__(self, *args, **kwargs):
        super(AnonSubmissionFormUpdate, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['email'].widget.attrs['readonly'] = True
    def clean_email(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.email
        else:
            return self.cleaned_data['email']
#     class Meta:
#         model = Submission
#         exclude = ['submitted','sample_data','sra_data','status','internal_id','email']
#     layout = material.base.Layout(
#         'participants',
#         material.base.Row('name','phone'),
#         material.base.Row('pi_name', 'pi_email'),
#         'institute',
#         'notes',
#         'type',
#         'sample_form',
#         'sra_form',
#         'biocore',
#     )
class AdminSubmissionForm(SubmissionForm):
    class Meta:
        model = Submission
        exclude = ['submitted','sample_data','sra_data','status','internal_id']
    layout = material.base.Layout(
        'participants',
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

class ValidatorForm(forms.ModelForm):
    class Meta:
        model = Validator
        exclude = []
        help_texts = {
                      'regex':'Enter a valid regular expression to validate against. Example for matching values such as "20.3 ul": ^\d+(\.{1}\d+)? ul$',
                      'choices':'Enter comma delimited choices.',
                      'range':'Enter a numeric range.  You may enter a min, max, or both.'
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

class SubmissionTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionTypeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance:
            self.fields['exclude_fields'].help_text += '  Current options are: '+', '.join(instance.samplesheet.headers)
    class Meta:
        model = SubmissionType
        exclude = []
        help_texts = {
                      'prefix':"This will be prepended to the submission's internal id.",
                      'header_index':'Which row are the variables on?',
                      'skip_rows':'The number of rows after the variables to ignore.  This is useful if providing examples.',
                      'start_column':'What column (A-Z) do variables start on.',
                      'end_column':'What column (A-Z) do variables end on?',
                      'sample_identifier': 'What is in the header for the sample name/id column?',
                      'form': 'Please upload a template in XLSX format, minimally containing variable names in one row.',
                      'exclude_fields': 'Comma delimited list of variables that should not be printed out by default.'
                      }
        labels = {
                'header_index': 'Variable row'
            }
        widgets = {
                'form':ClearableFileInput
            }

class CustomPrintForm(forms.Form):
    exclude = forms.MultipleChoiceField(label="Exclude variables")#widget=forms.CheckboxSelectMultiple
    vertical = forms.BooleanField(label="Vertical (layout samples in columns instead of rows)")
    max_samples = forms.IntegerField(label="Maximum number of samples per page")
    def __init__(self,submission,*args,**kwargs):
        super(CustomPrintForm, self).__init__(*args,**kwargs)
        self.fields['exclude'].choices = zip(submission.samplesheet.headers,submission.samplesheet.headers)
#     layout = material.base.Layout(
#         'exclude',
#         material.base.Row('vertical', 'max_samples'),
#     )
