from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user','driver_name', 'driver_surname', 'driver_licence','driver_photo']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Oturum açmış kullanıcıyı alın
        super(DriverForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Form oluşturulduğunda 'user' alanını otomatik olarak ayarlayın
            self.fields['user'].widget.attrs['readonly'] = True  # 'user' alanını değiştirilemez yapın
    def clean(self):
        cleaned_data = super().clean()
        driver_name = cleaned_data.get("driver_name")
        driver_surname = cleaned_data.get("driver_surname")
        driver_licence = cleaned_data.get("driver_licence")
        driver_photo = cleaned_data.get("driver_photo")

        if not (driver_name and driver_surname and driver_licence and driver_photo):
            raise forms.ValidationError("Tüm alanları doldurunuz!")
        return cleaned_data
    def clean_driver_photo(self):
            driver_photo = self.cleaned_data.get('driver_photo', False)
            if driver_photo:
                if not driver_photo.content_type or not driver_photo.content_type.startswith('image'):
                    raise forms.ValidationError('Only image files are allowed.')
            return driver_photo
