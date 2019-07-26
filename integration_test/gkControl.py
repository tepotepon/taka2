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

Rango, Centro, MaxPos, MinPos = Homing(my_drive)