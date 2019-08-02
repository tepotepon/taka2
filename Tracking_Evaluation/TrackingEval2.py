import cv2
import numpy as np

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

# Lost the target as soon as it approached the puppet.
# Maybe because the number of frames is pretty low and
# the ball quite fast. Test it with the camera online.
#tracker = cv2.TrackerCSRT_create()

# Didn't even resisted one frame.
#tracker = cv2.TrackerKCF_create()

# Lost the target as soon as it approached the puppet.
# Maybe because the number of frames is pretty low and
# the ball quite fast. Test it with the camera online.
#tracker = cv2.TrackerBoosting_create()

# Super slow, lost the target too. Again, might be
# because of the low number of frames.
#tracker = cv2.TrackerMIL_create()

# Lots of false positives, pretty slow too.
#tracker = cv2.TrackerTLD_create()

# Lost the target as soon as it approached the puppet.
# Maybe because the number of frames is pretty low and
# the ball quite fast. Test it with the camera online.
#tracker = cv2.TrackerMedianFlow_create()

# Didn't even resisted one frame.
tracker = cv2.TrackerMOSSE_create()

while (cap.isOpened()):
	ret, frame = cap.read()
	if (ret == False):
		break

	frames = frames+1
	img = frame[ROI_Y:ROI_Y+ROI_HEIGHT,ROI_X:ROI_X+ROI_WIDTH]

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
		tracker.init(img,bbox)
		pause = True
		speed = 25

	elif frames > 87:
		(ok, box) = tracker.update(img)
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
