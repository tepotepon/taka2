import cv2
import numpy as np
from pypylon import pylon

# conecting to the first available camera
camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
camera.Open()
camera.GainAuto.SetValue("Once")
# Grabing Continusely (video) with minimal delay
camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
converter = pylon.ImageFormatConverter()

# converting to opencv bgr format
converter.OutputPixelFormat = pylon.PixelType_BGR8packed
converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

image = converter.Convert(grabResult)
img1 = image.GetArray()
counter = 0

out = cv2.VideoWriter('out.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 27, (800,600))


while camera.IsGrabbing():
	grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

	if grabResult.GrabSucceeded():
		image = converter.Convert(grabResult)
		img1 = image.GetArray()
		out.write(img1)
	
	cv2.imshow("img", img1)
	k = cv2.waitKey(1)
	if k == 27:
		break
	elif k == 32:
		counter = counter + 1
		print("photo_" + str(counter) + ".jpg")
		cv2.imwrite("photo_" + str(counter) + ".jpg", img1)

camera.StopGrabbing()
out.release()
cv2.destroyAllWindows()
