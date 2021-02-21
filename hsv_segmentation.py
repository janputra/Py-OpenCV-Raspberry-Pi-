#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


def nothing(x):
    pass
cv2.namedWindow('test')
cv2.namedWindow('mask')

#initialize the camera and grab a reference to the raw camera capture
camera =PiCamera()
camera.resolution =(640,480)
camera.vflip=True
camera.hflip=True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

#creating trackbar
cv2.createTrackbar('h', 'mask',0,179,nothing)
#cv2.createTrackbar('s', 'test',0,179,nothing)
#cv2.createTrackbar('v', 'test',0,179,nothing)
s,v,h=100,100,100

cv2.createTrackbar('val', 'test',0,255,nothing)
val=0

#allow the camera to warm up
time.sleep(0.1)

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



    
    hsv= cv2.cvtColor(target, cv2.COLOR_BGR2HSV)
    h=cv2.getTrackbarPos('h','mask')
    #s=cv2.getTrackbarPos('s','test')
    #v=cv2.getTrackbarPos('v','test')
    #define range of hsv
    lower = [h-4,50,50]
    upper =[h+4,255,255]
    lower = np.array(lower,np.uint8)
    upper = np.array(upper,np.uint8)
    
    mask = cv2.inRange(hsv,lower,upper)

    #show the frame
   # cv2.imshow("Frame",image)
    cv2.imshow("test", target)
    cv2.imshow("mask",mask)
    
    key = cv2.waitKey(1)&0xFF

    #clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    #if the q key was pressed, break from the loop
    if key == ord("q"):
        break

    if key ==ord("s"):
       # cv2.imwrite('frame.png',image)
        cv2.imwrite('red.png',target)
        cv2.imwrite('mask.png',mask)
    
cv2.destroyAllWindows()
