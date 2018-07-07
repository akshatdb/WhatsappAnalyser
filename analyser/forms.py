from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    msgfile = forms.FileField()