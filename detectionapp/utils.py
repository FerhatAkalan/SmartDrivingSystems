# utils.py
import os
import ffmpeg
from ultralytics import YOLO, settings as ultralytics_settings
from report.models import Driver, ReportDetails, Reports, Trips
from .models import UploadedFile
from account.models import UserSettings

from .labels import inside_class_labels, outside_class_labels

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
ultralytics_settings.update({'runs_dir': os.path.join('detectionapp/static/detectionapp/runs')})
results_dir = os.path.join('detectionapp/static/detectionapp/runs/detect')
os.makedirs(results_dir, exist_ok=True)

def get_user_settings(user):
    try:
        user_settings = UserSettings.objects.get(user=user)
        return user_settings.vid_stride, user_settings.confidence
    except UserSettings.DoesNotExist:
        # Kullanıcı ayarları bulunamadıysa varsayılan değerleri döndür
        return 10, 0.5

def detect_dangerous_behavior(file_path, user, isOutside=False):
    vid_stride, confidence = get_user_settings(user)
    if isOutside:
        model = YOLO(os.path.join('detectionapp/static/detectionapp/model/best_outside.pt'))
    else:
        model = YOLO(os.path.join('detectionapp/static/detectionapp/model/best50.pt'))
    
    results = model.predict(file_path, save=True, conf=confidence, save_dir=results_dir, vid_stride=vid_stride)
    #print("Results:", results)
    return results

def get_latest_prediction():
    latest_file = None
    for root, dirs, files in os.walk(results_dir):
        for file in files:
            if file.endswith('.jpg') or file.endswith('.mp4') or file.endswith('.avi'):
                file_path = os.path.join(root, file)
                if latest_file is None or os.path.getmtime(file_path) > os.path.getmtime(latest_file):
                    latest_file = file_path
    
    if latest_file.endswith('.avi'):
        mp4_file = latest_file.replace('.avi', '.mp4')
        try:
            ffmpeg.input(latest_file).output(mp4_file).run()
            latest_file = mp4_file
            print("AVI dosyası MP4'e dönüştürüldü:", mp4_file)
        except ffmpeg.Error as e:
            print("Dönüştürme sırasında bir hata oluştu:", e.stderr)
    
    if latest_file is not None:
        latest_file = latest_file.replace("detectionapp/static/", "")
        latest_file = latest_file.replace("\\", "/")
    print("Latest File: " + latest_file)
 
    return latest_file

def process_results(results, is_car_interior):
    data = []
    total_frames = len(results)
    for i, result in enumerate(results):
        current_info= i+1
        frame_info = f"{i+1}/{total_frames}"
        if result.boxes.cls is not None and len(result.boxes.cls) > 0:
            label = inside_class_labels.get(int(result.boxes.cls[0]), "Unknown") if is_car_interior else outside_class_labels.get(int(result.boxes.cls[0]), "Unknown")
            confidence = float(result.boxes.conf[0])
            x_min, y_min = float(result.boxes.xyxy[0][0]), float(result.boxes.xyxy[0][1])
            x_max, y_max = float(result.boxes.xyxy[0][2]), float(result.boxes.xyxy[0][3])
            x_center, y_center = float(result.boxes.xywh[0][0]), float(result.boxes.xywh[0][1])
            width, height = float(result.boxes.xywh[0][2]), float(result.boxes.xywh[0][3])
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
                'frame_info': frame_info,
                'current_info' : current_info,
                'is_car_interior': is_car_interior
            })
    return data

def create_report(user, trip, inside_results, car_inside_latest_file, outside_results, car_outside_latest_file,total_frames_inside,total_frames_outside ):
    report = Reports.objects.create(
            user=user,
            driver=trip.driver,
            trip=trip,
            report_text="Detection results for dangerous behavior",
            car_inside_report_path=car_inside_latest_file,
            car_outside_report_path=car_outside_latest_file,
            total_frames_inside=total_frames_inside,
            total_frames_outside=total_frames_outside,
    )
     
    for entry in process_results(inside_results, is_car_interior=True):
        report_detail = ReportDetails(
            report=report,
            label=entry['label'],
            confidence=entry['confidence'],
            top_left_x=entry['x_min'],
            top_left_y=entry['y_min'],
            bottom_right_x=entry['x_max'],
            bottom_right_y=entry['y_max'],
            center_x=entry['x_center'],
            center_y=entry['y_center'],
            width=entry['width'],
            height=entry['height'],
            frame_info=entry['current_info'],
            is_car_interior=True
        )
        report_detail.save()

    for entry in process_results(outside_results, is_car_interior=False):
        report_detail = ReportDetails(
            report=report,
            label=entry['label'],
            confidence=entry['confidence'],
            top_left_x=entry['x_min'],
            top_left_y=entry['y_min'],
            bottom_right_x=entry['x_max'],
            bottom_right_y=entry['y_max'],
            center_x=entry['x_center'],
            center_y=entry['y_center'],
            width=entry['width'],
            height=entry['height'],
            frame_info=entry['current_info'],
            is_car_interior=False
        )
        report_detail.save()

    return report
