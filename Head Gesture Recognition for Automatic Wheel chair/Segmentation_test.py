from imageoperator import Operation
from PiVidStream import vidstream
import time
import serial
import math
import numpy as np
import cv2
import numpy as np


cv=Operation()
stream=vidstream((160,120)).start()

YCCseg=cv.YCCSeg
HSV=cv.HSVSeg

up=down=right=left= False
forward=backward=stop=False
gesture1=gesture2= "no"

#time.sleep(2)
#oldframe=cv.makeArray((240,320))
Hgesture=Vgesture="No"
u=v=np.zeros((240,320))
n=0
posX=posY=0
time.sleep(5)

if __name__ == '__main__':
    while True:
        
        frame=stream.read()
        
        ycc=YCCseg(frame,mode="binary")
        ycc1=YCCseg(frame,mode="gray")
##        ycc1=YCCseg(frame,mode="gray")
##        hsv=HSV(frame,mode="binary")
##
##        if n==5:
##            cv2.imwrite('yccPer.png',ycc)
##            cv2.imwrite('oriPer.png',frame)
##        if n==6:
##            cv2.imwrite('yccPer1.png',ycc)
##            cv2.imwrite('oriPer1.png',frame)
##        n=n+1
       # cv2.imshow('Frame',frame)
        cv2.imshow('YCraCrb',ycc)
        cv2.imshow('YCraCrb1',ycc1)
        cv2.imshow('test',frame)
##        cv2.imshow('HSV',ycc1)
        if cv.KeyAct('q'):
            break
        if cv.KeyAct('s'):
            cv2.imwrite('Ori1.png',frame)
            cv2.imwrite('ycc.png',ycc1)
            cv2.imwrite('Ycc1.png',ycc)
   
    stream.stop()
    cv.stop()
