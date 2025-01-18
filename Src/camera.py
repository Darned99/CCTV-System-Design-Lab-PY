import cv2
import time
import datetime
import os
from screeninfo import get_monitors

# Inicjalizacja kamer - numeracja zależy od liczby podłączonych urządzeń
camera1 = cv2.VideoCapture(0)
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
frame_size = (int(camera1.get(3)), int(camera1.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Utworzenie katalogu Videos, jeśli nie istnieje
videos_dir = "../Videos"
os.makedirs(videos_dir, exist_ok=True)

# Nagrywanie ciągłe z kamery 2
out2 = cv2.VideoWriter(f"{videos_dir}/camera2_video.mp4", fourcc, 20.0, frame_size)

# Główna pętla programu
while True:
    # Odczyt klatek z obu kamer
    _, frame1 = camera1.read()
    _, frame2 = camera2.read()

    # Konwersja klatek na odcienie szarości
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Detekcja twarzy i ciał w klatkach
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    bodies1 = body_cascade.detectMultiScale(gray1, 1.3, 5)
    faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)
    bodies2 = body_cascade.detectMultiScale(gray2, 1.3, 5)

    # Jeśli wykryto obiekt w kamerze 1
    if len(faces1) + len(bodies1) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%S")  
            out1 = cv2.VideoWriter(f"{videos_dir}/{current_time}.mp4", fourcc, 20.0, frame_size)
        print("Started recording!")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out1.release()
                print('Stop Recording!')
        else:
            timer_started = True
            detection_stopped_time = time.time()

    # Jeśli trwa detekcja, zapisz klatkę do pliku
    if detection:
        out1.write(frame1)
    
    # Zapis klatek z kamery 2 do osobnego pliku
    out2.write(frame2)

    # Rysowanie prostokątów wokół wykrytych obiektów
    for (x, y, width, height) in faces1:
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (255, 0, 0), 3)
    for (x, y, width, height) in faces2:
        cv2.rectangle(frame2, (x, y), (x + width, y + height), (0, 255, 0), 3)

    # Połączenie obrazów z obu kamer w jeden obraz
    combined_frame = cv2.hconcat([frame1, frame2])

    # Dopasowanie rozmiaru połączonego obrazu do rozdzielczości ekranu
    combined_frame = cv2.resize(combined_frame, (screen_width, screen_height))

    # Wyświetlanie obrazu z obu kamer w jednym oknie
    cv2.imshow("Combined View", combined_frame)

    # Sprawdzanie przycisku 'q' - możliwość zakończenia w każdej chwili
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Zakończono program.")
        break

# Zwolnienie zasobów i zamknięcie plików wideo
out2.release()
camera1.release()
camera2.release()
if detection:  # Zwolnienie zasobów nagrywania, jeśli trwała detekcja
    out1.release()
cv2.destroyAllWindows()
