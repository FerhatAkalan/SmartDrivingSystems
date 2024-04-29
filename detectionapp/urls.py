from django.urls import path
from .views import upload_file, results
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('results/', results, name='results'),
]
