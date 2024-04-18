from django import forms

from report.models import Driver, Trips
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    driver = forms.ModelChoiceField(queryset=Driver.objects.all(), label="Driver")
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    class Meta:
        model = UploadedFile
        fields = ['file', 'driver', 'start_time', 'end_time']

