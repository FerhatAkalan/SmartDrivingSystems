from django.shortcuts import render
from django.conf import settings


def add_driver(request):
    return render(request, 'report/add-driver.html')