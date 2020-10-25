from django import forms
from .common import LENGUAGES

class UploadFileForm(forms.Form):
    file = forms.FileField(required=True, label='Archivo', widget=forms.FileInput(attrs={'accept':'video/*'}))
    lenguage = forms.ChoiceField(choices=LENGUAGES)
    target = forms.ChoiceField(choices=LENGUAGES)

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        
        self.fields['file'].widget.attrs['class'] = 'form-control-file'
        self.fields['lenguage'].widget.attrs['class'] = 'form-control'
        self.fields['target'].widget.attrs['class'] = 'form-control'




