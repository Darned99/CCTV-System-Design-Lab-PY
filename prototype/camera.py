import cv2
import time
import datetime
import os
from screeninfo import get_monitors

# Camera initialization - numbering depends on the number of connected devices
camera1 = cv2.VideoCapture("rtsp://admin:hikvision0987@192.168.1.67:554/Streaming/channels/2/")
camera2 = cv2.VideoCapture(1)

# Loading Haar classifiers for face and body detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

# Control variables for detection process
detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

# Getting screen resolution
monitor = get_monitors()[0]
screen_width, screen_height = monitor.width, monitor.height

# Video recording parameters
frame_width = int(camera1.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera1.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_size = (frame_width, frame_height)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

# Create "Videos" directory if it does not exist
videos_dir = "../Videos"
os.makedirs(videos_dir, exist_ok=True)

# Continuous recording from camera 2
out2 = cv2.VideoWriter(f"{videos_dir}/camera2_video.mp4", fourcc, 20.0, frame_size)

# Main program loop
while True:
    # Read frames from both cameras
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()

    if not ret1 or not ret2:
        print("Error: Failed to read from one of the cameras.")
        break

    # Adjust frame sizes and data types if different
    if frame1.shape[:2] != frame2.shape[:2]:
        frame2 = cv2.resize(frame2, (frame1.shape[1], frame1.shape[0]))

    # Convert frames to grayscale
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    # Detect faces and bodies in frames
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    bodies1 = body_cascade.detectMultiScale(gray1, 1.3, 5)

    # Detection handling
    if len(faces1) + len(bodies1) > 0:
        if not detection:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out1 = cv2.VideoWriter(f"{videos_dir}/camera1_{current_time}.mp4", fourcc, 20.0, frame_size)
            print("Recording started!")
        timer_started = False
    elif detection:
        if not timer_started:
            detection_stopped_time = time.time()
            timer_started = True
        elif time.time() - detection_stopped_time > SECONDS_TO_RECORD_AFTER_DETECTION:
            detection = False
            timer_started = False
            out1.release()
            print("Recording stopped!")

    # Record if detection is active
    if detection:
        out1.write(frame1)

    # Continuous recording from camera 2
    out2.write(frame2)

    # Draw rectangles around detected objects
    for (x, y, w, h) in faces1:
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (255, 0, 0), 2)
    for (x, y, w, h) in bodies1:
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Merge images into one
    combined_frame = cv2.hconcat([frame1, frame2])

    # Resize combined frame to screen resolution
    combined_frame = cv2.resize(combined_frame, (screen_width, screen_height))

    # Display merged image
    cv2.imshow("Combined View", combined_frame)

    # Program termination
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Program terminated.")
        break

# Release resources
camera1.release()
camera2.release()
out2.release()
if detection:
    out1.release()
cv2.destroyAllWindows()
