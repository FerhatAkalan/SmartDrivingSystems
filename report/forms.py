from django import forms
from .models import Driver

class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = ['user','driver_name', 'driver_surname', 'driver_licence']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Oturum açmış kullanıcıyı alın
        super(DriverForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  # Form oluşturulduğunda 'user' alanını otomatik olarak ayarlayın
            self.fields['user'].widget.attrs['readonly'] = True  # 'user' alanını değiştirilemez yapın
