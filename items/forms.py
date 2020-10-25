from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(required=True, label='Archivo', widget=forms.FileInput(attrs={'accept':'video/*'}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs['class'] = 'form-control-file'
