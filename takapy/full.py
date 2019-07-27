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

import LibTaca.GkPos as gkp
import cv2

import numpy as np
from pypylon import pylon

cy = 0

# Create a GkPos object with an array size of 5
gkPos = gkp.GkPos(5)

f = open("data.txt","w+")

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
out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 27, (510,480))

# Orange color thresholds 
low_red = np.array([6, 150, 200])	
high_red = np.array([15, 250, 255])	
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)

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
		orange_mask = cv2.inRange(hsv_frame, low_red, high_red)
		orange = cv2.bitwise_and(img, img, mask=orange_mask)

	
	erosion = cv2.erode(orange_mask,kernel1,iterations = 1)
	dilation = cv2.dilate(erosion,kernel2,iterations = 2)
	last = cv2.bitwise_and(img, img, mask=dilation)

	contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	if(len(contours) == 1):
		cv2.drawContours(img, contours[0], -1, (0, 255, 0), 3)
		M = cv2.moments(contours[0])
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		# Pass it to GkPos 
		gkPos.push((cx,cy))

	# Get an updated estimate for the best goalkeeper position
	(x,y) = gkPos.get_estimate()
	#y = cy

	img	=	cv2.drawMarker(img, (cx,cy), [0,255,0], 0, 20, 1, 8)
	out.write(img)

	# Convert it to Motor Control coordinates
	y_ref = (MaxPos-MinPos)/gkPos.get_const()*y + MinPos

	# Constrain the reference once again
	if y_ref > MaxPos:
		y_ref = MaxPos
	elif y_ref < MinPos:
		y_ref = MinPos
	t_log = time.time_ns()
	# Log relevant vars
	pos = A0.controller.pos_setpoint
	I = A0.motor.current_control.Iq_measured
	datos = str(t_log) + ", " + str(I) + ", " + str(pos) + ", " + str(y) + ", " + str(y_ref) + str(cx) + ", " + str(cy) + ";\r\n"
	f.write(datos)

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

cv2.destroyAllWindows()