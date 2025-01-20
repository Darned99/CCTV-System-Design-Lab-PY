import cv2
import time
import datetime
import os
from screeninfo import get_monitors

# Inicjalizacja kamer - numeracja zależy od liczby podłączonych urządzeń
camera1 = cv2.VideoCapture("rtsp://admin:hikvision1231@192.168.1.65:554/Streaming/channels/2/")
camera2 = cv2.VideoCapture(1)

# Ładowanie klasyfikatorów Haar do wykrywania twarzy i ciał
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Zmienne kontrolne dla procesu detekcji
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# Pobieranie rozdzielczości ekranu
monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

# Parametry nagrywania wideo
frame_width = int(camera1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera1.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Utworzenie katalogu Videos, jeśli nie istnieje
videos_dir = "../Videos"
os.makedirs(videos_dir, exist_ok=True)

# Nagrywanie ciągłe z kamery 2
out2 = cv2.VideoWriter(f"{videos_dir}/camera2_video.mp4", fourcc, 20.0, frame_size)

# Główna pętla programu
while True:
    # Odczyt klatek z obu kamer
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    if not ret1 or not ret2:
        print("Błąd: Nie udało się odczytać jednej z kamer.")
        break

    # Dopasowanie rozmiarów i typów danych, jeśli różne
    if frame1.shape[:2] != frame2.shape[:2]:
        frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))

    # Konwersja klatek na odcienie szarości
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Detekcja twarzy i ciał w klatkach
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    bodies1 = body_cascade.detectMultiScale(gray1, 1.3, 5)

    # Obsługa detekcji
    if len(faces1) + len(bodies1) > 0:
        if not detection:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out1 = cv2.VideoWriter(f"{videos_dir}/camera1_{current_time}.mp4", fourcc, 20.0, frame_size)
            print("Rozpoczęto nagrywanie!")
        timer_started = False
    elif detection:
        if not timer_started:
            detection_stopped_time = time.time()
            timer_started = True
        elif time.time() - detection_stopped_time > SECONDS_TO_RECORD_AFTER_DETECTION:
            detection = False
            timer_started = False
            out1.release()
            print("Zakończono nagrywanie!")

    # Nagrywanie, jeśli trwa detekcja
    if detection:
        out1.write(frame1)

    # Nagrywanie z kamery 2
    out2.write(frame2)

    # Rysowanie prostokątów na wykrytych obiektach
    for (x, y, w, h) in faces1:
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in bodies1:
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Łączenie obrazów w jeden
    combined_frame = cv2.hconcat([frame1, frame2])

    # Dopasowanie rozmiaru połączonego obrazu do rozdzielczości ekranu
    combined_frame = cv2.resize(combined_frame, (screen_width, screen_height))

    # Wyświetlanie połączonego obrazu
    cv2.imshow("Combined View", combined_frame)

    # Przerwanie programu
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Zakończono program.")
        break

# Zwolnienie zasobów
camera1.release()
camera2.release()
out2.release()
if detection:
    out1.release()
cv2.destroyAllWindows()
