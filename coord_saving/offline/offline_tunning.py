import sys
from lib_cs.CentroidTracker import CentroidTracker
import cv2
import numpy as np
import time

#Some util. fuctions: 
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

#init video: 
ct = CentroidTracker()
cap = cv2.VideoCapture(sys.argv[1])

#Some flags and variables:
save_flag = False
pause = False

#init of visualization window:
cv2.namedWindow('ball_detection',cv2.WINDOW_NORMAL)
cv2.namedWindow('Team1_detection',cv2.WINDOW_NORMAL)
cv2.namedWindow('team2_detection',cv2.WINDOW_NORMAL)

# create trackbars for testing ball colors:
cv2.createTrackbar('low H','ball_detection',6,255,nothing)
cv2.createTrackbar('high H','ball_detection',15,255,nothing)
cv2.createTrackbar('low S','ball_detection',110,255,nothing)
cv2.createTrackbar('high S','ball_detection',250,255,nothing)
cv2.createTrackbar('low V','ball_detection',200,255,nothing)
cv2.createTrackbar('high V','ball_detection',255,255,nothing)
switch_ball = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch_ball, 'ball_detection',0,1,nothing)

# create trackbars for testing team1 colors:
cv2.createTrackbar('low H','Team1_detection',20,255,nothing)
cv2.createTrackbar('high H','Team1_detection',30,255,nothing)
cv2.createTrackbar('low S','Team1_detection',52,255,nothing)
cv2.createTrackbar('high S','Team1_detection',255,255,nothing)
cv2.createTrackbar('low V','Team1_detection',149,255,nothing)
cv2.createTrackbar('high V','Team1_detection',255,255,nothing)
switch_team1 = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch_team1, 'Team1_detection',0,1,nothing)

# create trackbars for testing team2 colors:
cv2.createTrackbar('low H','team2_detection',0,255,nothing)
cv2.createTrackbar('high H','team2_detection',10,255,nothing)
cv2.createTrackbar('low S','team2_detection',0,255,nothing)
cv2.createTrackbar('high S','team2_detection',255,255,nothing)
cv2.createTrackbar('low V','team2_detection',0,255,nothing)
cv2.createTrackbar('high V','team2_detection',255,255,nothing)
switch_team2 = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch_team2, 'team2_detection',0,1,nothing)

while cap.isOpened():

	#update image: 
	if (pause == False):
		_ , img1 = cap.read()
	else:
		img1 = last_image

	#convertion to  HSV color space: 
	hsv_frame = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)

	# get current positions of four trackbars:
	ball_h1 = cv2.getTrackbarPos('low H','ball_detection')
	ball_h2 = cv2.getTrackbarPos('high H','ball_detection')
	ball_s1 = cv2.getTrackbarPos('low S','ball_detection')
	ball_s2 = cv2.getTrackbarPos('high S','ball_detection')
	ball_v1 = cv2.getTrackbarPos('low V','ball_detection')
	ball_v2 = cv2.getTrackbarPos('high V','ball_detection')
	ball_s = cv2.getTrackbarPos(switch_ball,'ball_detection')

	# get current positions of four trackbars:
	team1_h1 = cv2.getTrackbarPos('low H','Team1_detection')
	team1_h2 = cv2.getTrackbarPos('high H','Team1_detection')
	team1_s1 = cv2.getTrackbarPos('low S','Team1_detection')
	team1_s2 = cv2.getTrackbarPos('high S','Team1_detection')
	team1_v1 = cv2.getTrackbarPos('low V','Team1_detection')
	team1_v2 = cv2.getTrackbarPos('high V','Team1_detection')
	team1_s = cv2.getTrackbarPos(switch_team1,'Team1_detection')

	# get current positions of four trackbars:
	team2_h1 = cv2.getTrackbarPos('low H','team2_detection')
	team2_h2 = cv2.getTrackbarPos('high H','team2_detection')
	team2_s1 = cv2.getTrackbarPos('low S','team2_detection')
	team2_s2 = cv2.getTrackbarPos('high S','team2_detection')
	team2_v1 = cv2.getTrackbarPos('low V','team2_detection')
	team2_v2 = cv2.getTrackbarPos('high V','team2_detection')
	team2_s = cv2.getTrackbarPos(switch_team2,'team2_detection')

	#new trackbars thresholds:
	lower_ball = np.array([ball_h1, ball_s1, ball_v1])
	upper_ball = np.array([ball_h2, ball_s2, ball_v2])

	#new trackbars thresholds:
	lower_team1 = np.array([team1_h1, team1_s1, team1_v1])
	upper_team1 = np.array([team1_h2, team1_s2, team1_v2])

	#new trackbars thresholds:
	lower_team2 = np.array([team2_h1, team2_s1, team2_v1])
	upper_team2 = np.array([team2_h2, team2_s2, team2_v2])

	#foostable field corner detection (green color based): 
	green = cv2.inRange(hsv_frame, (47, 52, 72), (68, 255,255))
	green1 = cv2.morphologyEx(green, cv2.MORPH_CLOSE, np.ones((9,9),np.uint8))
	green_field = cv2.dilate(green1,np.ones((9,9),np.uint8),iterations = 3)

	contours_field, _ = cv2.findContours(green_field,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	epsilon = 0.1*cv2.arcLength(contours_field[0],False)
	corners = cv2.approxPolyDP(contours_field[0],epsilon,True)

	if (len(corners) == 4):
		warped_rgb = four_point_transform(img1, corners)
		warped_rgb = cv2.resize(warped_rgb, (1600,800))
		warped_hsv = cv2.cvtColor(warped_rgb, cv2.COLOR_BGR2HSV)

	#foostable field corner detection (green color based):
	team1_mask = cv2.inRange(warped_hsv, lower_team1, upper_team1)
	team1_mask = cv2.erode(team1_mask,np.ones((5,5),np.uint8),iterations = 2)
	team1_mask = cv2.dilate(team1_mask,np.ones((7,7),np.uint8),iterations = 2)
	team1_contours , _ = cv2.findContours(team1_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	ball_mask = cv2.inRange(warped_hsv, lower_ball, upper_ball)
	ball_mask = cv2.erode(ball_mask,np.ones((5,5),np.uint8),iterations = 2)
	ball_mask = cv2.dilate(ball_mask,np.ones((7,7),np.uint8),iterations = 2)
	ball_contours , _ = cv2.findContours(ball_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

	team2_mask = cv2.inRange(warped_hsv, lower_team2, upper_team2)
	team2_mask = cv2.erode(team2_mask,np.ones((5,5),np.uint8),iterations = 2)
	team2_mask = cv2.dilate(team2_mask,np.ones((7,7),np.uint8),iterations = 2)
	team2_contours , _ = cv2.findContours(team2_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


	if (team1_s==0): 
		cv2.imshow("Team1_detection", warped_rgb)
	else:
		cv2.imshow("Team1_detection", team1_mask)

	if (ball_s==0): 
		cv2.imshow("ball_detection", warped_rgb)
	else:
		cv2.imshow("ball_detection", ball_mask)

	if (team2_s==0): 
		cv2.imshow("team2_detection", warped_rgb)
	else:
		cv2.imshow("team2_detection", team2_mask)


	k = cv2.waitKey(1)
	if k == 27:
		break
	elif k == 32:
		save_flag = not save_flag
	elif k == 112: 
		pause = not pause
		last_image = img1