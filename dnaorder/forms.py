from django import forms

class CustomPrintForm(forms.Form):
    exclude = forms.MultipleChoiceField(label="Exclude variables")#widget=forms.CheckboxSelectMultiple
    vertical = forms.BooleanField(label="Vertical (layout samples in columns instead of rows)")
    max_samples = forms.IntegerField(label="Maximum number of samples per page")
    def __init__(self,submission,*args,**kwargs):
        super(CustomPrintForm, self).__init__(*args,**kwargs)
        self.fields['exclude'].choices = zip(submission.samplesheet.headers,submission.samplesheet.headers)
