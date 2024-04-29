from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    driver_surname = models.CharField(max_length=100)
    driver_licence = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.driver_name} {self.driver_surname}"

class Trips(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    file_path = models.TextField()
    
    def __str__(self):
        return f"Trip for {self.driver} from {self.start_time} to {self.end_time}"

class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    report_text = models.TextField()
    report_path = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    total_frames = models.IntegerField()

class ReportDetails(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    label = models.CharField(max_length=10)
    confidence = models.FloatField()
    top_left_x = models.FloatField()
    top_left_y = models.FloatField()
    bottom_right_x = models.FloatField()
    bottom_right_y = models.FloatField()
    center_x = models.FloatField()
    center_y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    masks = models.JSONField(null=True, blank=True)
    keypoints = models.JSONField(null=True, blank=True)
    probabilities = models.JSONField(null=True, blank=True)
    frame_info = models.IntegerField()  # Frame information
    
    def __str__(self):
        return f"Report Details for {self.report}"