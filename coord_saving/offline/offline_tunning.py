import sys
from CentroidTracker import CentroidTracker
import cv2
import numpy as np
import time

#Some util. fuctions: 
def nothing(x):
    pass

#init video: 
ct = CentroidTracker()
cap = cv2.VideoCapture(sys.argv[1])

#init output document:
f = open("data/ball_tracking.txt","w+")

#Some flags and variables:
save_flag = False
pause = False
#actual_center = (0,0)

# Orange color (Ball) thresholds:
low_red = np.array([6, 110, 200])	
high_red = np.array([15, 250, 255])

#diferent kernels
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
kernel3 = np.ones((7,7),np.uint8)


#init of visualization window:
cv2.namedWindow('player_detection',cv2.WINDOW_NORMAL)

# create trackbars or testing color changes:
cv2.createTrackbar('low H','player_detection',44,255,nothing)
cv2.createTrackbar('high H','player_detection',65,255,nothing)
cv2.createTrackbar('low S','player_detection',0,255,nothing)
cv2.createTrackbar('high S','player_detection',255,255,nothing)
cv2.createTrackbar('low V','player_detection',0,255,nothing)
cv2.createTrackbar('high V','player_detection',255,255,nothing)
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'player_detection',0,1,nothing)

while cap.isOpened():

	#update image: 
	if (pause == False):
		_ , img1 = cap.read()
	else:
		img1 = last_image

	#resize image: 
	img1 = cv2.resize(img1, (640,480))

	#convertion to  HSV color space: 
	hsv_frame = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

	# get current positions of four trackbars:
	h1 = cv2.getTrackbarPos('low H','player_detection')
	h2 = cv2.getTrackbarPos('high H','player_detection')
	s1 = cv2.getTrackbarPos('low S','player_detection')
	s2 = cv2.getTrackbarPos('high S','player_detection')
	v1 = cv2.getTrackbarPos('low V','player_detection')
	v2 = cv2.getTrackbarPos('high V','player_detection')
	s = cv2.getTrackbarPos(switch,'player_detection')

	#new trackbars thresholds:
	lower = np.array([h1, s1, v1])
	upper = np.array([h2, s2, v2])

	#foostable field corner detection (green color based): 
	green = cv2.inRange(hsv_frame, (47, 52, 72), (68, 255,255))
	green1 = cv2.morphologyEx(green, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
	green_field = cv2.dilate(green1,np.ones((9,9),np.uint8),iterations = 3)


	if (s==0): 
		cv2.imshow("player_detection", hsv_frame)
	else:
		cv2.imshow("player_detection", green_field)


	k = cv2.waitKey(1)
	if k == 27:
		break
	elif k == 32:
		save_flag = not save_flag
	elif k == 112: 
		pause = not pause
		last_image = img1