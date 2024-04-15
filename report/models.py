from django.db import models
from django.contrib.auth.models import User

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    driver_surname = models.CharField(max_length=100)
    driver_licence = models.CharField(max_length=50)

class Trips(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    video_path = models.CharField(max_length=255)

class Reports(models.Model):
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    report_text = models.TextField()
    report_path = models.CharField(max_length=255)

