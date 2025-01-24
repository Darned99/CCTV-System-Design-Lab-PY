import cv2
from cctv_project import CameraMonitor

def main():
    #0,  # Kamera lokalna
    #1,  # Kamera lokalna
    # 'rtsp://admin:hikvision0987@192.168.1.67:554/Streaming/Channels/2',  # Strumień RTSP
    # 'rtsp://admin:hikvision0987@192.168.1.68:554/Streaming/Channels/2',  # Strumień RTSP

    # Pobieranie liczby kamer od użytkownika
    num_cameras = int(input("Podaj liczbę kamer do zainicjalizowania: "))

    camera_sources = []
    for i in range(num_cameras):
        camera_id = input(f"Podaj identyfikator kamery {i+1} (np. 0, 1 lub URL strumienia RTSP): ")
        if camera_id.isdigit():
            camera_sources.append(int(camera_id))
        else:
            camera_sources.append(camera_id)

    camera_monitors = [CameraMonitor(source) for source in camera_sources]

    try:
        print("Rozpoczynam monitorowanie kamer. Wciśnij '1' dla wykrywania ruchu, '2' dla ciągłego nagrywania, 'q' aby zakończyć.")
        while True:
            for monitor in camera_monitors:
                if not monitor.process_frame():
                    print(f"Nie udało się przetworzyć klatki dla kamery {monitor.camera_id}")

            key = cv2.waitKey(1) & 0xFF
            if key == ord('1'):
                print("Zmieniono tryb na wykrywanie ruchu.")
                for monitor in camera_monitors:
                    monitor.set_mode(1)
            elif key == ord('2'):
                print("Zmieniono tryb na ciągłe nagrywanie.")
                for monitor in camera_monitors:
                    monitor.set_mode(2)
            elif key == ord('q'):
                break

    finally:
        print("Zatrzymuję monitorowanie i zwalniam zasoby...")
        for monitor in camera_monitors:
            monitor.release_resources()

if __name__ == "__main__":
    main()
