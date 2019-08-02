import cv2
import numpy as np
import sys

if (int(sys.argv[1]) == 1):
	cap = cv2.VideoCapture("data/outpy.avi")
	ROI_X = 0
	ROI_Y = 0
	ROI_WIDTH = 510
	ROI_HEIGHT = 480
	t = 80
elif (int(sys.argv[1]) == 2):
	cap = cv2.VideoCapture("data/test.avi")
	ROI_X = 140
	ROI_Y = 70
	ROI_WIDTH = 520
	ROI_HEIGHT = 470
	t = 50
else:
	print("Error: Solo debe haber un argumento y con valor 1 o 2")

# Orange color thresholds 
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)

pause = True
frames = 0
out = cv2.VideoWriter('data/GoalKeeperID.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 60, (510,480))

while (cap.isOpened()):
	ret, frame = cap.read()
	if (ret == False):
		break
	frames = frames + 1
	# From the identified coordinates from the QR codes, select the rightmost half of the ROI.
	img = frame[ROI_Y:ROI_Y+ROI_HEIGHT,ROI_X+int(ROI_WIDTH/2):ROI_X+ROI_WIDTH]
	# As we're interested on identifying a black object, color channels are unuseful information.
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# The threshold value is quite arbitrary and tuned empirically.
	ret, mask = cv2.threshold(gray, t, 255, cv2.THRESH_BINARY_INV)
	# Perform opening operation to filter out noise and isolate the goalkeeper
	erosion = cv2.erode(mask,kernel1,iterations = 2)
	dilation = cv2.dilate(erosion,kernel2,iterations = 3)
	# Find the goalkeeper countour and bounding box. This will be on ROI coordinates.
	contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	bbox = cv2.boundingRect(contours[0])
	(x, y, w, h) = [int(v) for v in bbox]
	# Go back to original image coordinates and draw over the BGR version
	x = x + ROI_X+int(ROI_WIDTH/2)
	y = y + ROI_Y
	cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
	# 
	cv2.imshow("Result", frame)
	out.write(frame)


	k = cv2.waitKey(1)
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