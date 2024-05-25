from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Driver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    driver_name = models.CharField(max_length=100)
    driver_surname = models.CharField(max_length=100)
    driver_licence = models.CharField(max_length=50, unique=True)
    driver_photo = models.ImageField(upload_to='driver_photos/', null=True, blank=True, 
                                     help_text="Maximum 2MB and allowed formats: JPG, JPEG, PNG") 
    created_at = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    driver_email = models.EmailField(null=True, blank=True)
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
    total_frames_inside = models.IntegerField()
    total_frames_outside = models.IntegerField()

    def __str__(self):
        return f"Report for {self.driver} - {self.created_at}"

class ReportDetails(models.Model):
    report = models.ForeignKey(Reports, on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    confidence = models.FloatField()
    top_left_x = models.FloatField()
    top_left_y = models.FloatField()
    bottom_right_x = models.FloatField()
    bottom_right_y = models.FloatField()
    center_x = models.FloatField()
    center_y = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    frame_info = models.IntegerField()
    is_car_interior = models.BooleanField(default=False)
    def __str__(self):
        return f"Report Details for {self.report}"
