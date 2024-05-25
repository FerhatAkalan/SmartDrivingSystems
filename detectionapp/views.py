from django.shortcuts import render
from report.models import Trips
from .forms import UploadFileForm
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .utils import detect_dangerous_behavior, process_results, get_latest_prediction, create_report

def home(request):
    return render(request, 'detectionapp/home.html')
def about(request):
    return render(request, 'detectionapp/about.html')
def contact(request):
    return render(request, 'detectionapp/contact.html')
def help(request):
    return render(request, 'detectionapp/help.html')

@login_required
def upload_file(request):
    initial_values = {'confidence': request.user.usersettings.confidence, 'vid_stride': request.user.usersettings.vid_stride}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            # Dosyayı kaydet
            uploaded_file = form.save()
            driver = form.cleaned_data.get('driver')
            # Trips modeline yeni bir örnek oluştur ve video_path alanını kaydet
            trip = Trips.objects.create(
                driver=driver,  # Kullanıcının sürücü profilini alır
                start_time=form.cleaned_data['start_time'],  # Formdan alınan başlangıç zamanı
                end_time=form.cleaned_data['end_time'],  # Formdan alınan bitiş zamanı
                car_inside_file_path=uploaded_file.car_inside_file.path, 
                car_outside_file_path=uploaded_file.car_outside_file.path   
            )
            return render(request, 'detectionapp/uploaded_file.html', {'uploaded_file': uploaded_file, 'trip': trip})
    else:
        form = UploadFileForm(user=request.user, initial=initial_values)
    return render(request, 'detectionapp/upload.html', {'form': form})

@login_required
def results(request):
    if request.method == 'POST':
        file_id = request.POST.get('file_id')
        trip_id = request.POST.get('trip_id')
        uploaded_file = UploadedFile.objects.get(id=file_id)
        trip = Trips.objects.get(id=trip_id)
        # Tehlikeli davranışları tespit et ve sonuçları işle
        car_inside_file_path = trip.car_inside_file_path
        car_outside_file_path = trip.car_outside_file_path
        # Car Inside Results
        car_inside_results = detect_dangerous_behavior(car_inside_file_path, user=request.user)
        car_inside_latest_file = get_latest_prediction()
        # Car Outside Results
        car_outside_results = detect_dangerous_behavior(car_outside_file_path, isOutside=True, user=request.user)
        car_outside_latest_file = get_latest_prediction()
        total_frames_inside = len(car_inside_results)  
        total_frames_outside = len(car_outside_results) 
        # Çıkarım sonuçlarını işleyerek bir grafik oluştur

        # İşlenmiş dosyanın yolunu Reports modelinde kaydedin
        data_inside = process_results(car_inside_results,is_car_interior=True)
        data_outside = process_results(car_outside_results,is_car_interior=False)
        report = create_report(request.user, trip, car_inside_results, car_inside_latest_file, car_outside_results ,car_outside_latest_file,total_frames_inside,total_frames_outside)

        # Pass the processed data and other context to the template
        context = {
            'report': report,
            'data_inside': data_inside,
            'data_outside': data_outside,
        }
        return render(request, 'detectionapp/results.html', context)
    else:
        # Handle GET request (if needed)
        pass