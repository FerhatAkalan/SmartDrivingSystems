from django.db import models
from django.apps import apps

# Create your models here.
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')

    class Meta:
        app_label = apps.get_app_config('detectionapp').name
