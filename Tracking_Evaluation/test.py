import cv2
import numpy as np

cap = cv2.VideoCapture("data/test.avi")

# Orange color thresholds 
low_red = np.array([6, 150, 200])	
high_red = np.array([15, 250, 255])	
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)

ROI_X = 140
ROI_Y = 70
ROI_WIDTH = 520
ROI_HEIGHT = 470

pause = True

while (cap.isOpened()):
	ret, frame = cap.read()
	if (ret == False):
		break

	img = frame[ROI_Y:ROI_Y+ROI_HEIGHT,ROI_X:ROI_X+ROI_WIDTH]
	hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	orange_mask = cv2.inRange(hsv_frame, low_red, high_red)
	erosion = cv2.erode(orange_mask,kernel1,iterations = 1)
	dilation = cv2.dilate(erosion,kernel2,iterations = 2)
	last = cv2.bitwise_and(img, img, mask=dilation)
	cv2.imshow("Result", dilation)

	k = cv2.waitKey(25)
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
