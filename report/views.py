import base64
import io
from django.shortcuts import get_object_or_404, render, redirect
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
from .forms import DriverForm
from .models import Driver, ReportDetails, SpeedingViolationDetails
from .models import Reports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import Http404
import matplotlib
matplotlib.use('Agg')


@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            if form.cleaned_data['user'] != request.user:
                raise Http404("You are not allowed to add driver for other users.")
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm(user=request.user)
    return render(request, 'add-driver.html', {'form': form})

@login_required
def driver_list(request):
    drivers = Driver.objects.filter(user=request.user)  # Tüm sürücüleri alır
    return render(request, 'driver-list.html', {'drivers': drivers})

from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Reports, Driver

@login_required
def driver_reports(request, driver_id=None):
    # Eğer driver_id belirtilmemişse, kullanıcının kendi raporlarını göster
    if driver_id:
        driver = get_object_or_404(Driver, pk=driver_id)
        report_list = Reports.objects.filter(trip__driver=driver)
    else:
        report_list = Reports.objects.filter(trip__driver__user=request.user)
    
    report_list = report_list.order_by('-created_at')

    paginator = Paginator(report_list, 6)  # Sayfa başına 6 rapor
    page = request.GET.get('page')
    try:
        reports = paginator.page(page)
    except PageNotAnInteger:
        # page parametresi bir tam sayı değilse, ilk sayfayı al
        reports = paginator.page(1)
    except EmptyPage:
        # page parametresi mevcut sayfa sayısından fazlaysa, son sayfayı al
        reports = paginator.page(paginator.num_pages)
    
    return render(request, 'driver-reports.html', {'reports': reports})

@login_required
def report_details(request, report_id):
    # Veritabanından rapor detaylarını al
    report = get_object_or_404(Reports, pk=report_id)
    violations = SpeedingViolationDetails.objects.filter(report_id=report_id).order_by('violation_time')

    report_details_interior = ReportDetails.objects.filter(report_id=report_id, is_car_interior=True)
    report_details_exterior = ReportDetails.objects.filter(report_id=report_id, is_car_interior=False)
    
    label_counts_interior = ReportDetails.objects.filter(report=report, is_car_interior=True).values('label').annotate(count=Count('label'))
    label_counts_exterior = ReportDetails.objects.filter(report=report, is_car_interior=False).values('label').annotate(count=Count('label'))
    
    times = [violation.violation_time for violation in violations]
    speeds = [violation.detected_speed for violation in violations]
    speed_limits = [violation.speed_limit for violation in violations]


    context = {
        'report': report,
        'report_details_interior': report_details_interior,
        'report_details_exterior': report_details_exterior,
        'label_counts_interior': label_counts_interior,
        'label_counts_exterior': label_counts_exterior,
        'violations': violations,
        'times': times,
        'speeds': speeds,
        'speed_limits': speed_limits,
    }
    return render(request, 'report-details.html', context)


@login_required
def driver_profiles(request, driver_id):
    # Veritabanından rapor detaylarını al
    driver = get_object_or_404(Driver, pk=driver_id)
   
    
    context = {
        'driver': driver,
    
    }
    return render(request, 'driver-profiles.html', context)


