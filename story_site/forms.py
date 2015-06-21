from django import forms
from .models import Language, Country, Region, Dialect, City

class UploadAudioFileForm(forms.Form):
    langObjs = Language.objects.all()
    regObjs = Region.objects.all()
    countryObjs = Country.objects.all()
    
    title = forms.CharField(max_length=50)
    description = forms.CharField(max_length=500)
    language = forms.ModelChoiceField(queryset = langObjs, empty_label=None)
    region = forms.ModelChoiceField(queryset = regObjs, empty_label=None)
    country = forms.ModelChoiceField(queryset = countryObjs, empty_label=None)
    dialect = forms.ModelChoiceField(queryset = Dialect.objects.all(), empty_label=None)
    # city = forms.ModelChoiceField(queryset = City.objects.all(), empty_label=None)

    file = forms.FileField()


class NoTitleSearchForm(forms.Form):
    langObjs = Language.objects.all()
    language = forms.ModelChoiceField(queryset = langObjs, empty_label=None)

    regObjs = Region.objects.all()
    region = forms.ModelChoiceField(queryset = regObjs, empty_label=None)

    countryObjs = Country.objects.all()
    country = forms.ModelChoiceField(queryset = countryObjs, empty_label=None)

    
    
