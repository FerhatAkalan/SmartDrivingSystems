from django.db import models

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=100)
    userSurname = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
