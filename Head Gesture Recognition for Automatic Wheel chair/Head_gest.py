#Output as text and shown in Terminal

from imageoperator import Operation
from PiVidStream import vidstream
import time
import serial
import math
import numpy as np
import cv2



##ser= serial.Serial(
##    port='/dev/ttyACM0',
##    baudrate =9600)


cv=Operation()
stream=vidstream((160,120)).start()
time.sleep(5)
YCCseg=cv.YCCSeg
OF=cv.OpticalFlowLK


up=down=right=left= False
                                           
u=v=np.zeros((120,160))
n=j=k=l=0
bufMovU=bufMovV=np.zeros(10)
avgU=avgV=fil_U=fil_V=0
state="Static Center"
dynamic="-"
info=None
total_distanceX=0
total_distanceY=0
moved="-"
if __name__ == '__main__':
    while True:
      #  start = time.perf_counter()
#----------------Capturing image--------------#
        frame=stream.read()
#---------------Segmentation Process---------#
        newframe=YCCseg(frame,mode="gray")
#---------------Optical Flow Calucaltion--------#
        if n>1:
            u,v=OF(oldframe,newframe,win=3)
            n=1

        n=n+1
        oldframe=newframe
#--------------------------------------------#
        
#-------------mean calculation------------       
        avgU=u.sum()/(u!=0).sum()
        avgV=v.sum()/(v!=0).sum()
#-----------------------------------------
#-----------------Moving Average-----------#
        bufMovU[l]=avgU
        bufMovV[l]=avgV
        l=l+1
        if l>=10:
            l=9
        fil_U=bufMovU.sum()/10
        fil_V=bufMovV.sum()/10
        bufMovU=np.roll(bufMovU,-1)
        bufMovV=np.roll(bufMovV,-1)
#------------------------------------------#

        if fil_U>-0.1 and  fil_U<0.1 and fil_V>-0.1 and  fil_V<0.1:
            
            if state=="Static Center":
                if moved=="Right":
                    state="Static Right"
                elif moved=="Left":
                    state="Static Left"
                elif moved=="Up":
                    state="Static Up"
                elif moved=="Down":
                    state="Static Down"
            elif state=="Static Right":
                if moved=="Left":
                    state="Static Center"
            elif state=="Static Left":
                if moved=="Right":
                    state="Static Center"
            elif state=="Static Down":
                if moved=="Up":
                    state="Static Center"
            elif state=="Static Up":
                if moved=="Down":
                    state="Static Center"
            dynamic="-"
            total_distanceX=0
            total_distanceY=0
            moved="-"         
                    
        elif fil_U<-0.1:
            if dynamic=="-":
                dynamic ="Left"
        elif fil_U>0.1:
            if dynamic=="-":
                dynamic = "Right"
        elif fil_V<-0.1:
            if dynamic=="-":
                dynamic="Down"
        elif fil_V>0.1:
            if dynamic=="-":
                dynamic="Up"

        
        if (dynamic=="Left" or dynamic=="Right"):#and (dynamic!="Up" or dynamic !="Down"):
            total_distanceX+=fil_U

        if (dynamic=="Up" or dynamic=="Down"):#and (dynamic=="Up" or dynamic =="Down"):
            total_distanceY+=fil_V

        print (total_distanceY)
##
        if total_distanceX>3:
            moved= "Right"
        elif total_distanceX<-3:
            moved="Left"
##
        if total_distanceY>2:
            moved= "Up"
        elif total_distanceY<-2:
            moved="Down"

        if state=="Static Center":
            print('Center')
        elif state=="Static Right":
            print('Menoleh Kanan')
        elif state=="Static Left":
            print('Menoleh Kiri')
        elif state=="Static Down":
            print('Menunduk')
        elif state=="Static Up":
            print('Menengadah')





        #print('time:',time.perf_counter() - start)
##        if data!='no':
##            ser.write(bytes(data,'UTF-8'))
##        print('Gesture',gesture,'|','Gerakan Kepala:',HeadGesture,'|',"Command dikirim",data)
        cv2.imshow('frame',newframe)
              
        if cv.KeyAct('q'):
            break
        
    stream.stop()
    cv.stop()


