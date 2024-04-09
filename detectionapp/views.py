from django.shortcuts import render
from ultralytics import settings as ultralytics_settings
from .forms import UploadFileForm
import os
from ultralytics import YOLO
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'detectionapp/home.html')

def about(request):
    return render(request, 'detectionapp/about.html')

def contact(request):
    return render(request, 'detectionapp/contact.html')

# Ultralytics ayarlarını güncelle
ultralytics_settings.update({'runs_dir': os.path.join('detectionapp/static/detectionapp/runs')})

# Sonuçların kaydedileceği dizin
results_dir = os.path.join('detectionapp/static/detectionapp/runs/detect')
os.makedirs(results_dir, exist_ok=True)

def detect_dangerous_behavior(file_path, results_dir):
    # YOLO modelini yükle"
    model = YOLO(os.path.join('detectionapp/static/detectionapp/model/best.pt'))
    # Resim veya videoyu analiz et ve sonuçları kaydet
    results = model.predict(file_path, save=True, conf=0.5, save_dir=results_dir)
    print("Results:", results)
    # Sonuçları işleyip döndür
    return results

def get_latest_prediction(results_dir):
    # En son oluşturulan sonuç dosyasının yolunu bul
    latest_file = None
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.mp4') or file.endswith('.avi'):
                file_path = os.path.join(root, file)
                if latest_file is None or os.path.getmtime(file_path) > os.path.getmtime(latest_file):
                    latest_file = file_path
    
    # results_dir başındaki "detectionapp/static" kısmını kaldır
    if latest_file is not None:
        latest_file = latest_file.replace("detectionapp/static/", "")
    
    print("abc: " + latest_file)
 
    return latest_file


class_labels = {
    0: "Drinking",
    1: "Texting",
    # Add more class labels as needed
}

@login_required
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

            # Çıkarım sonuçlarını işleyerek bir grafik oluştur
            data = []
            for result in results:
                if result.boxes.cls is not None and len(result.boxes.cls) > 0:  # Eğer cls listesi boş değilse
                    label = class_labels.get(int(result.boxes.cls[0]), "Unknown")  # Map class index to label
                    confidence = float(result.boxes.conf[0])  # Convert tensor to float
                    x_min, y_min = float(result.boxes.xyxy[0][0]), float(result.boxes.xyxy[0][1])  # Convert tensors to float
                    x_max, y_max = float(result.boxes.xyxy[0][2]), float(result.boxes.xyxy[0][3])  # Convert tensors to float
                    x_center, y_center = float(result.boxes.xywh[0][0]), float(result.boxes.xywh[0][1])  # Convert tensors to float
                    width, height = float(result.boxes.xywh[0][2]), float(result.boxes.xywh[0][3])  # Convert tensors to float
                    masks = result.masks
                    keypoints = result.keypoints
                    probs = result.probs

                    # Append the formatted details to the list
                    data.append({
                        'label': label,
                        'confidence': confidence,
                        'x_min': x_min,
                        'y_min': y_min,
                        'x_max': x_max,
                        'y_max': y_max,
                        'x_center': x_center,
                        'y_center': y_center,
                        'width': width,
                        'height': height,
                        'masks': masks,
                        'keypoints': keypoints,
                        'probs': probs,
                    })
                else:
                    # cls listesi boşsa, labeli Unknown olarak işaretle
                    label = "Unknown"
                    confidence = 0.0
                    x_min = y_min = x_max = y_max = x_center = y_center = width = height = 0.0
                    masks = keypoints = probs = None

                    # Append the formatted details to the list
                    data.append({
                        'label': label,
                        'confidence': confidence,
                        'x_min': x_min,
                        'y_min': y_min,
                        'x_max': x_max,
                        'y_max': y_max,
                        'x_center': x_center,
                        'y_center': y_center,
                        'width': width,
                        'height': height,
                        'masks': masks,
                        'keypoints': keypoints,
                        'probs': probs,
                    })

            # Sonucu template'e gönder
            return render(request, 'detectionapp/result.html', {'results': results, 'latest_file': latest_file, 'data': data})
    else:
        form = UploadFileForm()
    
    return render(request, 'detectionapp/upload.html', {'form': form})
