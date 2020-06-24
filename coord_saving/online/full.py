import odrive
from odrive.enums import *
from odrive.utils import start_liveplotter
from odrive.utils import dump_errors
import time
import math
import usb.core
import usb.util

from LibTaca.TacaTools import Homing
from LibTaca.TacaTools import WriteExcel
from LibTaca.utilsmod import start_liveplotter2 as lp2
from LibTaca.CentroidTracker import CentroidTracker

import LibTaca.GkPos as gkp
import cv2

import numpy as np
from pypylon import pylon


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

cy = 0

# Create a GkPos object with an array size of 5
gkPos = gkp.GkPos(5)

f = open("output/data.txt","w+")
ball_f = open("output/ball_coords.txt","w+")

# Camera stuff
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.GainAuto.SetValue("Once")
# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

#Define codec to save video
out = cv2.VideoWriter('output/outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 27, (510,480))

# Orange color thresholds 
lower_ball = np.array([6, 110, 200])	
upper_ball = np.array([15, 250, 255])

# team1 color thresholds 
lower_team1 = np.array([20, 52, 149])	
upper_team1 = np.array([30, 255, 255])	

# Orange color thresholds 
lower_team2 = np.array([0, 0, 0])	
upper_team2 = np.array([10, 250, 255])

# Motos stuff

print("finding an odrive...")
my_drive = odrive.find_any()
A0 = my_drive.axis0
print("Odrive found.")

if((A0.motor.is_calibrated)==False):
    # Calibrate motor and wait for it to finish
    print("starting calibration...")
    my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    
while my_drive.axis0.current_state != AXIS_STATE_IDLE:
    time.sleep(0.1)

my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

my_drive.axis0.motor.config.current_lim = 25 # Amperes de corriente limite

print ("Homing...\n")
Rango, Centro, MaxPos, MinPos = Homing(my_drive)

time.sleep(1)
while camera.IsGrabbing():
	# Get the actual pos
	grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

	if grabResult.GrabSucceeded():
		image = converter.Convert(grabResult)
		img1 = image.GetArray()
		img = img1[60:540,170:680]
		hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		ball_mask = cv2.inRange(hsv_frame, lower_ball, upper_ball)
		team1_mask = cv2.inRange(hsv_frame, lower_team1, upper_team1)
		team2_mask = cv2.inRange(hsv_frame, lower_team12 upper_team2)
	
	ball_mask = cv2.erode(ball_mask,np.ones((5,5),np.uint8),iterations = 1)
	ball_mask = cv2.dilate(ball_mask,np.ones((7,7),iterations = 2))

	contours , _ = cv2.findContours(ball_mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	for i in range(3):
		if (i==0):
			mask = cv2.inRange(warped_hsv, lower_ball, upper_ball)
		if (i==1):
			mask = cv2.inRange(warped_hsv, lower_team1, upper_team1)
		if (i==2):
			mask = cv2.inRange(warped_hsv, lower_team2, upper_team2)

		mask = cv2.erode(mask,np.ones((5,5),np.uint8),iterations = 2)
		mask = cv2.dilate(mask,np.ones((7,7),np.uint8),iterations = 2)
		cont , _ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

		if (i==0):
			ball_objects = ball_ct.update(cont)
			if(len(cont) == 1):
				M = cv2.moments(contours[0])
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				# Pass it to GkPos 
				gkPos.push((cx,cy))
		if (i==1):
			team1_objects = team1_ct.update(cont)
		if (i==2):
			team2_objects = team2_ct.update(cont)

	# Get an updated estimate for the best goalkeeper position
	(x,y) = gkPos.get_estimate()
	#y = cy

	# Convert it to Motor Control coordinates
	y_ref = (MaxPos-MinPos)/gkPos.get_const()*y + MinPos

	# Constrain the reference once again
	if y_ref > MaxPos:
		y_ref = MaxPos
	elif y_ref < MinPos:
		y_ref = MinPos

	for (objectID, centroid) in team1_objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(warped_rgb, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
		cv2.circle(warped_rgb, (centroid[0], centroid[1]), 5, (0, 255, 0), -1)
		if (save_flag == True) and (pause == False):
			datos = str(frame) + ", " + text + ", " + str(centroid[0]) + ", " + str(centroid[1]) + ";\r\n"
			fteam1.write(datos)
	
	
	for (objectID, centroid) in ball_objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		#print((objectID, centroid))
		cv2.putText(warped_rgb, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
		cv2.circle(warped_rgb, (centroid[0], centroid[1]), 5, (0, 255, 0), -1)
		if (save_flag == True) and (pause == False):
			datos = str(frame) + ", " + text + ", " + str(centroid[0]) + ", " + str(centroid[1]) + ";\r\n"
			fb.write(datos)

	for (objectID, centroid) in team2_objects.items():
		# draw both the ID of the object and the centroid of the
		# object on the output frame
		text = "ID {}".format(objectID)
		cv2.putText(warped_rgb, text, (centroid[0] - 10, centroid[1] - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
		cv2.circle(warped_rgb, (centroid[0], centroid[1]), 5, (0, 255, 0), -1)
		if (save_flag == True) and (pause == False):
			datos = str(frame) + ", " + text + ", " + str(centroid[0]) + ", " + str(centroid[1]) + ";\r\n"
			fteam2.write(datos)
			
	# Send the motor to the required position
	A0.controller.pos_setpoint = y_ref

	cv2.imshow("results", img)
	print(datos)
	k = cv2.waitKey(1)
	if k == 27:
		break

camera.StopGrabbing()
out.release()
f.close()
ball_f.close()

cv2.destroyAllWindows()
