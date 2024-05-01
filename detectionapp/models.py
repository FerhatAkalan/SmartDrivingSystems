from django.db import models
from django.apps import apps

class UploadedFile(models.Model):
    car_inside_file = models.FileField(upload_to='uploads/', verbose_name="In-car File")
    car_outside_file = models.FileField(upload_to='uploads/', verbose_name="Out-car File")

    class Meta:
        app_label = apps.get_app_config('detectionapp').name
