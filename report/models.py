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
    car_inside_file_path = models.TextField(null=True, blank=True)
    car_outside_file_path = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"Trip for {self.driver} from {self.start_time} to {self.end_time}"

class Reports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trips, on_delete=models.CASCADE)
    report_text = models.TextField()
    car_inside_report_path = models.TextField()
    car_outside_report_path = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
<<<<<<< HEAD
    total_frames_inside = models.IntegerField()
    total_frames_outside = models.IntegerField()

    def __str__(self):
        return f"Report for {self.driver} - {self.created_at}"
=======
    total_frames = models.IntegerField()
>>>>>>> 98edbe154e192af30c55f166f9544ed12d278430

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
<<<<<<< HEAD
    frame_info = models.IntegerField()
    is_car_interior = models.BooleanField(default=False)
=======
    masks = models.JSONField(null=True, blank=True)
    keypoints = models.JSONField(null=True, blank=True)
    probabilities = models.JSONField(null=True, blank=True)
    frame_info = models.IntegerField()  # Frame information
    
>>>>>>> 98edbe154e192af30c55f166f9544ed12d278430
    def __str__(self):
        return f"Report Details for {self.report}"
