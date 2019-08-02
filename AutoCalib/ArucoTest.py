import cv2
import numpy as np
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()

    if (ret == False):
        break

    blur = cv2.GaussianBlur(img,(7,7),0)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame = aruco.drawDetectedMarkers(img, corners, ids)
    cv2.imshow('Aruco', frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
    
# Releasing the resource    
camera.StopGrabbing()

cv2.destroyAllWindows()