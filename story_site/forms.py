from django import forms

class UploadAudioFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)
    file = forms.FileField()
