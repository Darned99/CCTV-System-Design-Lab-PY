import cv2
import time
import datetime
import os
from pathlib import Path
import numpy as np

class CameraMonitor:
    # Statyczny licznik instancji
    instance_counter = 0

    def __init__(self, camera_id, seconds_to_record_after_detection=5, mode=1, retention_days=7):
        self.camera_id = camera_id
        self.seconds_to_record_after_detection = seconds_to_record_after_detection
        self.mode = mode  # 1: Wykrywanie ruchu, 2: Ciągłe nagrywanie
        self.retention_days = retention_days  # Liczba dni przechowywania nagrań

        # Przydzielenie unikalnego identyfikatora instancji
        CameraMonitor.instance_counter += 1
        self.instance_id = CameraMonitor.instance_counter

        # Tworzenie lokalnego folderu Videos
        self.output_dir = Path(os.path.abspath("Videos"))
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Usuwanie starych nagrań
        self.cleanup_old_videos()

        # Inicjalizacja kamery
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise ValueError(f"Camera {self.instance_id}: Unable to open stream.")

        # Rozdzielczość klatek
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.frame_size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # FPS i kodek
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        # Inicjalizacja detekcji
        self.detection = False
        self.recording = True
        self.detection_stopped_time = None
        self.timer_started = False
        self.out = None

        # Ładowanie klasyfikatorów
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.body_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_fullbody.xml"
        )

    def cleanup_old_videos(self):
        now = time.time()
        retention_period = self.retention_days * 86400  # Liczba sekund w dniu

        for video_file in self.output_dir.glob("*.mp4"):
            file_mod_time = video_file.stat().st_mtime
            if now - file_mod_time > retention_period:
                video_file.unlink()  # Usuwanie pliku
                print(f"Usunięto stary plik: {video_file}")

    def set_mode(self, mode):
        self.mode = mode

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return False

        if self.mode == 1:  # Wykrywanie ruchu
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            bodies = self.body_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) + len(bodies) > 0:
                if not self.detection:
                    self.detection = True
                    current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                    video_filename = self.output_dir / f"camera_{self.instance_id}_{current_time}.mp4"
                    self.out = cv2.VideoWriter(str(video_filename), self.fourcc, self.fps, self.frame_size)
                self.timer_started = False
            elif self.detection:
                if not self.timer_started:
                    self.detection_stopped_time = time.time()
                    self.timer_started = True
                elif time.time() - self.detection_stopped_time > self.seconds_to_record_after_detection:
                    self.detection = False
                    self.timer_started = False
                    if self.out:
                        self.out.release()
                        self.out = None
                        print('Stopped recording')

            if self.detection and self.out:
                self.out.write(frame)

        elif self.mode == 2:  # Ciągłe nagrywanie
            if not self.out:
                current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
                video_filename = self.output_dir / f"camera_{self.instance_id}_{current_time}.mp4"
                self.out = cv2.VideoWriter(str(video_filename), self.fourcc, self.fps, self.frame_size)
            self.out.write(frame)

        return frame

    def release_resources(self):
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
        cv2.destroyAllWindows()
