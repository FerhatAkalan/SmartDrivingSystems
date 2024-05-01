# detectionapp/forms.py

from django import forms
from report.models import Driver, Trips
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UploadFileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['driver'].queryset = Driver.objects.filter(user=user)

    driver = forms.ModelChoiceField(queryset=Driver.objects.none(), label="Driver")
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    car_inside_file = forms.FileField(label="Upload In-car Video (Supported formats: JPG, MP4)", required=True, help_text="Supported formats: JPG, MP4")
    car_outside_file = forms.FileField(label="Upload Out-car Video (Supported formats: JPG, MP4)", required=True, help_text="Supported formats: JPG, MP4")
    
    class Meta:
        model = UploadedFile
        fields = ['car_inside_file', 'car_outside_file', 'driver', 'start_time', 'end_time']
