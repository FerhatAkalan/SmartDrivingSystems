from django.db import models
from account.models import Users

class Driver(models.Model):
    driverId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(Users, on_delete=models.CASCADE)
    driverName = models.CharField(max_length=100)
    driverSurname = models.CharField(max_length=100)
    driverLicence = models.CharField(max_length=100)

class Trips(models.Model):
    tripId = models.AutoField(primary_key=True)
    driverId = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    video_path = models.CharField(max_length=255)

class Reports(models.Model):
    reportId = models.AutoField(primary_key=True)
    tripId = models.ForeignKey(Trips, on_delete=models.CASCADE)
    report_content = models.TextField()
    report_filename = models.CharField(max_length=255)