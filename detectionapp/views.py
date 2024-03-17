from django.shortcuts import render
from .forms import UploadFileForm
import os
from ultralytics import YOLO

# Sonuçların kaydedileceği dizin
results_dir = 'C:/Users/Ferhat/smartdrivingsystems/runs/detect'
os.makedirs(results_dir, exist_ok=True)

def detect_dangerous_behavior(file_path, results_dir):
    # YOLO modelini yükle
    model = YOLO('C:/Users/Ferhat/Downloads/best.pt')

    # Resim veya videoyu analiz et ve sonuçları kaydet
    results = model.predict(file_path, save=True, conf=0.5, save_dir=results_dir)

    # Sonuçları işleyip döndür
    return results

def get_latest_prediction(results_dir):
    # En son oluşturulan sonuç dosyasının yolunu bul
    latest_file = None
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.mp4'):
                file_path = os.path.join(root, file)
                if latest_file is None or os.path.getmtime(file_path) > os.path.getmtime(latest_file):
                    latest_file = file_path
    print(latest_file)

    return latest_file

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # Dosyayı kaydet
            form.save()

            # Modelden dönen sonuçları al
            file_path = form.instance.file.path
            results = detect_dangerous_behavior(file_path, results_dir)

            # Sonucun en son oluşturulan dosyasını al
            latest_file = get_latest_prediction(results_dir)

            # Sonucu template'e gönder
            return render(request, 'detectionapp/result.html', {'results': results, 'latest_file': latest_file})
    else:
        form = UploadFileForm()
    return render(request, 'detectionapp/upload.html', {'form': form})
