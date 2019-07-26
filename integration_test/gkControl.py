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

# Create a GkPos object with an array size of 5
gkPos = gkp.GkPos(5)

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

time.sleep(10)
while(True):
	# Get the actual pos
	p = (0,0) # replace with call to ball detector

	# Pass it to GkPos 
	gkPos.push(p)

	# Get an updated estimate for the best goalkeeper position
	(x,y) = gkPos.get_estimate()

	# Convert it to Motor Control coordinates
	y_ref = (MaxPos-abs(0.05*MaxPos)-(MinPos+abs(0.05*MinPos)))/gkPos.get_const()*y + (MinPos+abs(0.05*MinPos))

	# Constrain the reference once again
	if y_ref > MaxPos:
		y_ref = MaxPos
	elif y_ref < MinPos:
		y_ref = MinPos

	# Send the motor to the required position
	A0.controller.pos_setpoint = y_ref
	k = cv2.waitKey(1)
	if k == 27:
		break