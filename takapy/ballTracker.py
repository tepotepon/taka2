
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

# Orange color thresholds 
low_red = np.array([6, 150, 200])	
high_red = np.array([15, 250, 255])	
kernel1 = np.ones((3,3),np.uint8)
kernel2 = np.ones((5,5),np.uint8)
actual_center = (0,0)
last_center = (0,0)


while camera.IsGrabbing():
	grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

	if grabResult.GrabSucceeded():
		image = converter.Convert(grabResult)
		img1 = image.GetArray()
		img = img1[60:540,170:680]
		hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		orange_mask = cv2.inRange(hsv_frame, low_red, high_red)
		orange = cv2.bitwise_and(img, img, mask=orange_mask)

		#cv2.imshow("orange_mask", orange_mask)
	print(int(img.get(3)),int(img.get(4)))
	erosion = cv2.erode(orange_mask,kernel1,iterations = 1)
	dilation = cv2.dilate(erosion,kernel2,iterations = 2)
	last = cv2.bitwise_and(img, img, mask=dilation)

	contours , _ = cv2.findContours(dilation,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	
	if(len(contours) == 1):
		cv2.drawContours(img, contours[0], -1, (0, 255, 0), 3)
		M = cv2.moments(contours[0])
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		actual_center = (cx,cy)
		#print(actual_center)

	out.write(img)
	cv2.imshow("img", img)




	#cv2.imshow("orange_mask", orange_mask)
	k = cv2.waitKey(1)
	if k == 27:
		break

# Releasing the resource    
camera.StopGrabbing()
out.release()

cv2.destroyAllWindows()
