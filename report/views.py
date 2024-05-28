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

    # Bar Plot oluşturma
    if(label_counts_interior and label_counts_exterior):
        interior_labels, interior_counts = zip(*[(item['label'], item['count']) for item in label_counts_interior])
        exterior_labels, exterior_counts = zip(*[(item['label'], item['count']) for item in label_counts_exterior])

        interior_plot_url = create_bar_plot(interior_labels, interior_counts, "İç Davranış Etiketleri", "Frekans")
        exterior_plot_url = create_bar_plot(exterior_labels, exterior_counts, "Dış Davranış Etiketleri", "Frekans")

        # Normal Dağılım, Ki-Kare Testi ve Üstel Dağılım analizleri
        normal_dist_plot_interior_url = create_normal_distribution_plot(report_details_interior, "İç Davranışlar İçin Normal Dağılım")
        exponential_dist_plot_interior_url = create_exponential_distribution_plot(report_details_interior, "İç Davranışlar İçin Üstel Dağılım")
        
        normal_dist_plot_exterior_url = create_normal_distribution_plot(report_details_exterior, "Dış Davranışlar İçin Normal Dağılım")
        exponential_dist_plot_exterior_url = create_exponential_distribution_plot(report_details_exterior, "Dış Davranışlar İçin Üstel Dağılım")
        
        chi_square_test_result_interior = perform_chi_square_test(label_counts_interior)
        chi_square_test_result_exterior = perform_chi_square_test(label_counts_exterior)

    times = [violation.violation_time for violation in violations]
    speeds = [violation.detected_speed for violation in violations]
    speed_limits = [violation.speed_limit for violation in violations]


    context = {
        'report': report,
        'report_details_interior': report_details_interior,
        'report_details_exterior': report_details_exterior,
        'label_counts_interior': label_counts_interior,
        'label_counts_exterior': label_counts_exterior,
        'interior_plot_url': interior_plot_url,
        'exterior_plot_url': exterior_plot_url,
        'normal_dist_plot_interior_url': normal_dist_plot_interior_url,
        'exponential_dist_plot_interior_url': exponential_dist_plot_interior_url,
        'normal_dist_plot_exterior_url': normal_dist_plot_exterior_url,
        'exponential_dist_plot_exterior_url': exponential_dist_plot_exterior_url,
        'chi_square_test_result_interior': chi_square_test_result_interior,
        'chi_square_test_result_exterior': chi_square_test_result_exterior,
        'violations': violations,
        'times': times,
        'speeds': speeds,
        'speed_limits': speed_limits,
    }
    return render(request, 'report-details.html', context)

def create_bar_plot(labels, counts, title, ylabel):
    plt.figure(figsize=(10, 6))
    plt.bar(labels, counts, color='skyblue')
    plt.xlabel('Etiketler')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return 'data:image/png;base64,' + graphic

def create_normal_distribution_plot(report_details, title):
    frame_infos = [detail.frame_info for detail in report_details]

    plt.figure(figsize=(10, 6))
    plt.hist(frame_infos, bins=30, density=True, alpha=0.6, color='r')

    mu, std = np.mean(frame_infos), np.std(frame_infos)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    p = stats.norm.pdf(x, mu, std)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title(f"{title}\nFit results: mu = {mu:.2f},  std = {std:.2f}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return 'data:image/png;base64,' + graphic

def perform_chi_square_test(label_counts):
    observed = [item['count'] for item in label_counts]
    expected = [np.mean(observed)] * len(observed)  # Beklenen değerler ortalama olarak alındı
    chi2, p = stats.chisquare(f_obs=observed, f_exp=expected)
    return f"Ki-Kare Değeri: {chi2:.2f}, p-değeri: {p:.2e}"

def create_exponential_distribution_plot(report_details, title):
    frame_infos = [detail.frame_info for detail in report_details]

    plt.figure(figsize=(10, 6))
    plt.hist(frame_infos, bins=30, density=True, alpha=0.6, color='g')

    lambda_param = 1 / np.mean(frame_infos)
    x = np.linspace(0, max(frame_infos), 100)
    p = lambda_param * np.exp(-lambda_param * x)
    plt.plot(x, p, 'k', linewidth=2)
    plt.title(f"{title}\nFit results: lambda = {lambda_param:.2f}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return 'data:image/png;base64,' + graphic


@login_required
def driver_profiles(request, driver_id):
    # Veritabanından rapor detaylarını al
    driver = get_object_or_404(Driver, pk=driver_id)
   
    
    context = {
        'driver': driver,
    
    }
    return render(request, 'driver-profiles.html', context)

