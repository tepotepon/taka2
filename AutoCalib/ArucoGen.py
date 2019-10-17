import cv2
import numpy as np
from cv2 import aruco

aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

for i in range(1,9):
	cv2.imwrite(str(i)+'.jpg', aruco.drawMarker(aruco_dict,i, 400))