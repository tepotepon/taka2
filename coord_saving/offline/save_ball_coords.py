import sys
from lib_cs.CentroidTracker import CentroidTracker
import cv2
import numpy as np
import time

def order_points(pts):
	# initialzie a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
 
	# the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum
	s = pts.sum(axis = 2)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]
 
	# now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 2)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]
 
	# return the ordered coordinates
	return rect

def four_point_transform(image, pts):
	# obtain a consistent order of the points and unpack them
	# individually
	rect = order_points(pts)
	(tl, tr, br, bl) = rect
 
	# compute the width of the new image, which will be the
	# maximum distance between bottom-right and bottom-left
	# x-coordiates or the top-right and top-left x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))
 
	# compute the height of the new image, which will be the
	# maximum distance between the top-right and bottom-right
	# y-coordinates or the top-left and bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))
 
	# now that we have the dimensions of the new image, construct
	# the set of destination points to obtain a "birds eye view",
	# (i.e. top-down view) of the image, again specifying points
	# in the top-left, top-right, bottom-right, and bottom-left
	# order
	dst = np.array([
		[0, 0],
		[maxWidth - 1, 0],
		[maxWidth - 1, maxHeight - 1],
		[0, maxHeight - 1]], dtype = "float32")
 
	# compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
 
	# return the warped image
	return warped

def nothing(x):
    pass

ct = CentroidTracker()
cap = cv2.VideoCapture(sys.argv[1])
f = open("coords_data/ball_tracking.txt","w+")
save_flag = False
pause = False
frame = 0

cv2.namedWindow('ball_detection',cv2.WINDOW_NORMAL)

# create trackbars for color change
cv2.createTrackbar('low H','ball_detection',6,255,nothing)
cv2.createTrackbar('high H','ball_detection',15,255,nothing)
cv2.createTrackbar('low S','ball_detection',110,255,nothing)
cv2.createTrackbar('high S','ball_detection',250,255,nothing)
cv2.createTrackbar('low V','ball_detection',200,255,nothing)
cv2.createTrackbar('high V','ball_detection',255,255,nothing)
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'ball_detection',0,1,nothing)

while cap.isOpened():

	frame += 1 
	if (pause == False):
		_ , img1 = cap.read()
	else:
		img1 = last_image

	hsv_frame = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

	# get current positions of four trackbars
	h1 = cv2.getTrackbarPos('low H','ball_detection')
	h2 = cv2.getTrackbarPos('high H','ball_detection')
	s1 = cv2.getTrackbarPos('low S','ball_detection')
	s2 = cv2.getTrackbarPos('high S','ball_detection')
	v1 = cv2.getTrackbarPos('low V','ball_detection')
	v2 = cv2.getTrackbarPos('high V','ball_detection')
	s = cv2.getTrackbarPos(switch,'ball_detection')

	lower = np.array([h1, s1, v1])
	upper = np.array([h2, s2, v2])
	
	green = cv2.inRange(hsv_frame, (47, 52, 72), (68, 255,255))
	green1 = cv2.morphologyEx(green, cv2.MORPH_CLOSE, np.ones((11,11),np.uint8))
	green_field = cv2.dilate(green1,np.ones((11,11),np.uint8),iterations = 3)
	
	contours_field, _ = cv2.findContours(green_field,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	epsilon = 0.1*cv2.arcLength(contours_field[0],False)
	corners = cv2.approxPolyDP(contours_field[0],epsilon,True)
	if (len(corners) == 4):
		warped_rgb = four_point_transform(img1, corners)
		warped_rgb = cv2.resize(warped_rgb, (1600,800))
		warped_hsv = cv2.cvtColor(warped_rgb, cv2.COLOR_BGR2HSV)

	orange_mask = cv2.inRange(warped_hsv, lower, upper)
	erosion = cv2.erode(orange_mask,np.ones((5,5),np.uint8),iterations = 2)
	dilation = cv2.dilate(erosion,np.ones((7,7),np.uint8),iterations = 2)
	contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	objects = ct.update(contours)
	# loop over the tracked objects
	for (objectID, centroid) in objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(warped_rgb, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
		cv2.circle(warped_rgb, (centroid[0], centroid[1]), 5, (0, 255, 0), -1)
		if (save_flag == True) and (pause == False):
			datos = str(frame) + ", " + text + ", " + str(centroid[0]) + ", " + str(centroid[1]) + ";\r\n"
			f.write(datos)

	if s == 0: cv2.imshow("ball_detection", warped_rgb)
	else: cv2.imshow("ball_detection", dilation)

	k = cv2.waitKey(1)
	if k == 27:
		break
	elif k == 32:
		save_flag = not save_flag
	elif k == 112: 
		pause = not pause
		last_image = img1

# Releasing the resource    
cap.release()
f.close()

cv2.destroyAllWindows()