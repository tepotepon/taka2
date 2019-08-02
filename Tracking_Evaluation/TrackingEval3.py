# TLD works quite fine, but it's slower than just plain detection

import cv2
import numpy as np
import sys

cap = cv2.VideoCapture("data/test.avi")

# Orange color thresholds 
low_red = np.array([6, 150, 200])	
high_red = np.array([15, 250, 255])	
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
actual_center = (0,0)
last_center = (0,0)

ROI_X = 140
ROI_Y = 70
ROI_WIDTH = 520
ROI_HEIGHT = 470
frames = 0
pause = False # For debugging, useless otherwise.
speed = 1

if(len(sys.argv)==2):
	if (int(sys.argv[1]) == 0):
		tracker = cv2.TrackerCSRT_create()
		print("CSRT\r\n")
	elif (int(sys.argv[1]) == 1):
		tracker = cv2.TrackerKCF_create()
		print("KCF\r\n")
	elif (int(sys.argv[1]) == 2):
		tracker = cv2.TrackerBoosting_create()
		print("Boosting\r\n")
	elif (int(sys.argv[1]) == 3):
		tracker = cv2.TrackerMIL_create()
		print("MIL\r\n")
	elif (int(sys.argv[1]) == 4):
		tracker = cv2.TrackerTLD_create()
		print("TLD\r\n")
	elif (int(sys.argv[1]) == 5):
		tracker = cv2.TrackerMedianFlow_create()
		print("Median Flow\r\n")
	elif (int(sys.argv[1]) == 6):
		tracker = cv2.TrackerMOSSE_create()
		print("MOSSE\r\n")
	else:
		print("Wrong parameter value. Try numbers from 0-6")
else:
	print("Wrong number of arguments.\r\n")
	exit()

while (cap.isOpened()):
	ret, frame = cap.read()
	if (ret == False):
		break

	frames = frames+1
	img = frame[ROI_Y:ROI_Y+ROI_HEIGHT,ROI_X:ROI_X+ROI_WIDTH]
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	orange_mask = cv2.inRange(hsv_frame, low_red, high_red)

	if frames == 87: # look for initial pos and bounding box
		hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		orange_mask = cv2.inRange(hsv_frame, low_red, high_red)
		erosion = cv2.erode(orange_mask,kernel1,iterations = 1)
		dilation = cv2.dilate(erosion,kernel2,iterations = 2)
		last = cv2.bitwise_and(img, img, mask=dilation)
		contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		bbox = cv2.boundingRect(contours[0])
		(x, y, w, h) = [int(v) for v in bbox]
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		tracker.init(orange_mask,bbox)
		pause = True
		speed = 25

	elif frames > 87:
		(ok, box) = tracker.update(orange_mask)
		if ok:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(img, (x, y), (x + w, y + h),(0, 255, 0), 2)
		else:
			print("Faiamos\r\n")

	cv2.imshow("Result", img)

	k = cv2.waitKey(speed)
	if k == 27:
		break
	elif k == 32:
		pause = True

	while pause == True:
		k = cv2.waitKey(1)
		if k == 32:
			pause = False
		elif k == 83:
			break
# Releasing the resource
cap.release()
cv2.destroyAllWindows()
