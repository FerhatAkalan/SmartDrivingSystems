from datetime import timedelta
from django.forms import DurationField
from django.shortcuts import get_object_or_404, render, redirect
from .forms import DriverForm
from .models import Driver, ReportDetails, SpeedingViolationDetails, Trips
from .models import Reports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db.models import Avg, F, ExpressionWrapper, DurationField
from datetime import timedelta



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



@login_required
def all_statistic(request):
    reports = Reports.objects.filter(user=request.user)
    report_count = reports.count() 
    unique_drivers_count = Driver.objects.filter(user=request.user).count()
    
    # Kullanıcının tüm raporlarındaki araç içi ve araç dışı etiketleri topla
    interior_labels = ReportDetails.objects.filter(report__in=reports, is_car_interior=True).values_list('label', flat=True)
    exterior_labels = ReportDetails.objects.filter(report__in=reports, is_car_interior=False).values_list('label', flat=True)
    
    # Etiketlerin sayısını hesapla
    interior_label_counts = {}
    exterior_label_counts = {}
    for label in interior_labels:
        if label in interior_label_counts:
            interior_label_counts[label] += 1
        else:
            interior_label_counts[label] = 1
    for label in exterior_labels:
        if label in exterior_label_counts:
            exterior_label_counts[label] += 1
        else:
            exterior_label_counts[label] = 1
    
    # Etiketleri ve sayımlarını JSON olarak döndür
    interior_labels = list(interior_label_counts.keys())
    interior_counts = list(interior_label_counts.values())
    exterior_labels = list(exterior_label_counts.keys())
    exterior_counts = list(exterior_label_counts.values())

        
    # Ortalama sürüş süresini hesapla
    trips = Trips.objects.filter(driver__user=request.user)
    trips_with_duration = trips.annotate(duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=DurationField()))
    avg_trip_duration = trips_with_duration.aggregate(Avg('duration'))['duration__avg']

    # Ortalamayı saat, dakika ve saniye olarak formatla
    if avg_trip_duration:
        avg_seconds = int(avg_trip_duration.total_seconds())
        avg_minutes, avg_seconds = divmod(avg_seconds, 60)
        avg_hours, avg_minutes = divmod(avg_minutes, 60)
        avg_trip_duration_seconds = int(avg_trip_duration.total_seconds())
        avg_trip_duration_formatted = f"{avg_hours} saat, {avg_minutes} dakika, {avg_seconds} saniye"
    else:
        avg_trip_duration_seconds = 0
        avg_trip_duration_formatted = "N/A"
    
    
    context={
        'report':reports,
        'report_count': report_count,
        'unique_drivers_count': unique_drivers_count,
        'interior_labels': interior_labels,
        'interior_counts': interior_counts,
        'exterior_labels': exterior_labels,
        'exterior_counts': exterior_counts,
        'avg_trip_duration': avg_trip_duration_formatted,
        'avg_trip_duration_seconds': avg_trip_duration_seconds
    }
    
    return render(request, 'all-statistic.html',context)


