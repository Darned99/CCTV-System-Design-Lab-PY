import cv2
import time
import datetime


# Video Capturing, the numeration is for how many devices we have
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(1)

while True:
    _, frame = cap.read()

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()