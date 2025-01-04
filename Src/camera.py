import cv2
import time
import datetime


# Video Capturing, the numeration is for how many devices we have
camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)


face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(camera1.get(3)), int(camera1.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


out2 = cv2.VideoWriter("video.mp4", fourcc, 20.0, frame_size)

while True:
    _, frame1 = camera1.read()
    _, frame2 = camera2.read()

    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    bodies1 = body_cascade.detectMultiScale(gray1, 1.3, 5)

    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)
    bodies2 = body_cascade.detectMultiScale(gray2, 1.3, 5)

    if len(faces1) + len(bodies1) > 0:
        if detection:
            timer_started = False
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%S")  
            out1 = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20.0, frame_size)
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

    if detection:
        out1.write(frame1)
    
    out2.write(frame2)

    for (x, y, width, height) in faces1:
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (255, 0, 0), 3)

    for (x, y, width, height) in faces2:
        cv2.rectangle(frame1, (x, y), (x + width, y + height), (0, 255, 0), 3)


    cv2.imshow("Camera 1", frame1)
    cv2.imshow("Camera 2", frame2)

    if cv2.waitKey(1) == ord('q'):
        break

out1.release()
out2.release()
camera1.release()
camera2.release()
cv2.destroyAllWindows()

