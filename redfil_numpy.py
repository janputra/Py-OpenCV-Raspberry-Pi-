#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

def nothing(x):
    pass
cv2.namedWindow('test')

#initialize the camera and grab a reference to the raw camera capture
camera =PiCamera()
camera.resolution =(640,480)
camera.vflip=True
camera.hflip=True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

#allow the camera to warm up
time.sleep(0.1)

cv2.createTrackbar('val', 'test',0,255,nothing)
val=0

#capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image=frame.array
    image = np.array(image,np.uint8)
    target = np.zeros((480,640,3),np.uint8)

    val=cv2.getTrackbarPos('val','test')

    #decreaseing red value operation (use numpy function instead loop through pixel using python loop)
    target[:,:,0]= image[:,:,0]
    target[:,:,1]=image[:,:,1]
    red =image[:,:,2]
    red = np.array(red,np.int16)
    red = np.where((red-val)<0,0,red-val)
    red = np.array(red,np.uint8)  
    target[:,:,2]=red         
    #show the frame
    cv2.imshow("Frame",image)
    cv2.imshow("test", target)
   
    key = cv2.waitKey(1)&0xFF

    #clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    #if the q key was pressed, break from the loop
    if key == ord("q"):
        break
