#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

#initialize the camera and grab a reference to the raw camera capture
camera =PiCamera()
camera.resolution =(640,480)
camera.vflip=True
camera.hflip=True
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

#allow the camera to warm up
time.sleep(0.1)


#capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image=frame.array
    image = np.array(image,np.uint8)
    target = np.zeros((480,640,3),np.int16)

    #decreaseing red value operation 
    for y in range(640):
        for x in range(480):
            
            target[x,y,0]=image[x,y,0]
            target[x,y,1]=image[x,y,1]
            target[x,y,2]=image[x,y,2]-30
            if target[x,y,2]<0:
                target[x,y,2]=0
    target=np.array(target,np.uint8)
          
    #show the frame
    cv2.imshow("Frame",image)
    cv2.imshow("test", target)
   
    key = cv2.waitKey(1)&0xFF

    #clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    #if the q key was pressed, break from the loop
    if key == ord("q"):
        break
