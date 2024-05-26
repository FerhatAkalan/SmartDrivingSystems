# detectionapp/forms.py

from django import forms
from report.models import Driver, Trips
from .models import UploadedFile

from django import forms
from django.core.exceptions import ValidationError
from report.models import Driver
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Kullanıcıyı init'te al
        super(UploadFileForm, self).__init__(*args, **kwargs)
        if self.user:
            self.fields['driver'].queryset = Driver.objects.filter(user=self.user)

    driver = forms.ModelChoiceField(queryset=Driver.objects.none(), label="Driver", required=True)
    start_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    end_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), required=False)
    car_inside_file = forms.FileField(label="Upload In-car Video (Supported formats: JPG, MP4)", required=True, help_text="Supported formats: JPG, MP4")
    car_outside_file = forms.FileField(label="Upload Out-car Video (Supported formats: JPG, MP4)", required=True, help_text="Supported formats: JPG, MP4")
    car_data_file = forms.FileField(label="Upload Car Data (CSV File)", required=True, help_text="Supported format: CSV")

    class Meta:
        model = UploadedFile
        fields = ['car_inside_file', 'car_outside_file', 'car_data_file', 'driver', 'start_time', 'end_time']

    def clean_car_inside_file(self):
        file = self.cleaned_data['car_inside_file']
        if not file.name.endswith(('.jpg', '.jpeg', '.mp4')):
            raise ValidationError("Invalid file format. Please upload a JPG or MP4 file.")
        return file

    def clean_car_outside_file(self):
        file = self.cleaned_data['car_outside_file']
        if not file.name.endswith(('.jpg', '.jpeg', '.mp4')):
            raise ValidationError("Invalid file format. Please upload a JPG or MP4 file.")
        return file

    def clean_car_data_file(self):
        file = self.cleaned_data['car_data_file']
        if not file.name.endswith('.csv'):
            raise ValidationError("Invalid file format. Please upload a CSV file.")
        return file

    def save(self, commit=True):
        instance = super(UploadFileForm, self).save(commit=False)
        instance.user = self.user  # Kullanıcıyı atama
        if commit:
            instance.save()
        return instance
