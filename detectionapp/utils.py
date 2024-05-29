# utils.py
import os
import ffmpeg
from ultralytics import YOLO, settings as ultralytics_settings
from report.models import Driver, ReportDetails, Reports, Trips, SpeedingViolationDetails
from .models import UploadedFile
from account.models import UserSettings
from .labels import inside_class_labels, outside_class_labels
from .speedlabels import speed_labels
import csv
from datetime import datetime

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
ultralytics_settings.update({'runs_dir': os.path.join('detectionapp/static/detectionapp/runs')})
results_dir = os.path.join('detectionapp/static/detectionapp/runs/detect')
os.makedirs(results_dir, exist_ok=True)
vid_stride=1
def get_user_settings(user):
    try:
        user_settings = UserSettings.objects.get(user=user)
        return user_settings.vid_stride, user_settings.confidence
    except UserSettings.DoesNotExist:
        return 10, 0.5

def detect_dangerous_behavior(file_path, user, isOutside=False):
    vid_stride, confidence = get_user_settings(user)
    if isOutside:
        model = YOLO(os.path.join('detectionapp/static/detectionapp/model/best_outside2.pt'))
        results = model.predict(file_path, save=True, conf=0.9, save_dir=results_dir, vid_stride=vid_stride)
    else:
        model = YOLO(os.path.join('detectionapp/static/detectionapp/model/best50.pt'))
        results = model.predict(file_path, save=True, conf=confidence, save_dir=results_dir, vid_stride=vid_stride)
    #results = model.predict(file_path, save=True, conf=confidence, save_dir=results_dir, vid_stride=vid_stride)
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

def process_results(results, car_data_file_path, is_car_interior):
    data = []
    total_frames = len(results)
    # CSV dosyasını bir kere oku
    with open(car_data_file_path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        car_data = list(reader)
    for i, result in enumerate(results):
        current_info= i+1
        frame_info = f"{i+1}/{total_frames}"
        if result.boxes.cls is not None and len(result.boxes.cls) > 0:
            label = inside_class_labels.get(int(result.boxes.cls[0]), "Unknown") if is_car_interior else outside_class_labels.get(int(result.boxes.cls[0]), "Unknown")
            confidence = round(float(result.boxes.conf[0]),3)
            x_min, y_min = round(float(result.boxes.xyxy[0][0]),3), round(float(result.boxes.xyxy[0][1]),3)
            x_max, y_max = round(float(result.boxes.xyxy[0][2]),3), round(float(result.boxes.xyxy[0][3]),3)
            x_center, y_center = round(float(result.boxes.xywh[0][0]),3), round(float(result.boxes.xywh[0][1]),3)
            width, height = round(float(result.boxes.xywh[0][2]),3), round(float(result.boxes.xywh[0][3]),3)
            current_frame = int(frame_info.split('/')[0])
            time_of_detection = (current_frame / 30)
            if is_car_interior == False and label in speed_labels:
                speed_limit = speed_labels.get(label)
                closest_time = None
                closest_speed = None
                min_time_diff = float('inf')
                # Önceden okunan CSV verilerini kullan
                for row in car_data:
                    csv_time = datetime.strptime(row['Time'], '%H:%M:%S')
                    csv_seconds = (csv_time.hour * 3600) + (csv_time.minute * 60) + csv_time.second
                    time_diff = abs(float(time_of_detection) - csv_seconds)
                    if time_diff < min_time_diff:
                        min_time_diff = time_diff
                        closest_time = csv_time
                        closest_speed = float(row['Arac Hizi (km/h)'])
                
                if closest_speed > speed_limit:
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
                        'current_info': current_info,
                        'is_car_interior': is_car_interior,
                        'time_of_detection': time_of_detection,
                        'speed_limit': speed_limit,
                        'detected_speed': closest_speed,
                        'violation_time': closest_time,
                    })
                    print("İf Speed Limit: ", speed_limit, " CSV File Speed: ", closest_speed, " Closest Time from CSV: ", closest_time, " Detected Time: ", time_of_detection)
                else:
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
                        'current_info': current_info,
                        'is_car_interior': is_car_interior,
                        'time_of_detection': time_of_detection,
                    })
            else:
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
                    'is_car_interior': is_car_interior,
                    'time_of_detection': time_of_detection
                })
    return data

def create_report(user, trip, inside_results, car_inside_latest_file, outside_results, car_outside_latest_file, total_frames_inside, total_frames_outside, car_data_file_path):
    report = Reports.objects.create(
            user=user,
            driver=trip.driver,
            trip=trip,
            report_text="Detection results for dangerous behavior",
            car_inside_report_path=car_inside_latest_file,
            car_outside_report_path=car_outside_latest_file,
            car_data_report_path=car_data_file_path,
            total_frames_inside=total_frames_inside,
            total_frames_outside=total_frames_outside,
    )
     
    for entry in process_results(inside_results, car_data_file_path, is_car_interior=True):
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

    for entry in process_results(outside_results, car_data_file_path, is_car_interior=False):
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
        # Hız sınırı ihlali varsa
        if 'speed_limit' in entry:
            speed_limit_violation = SpeedingViolationDetails.objects.create(
                report=report,
                speed_limit=entry['speed_limit'],
                detected_speed=entry['detected_speed'],
                violation_time=entry['time_of_detection'])
            speed_limit_violation.save()

    return report
