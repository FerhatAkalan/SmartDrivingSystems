from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user', 'driver_name', 'driver_surname', 'driver_licence']