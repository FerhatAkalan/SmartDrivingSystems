from django.contrib import admin
from django.urls import include, path
from detectionapp.views import upload_file
from smartdrivingsystems import settings
from . import views
from django.conf.urls.static import static


urlpatterns = [
    path('add-driver/', views.add_driver,name="add_driver"),
    path('drivers/', views.driver_list, name='driver_list'),
    path('driver-reports/', views.driver_reports, name='driver_reports'),
    path('report-details/<int:report_id>/', views.report_details, name='report_details'),
    path('driver-profiles/<int:driver_id>/', views.driver_profiles, name='driver_profiles'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
