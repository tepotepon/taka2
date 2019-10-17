import cv2
import numpy as np
from cv2 import aruco
import sys

aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
parameters = aruco.DetectorParameters_create()

if(len(sys.argv) != 2):
    print("Numero incorrecto de parametros.\r\n")
    exit()

img = cv2.imread(sys.argv[1])

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
aruco.drawDetectedMarkers(img, corners, ids)
for mark in corners:
    cv2.drawMarker(img, (int(mark[0][1][0]), int(mark[0][1][1])), [0,255,0], 0, 20, 1, 8)
cv2.imshow('Aruco', img)
cv2.waitKey(0)

cv2.destroyAllWindows()