from django.urls import path
from .views import upload_file, results

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('results/', results, name='results'),
]
