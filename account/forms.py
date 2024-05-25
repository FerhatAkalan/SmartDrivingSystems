from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserSettings

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

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ['vid_stride', 'confidence']

    def clean_vid_stride(self):
        vid_stride = self.cleaned_data.get('vid_stride')
        # Tür kontrolü
        if not isinstance(vid_stride, int):
            raise forms.ValidationError("Video Frame Stride tamsayı olmalıdır.")
        if vid_stride < 1:
            raise forms.ValidationError("Video Frame Stride en az 1 olmalıdır.")
        return vid_stride

    def clean_confidence(self):
        confidence = self.cleaned_data.get('confidence')
        # Tür kontrolü
        if not isinstance(confidence, (int, float)):
            raise ValidationError("Confidence bir sayı olmalıdır.")
        if confidence < 0 or confidence > 1:
            print("Confidence değeri 0 ile 1 arasında olmalıdır.")
            raise ValidationError("Confidence değeri 0 ile 1 arasında olmalıdır.")
        return confidence