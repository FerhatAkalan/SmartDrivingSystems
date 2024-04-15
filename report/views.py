from django.shortcuts import render, redirect
from .forms import DriverForm
from .models import Driver

def add_driver(request):
    if request.method == 'POST':
        form = DriverForm(request.POST)
        if form.is_valid():
            # formu kaydettirmeden önce, user alanını oturum açmış kullanıcıya ayarlayın
            form.instance.user = request.user
            form.save()
            return redirect('driver_list')
    else:
        form = DriverForm()

    return render(request, 'add-driver.html', {'form': form})

def driver_list(request):
    drivers = Driver.objects.filter(user=request.user)  # Tüm sürücüleri alır
    return render(request, 'driver-list.html', {'drivers': drivers})