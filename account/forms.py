from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Bu e-posta adresi zaten kullanılıyor.")
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if len(first_name) > 50:
            raise ValidationError("İsim çok uzun.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if len(last_name) > 50:
            raise ValidationError("Soyisim çok uzun.")
        return last_name
