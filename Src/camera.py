import cv2
import time
import datetime

# Inicjalizacja kamer - numeracja zależy od liczby podłączonych urządzeń
camera1 = cv2.VideoCapture(0)  # Pierwsza kamera
camera2 = cv2.VideoCapture(1)  # Druga kamera

# Ładowanie klasyfikatorów Haar do wykrywania twarzy i ciał
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")  # Detekcja twarzy
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")  # Detekcja ciał

# Zmienne kontrolne dla procesu detekcji
detection = False  # Flaga informująca, czy wykryto obiekt
detection_stopped_time = None  # Czas zatrzymania detekcji
timer_started = False  # Flaga dla opóźnionego zatrzymania
SECONDS_TO_RECORD_AFTER_DETECTION = 5  # Czas nagrywania po wykryciu

# Parametry nagrywania wideo
frame_size = (int(camera1.get(3)), int(camera1.get(4)))  # Rozdzielczość klatek
fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Format zapisu wideo

# Nagrywanie ciągłe z kamery 2
out2 = cv2.VideoWriter("video.mp4", fourcc, 20.0, frame_size)

# Główna pętla programu
while True:
    # Odczyt klatek z obu kamer
    _, frame1 = camera1.read()  # Klatka z kamery 1
    _, frame2 = camera2.read()  # Klatka z kamery 2

    # Konwersja klatek na odcienie szarości
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Kamera 1
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)  # Kamera 2

    # Detekcja twarzy i ciał w klatkach
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)  # Twarze, kamera 1
    bodies1 = body_cascade.detectMultiScale(gray1, 1.3, 5)  # Ciała, kamera 1
    
    faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)  # Twarze, kamera 2
    bodies2 = body_cascade.detectMultiScale(gray2, 1.3, 5)  # Ciała, kamera 2

    # Jeśli wykryto obiekt w kamerze 1
    if len(faces1) + len(bodies1) > 0:
        if detection:  # Jeśli już trwa nagrywanie
            timer_started = False  # Reset timera
        else:
            detection = True  # Rozpoczęcie detekcji
            # Utworzenie nowego pliku wideo dla kamery 1
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%S")  
            out1 = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)
        print("Started recording!")
    
    # Jeśli nic nie wykryto, ale wcześniej była detekcja
    elif detection:
        if timer_started:  # Jeśli timer już został uruchomiony
            # Sprawdzenie, czy minął czas na zakończenie nagrywania
            if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False  # Zatrzymanie detekcji
                timer_started = False
                out1.release()  # Zamknięcie pliku wideo
                print('Stop Recording!')
        else:
            timer_started = True  # Uruchomienie timera
            detection_stopped_time = time.time()

    # Jeśli trwa detekcja, zapisz klatkę do pliku
    if detection:
        out1.write(frame1)
    
    # Zapis klatek z kamery 2 do osobnego pliku
    out2.write(frame2)

    # Rysowanie prostokątów wokół wykrytych obiektów w kamerze 1
    for (x, y, width, height) in faces1:
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (255, 0, 0), 3)  # Twarze
        
    for (x, y, width, height) in bodies1:
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (0, 255, 0), 3)  # Ciała, kamera 1

    # Rysowanie prostokątów wokół wykrytych obiektów w kamerze 2
    for (x, y, width, height) in faces2:
        cv2.rectangle(frame2, (x, y), (x + width, y + height), (0, 255, 0), 3)  # Twarze

    for (x, y, width, height) in bodies2:
        cv2.rectangle(frame2, (x, y), (x + width, y + height), (0, 255, 0), 3)  # Ciała, kamera 2

    # Wyświetlanie obrazu z obu kamer
    cv2.imshow("Camera 1", frame1)  # Obraz z kamery 1
    cv2.imshow("Camera 2", frame2)  # Obraz z kamery 2

    # Przerwanie pętli po naciśnięciu klawisza 'q'
    if cv2.waitKey(1) == ord('q'):
        break

# Zwolnienie zasobów i zamknięcie plików wideo
out1.release()
out2.release()
camera1.release()
camera2.release()
cv2.destroyAllWindows()
