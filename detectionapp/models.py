from django.db import models
from django.apps import apps

# Create your models here.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField()
    user_surname = models.CharField()
    user_company = models.CharField()

class File(models.Model):
    file_id = models.AutoField(primary_key=True)
    userId = models.ForeignKey(User,on_delete=models.SET_NULL)
    file_name = models.CharField()
    upload_timestamp = models.DateTimeField()

class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    fileId = models.ForeignKey(File,on_delete=models.SET_NULL)
    issue = models.CharField()
    confidence_score = models.IntegerField()
    output_video_path = models.TextField()
