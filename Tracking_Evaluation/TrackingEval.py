import cv2
import numpy as np

cap = cv2.VideoCapture("data/outpy.avi")

# Orange color thresholds 
low_red = np.array([6, 150, 200])	
high_red = np.array([15, 250, 255])	
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
actual_center = (0,0)
last_center = (0,0)

while cap.isOpened():
	ret, frame = cap.read()
	img = frame[60:540,170:680]

	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	orange_mask = cv2.inRange(hsv_frame, low_red, high_red)
	erosion = cv2.erode(orange_mask,kernel1,iterations = 1)
	dilation = cv2.dilate(erosion,kernel2,iterations = 2)
	last = cv2.bitwise_and(img, img, mask=dilation)

	contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	if(len(contours) == 1): # ¿Is this if sentence ok?
		M = cv2.moments(contours[0])
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		actual_center = (cx,cy)
		print(actual_center)
		x,y,w,h = cv2.boundingRect(contours)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.imshow("Result", img)
	k = cv2.waitKey(1)
	if k == 27:
		break

# Releasing the resource
cap.release()
cv2.destroyAllWindows()
