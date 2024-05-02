from django.shortcuts import get_object_or_404, render, redirect
from .forms import DriverForm
from .models import Driver, ReportDetails
from .models import Reports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import Http404

@login_required
def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST, user=request.user)
        if form.is_valid():
            # Ek bir kontrol: Eğer formdaki kullanıcı, oturum açmış olan kullanıcı değilse, 404 hatası gönder
            if form.cleaned_data['user'] != request.user:
                raise Http404("You are not allowed to add driver for other users.")
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()
    return render(request, 'add-driver.html', {'form': form})

@login_required
def driver_list(request):
    drivers = Driver.objects.filter(user=request.user)  # Tüm sürücüleri alır
    return render(request, 'driver-list.html', {'drivers': drivers})

@login_required
def driver_reports(request):
    report_list = Reports.objects.filter(trip__driver__user=request.user).order_by('-created_at')  # Oturum açmış kullanıcının raporlarını filtrele
    paginator = Paginator(report_list, 6)  # Sayfa başına 10 rapor
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
    report_details = ReportDetails.objects.filter(report_id=report_id)
    label_counts = ReportDetails.objects.filter(report=report).values('label').annotate(count=Count('label'))

    context = {
        'report':report,
        'report_details': report_details,
        'label_counts': label_counts

    }
    return render(request, 'report-details.html', context)