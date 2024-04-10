from django.contrib import admin
from django.urls import include, path
from detectionapp.views import upload_file
from . import views


urlpatterns = [
    path('add-driver/', views.add_driver,name="add_driver"),
]