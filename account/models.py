from django.db import models

# class Users(models.Model):
#     userId = models.AutoField(primary_key=True)
#     userName = models.CharField(max_length=100)
#     userSurname = models.CharField(max_length=100)
#     email = models.EmailField()
#     password = models.CharField(max_length=100)
#     isAdmin = models.BooleanField(default=False)
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vid_stride = models.IntegerField(default=1)
    confidence = models.FloatField(default=0.5)

    def __str__(self):
        return f"Settings for {self.user.username}"
