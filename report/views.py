from django.shortcuts import render, redirect
from .forms import DriverForm
from .models import Driver
from .models import Reports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.http import Http404

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

def driver_list(request):
    drivers = Driver.objects.filter(user=request.user)  # Tüm sürücüleri alır
    return render(request, 'driver-list.html', {'drivers': drivers})

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