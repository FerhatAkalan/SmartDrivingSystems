from django.contrib import admin
from django.urls import include, path
from detectionapp.views import upload_file
from . import views


urlpatterns = [
    path('add-driver/', views.add_driver,name="add_driver"),
    path('drivers/', views.driver_list, name='driver_list'),
    path('driver-reports/', views.driver_reports, name='driver_reports'),
    path('report-details/<int:report_id>/', views.report_details, name='report_details'),
]