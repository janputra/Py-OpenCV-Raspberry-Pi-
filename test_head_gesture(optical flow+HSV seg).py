import numpy as np
import math
import cv2

def Avg(arr):
    arr= np.array(arr, np.float32)  
    kernel= np.array([[1/12,1/6,1/12],
                      [1/6,0,1/6],
                      [1/12,1/6,1/12]],np.float32)

    res=cv2.filter2D(arr,-1,kernel)


    return res

def HSVseg(image,hue):
    image = cv2.GaussianBlur(image, (11, 11), 0)
    mask=np.zeros_like((image),np.uint8)
    image=np.array(image)
    hsv= cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
    lower = [hue-10,10,10]
    upper = [hue+10,255,255]
    lower = np.array(lower,np.uint8)
    upper = np.array(upper,np.uint8)
    mask = cv2.inRange(hsv,lower,upper)
    return mask  

def SegInGray(image, hsvseg):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    result=np.zeros_like((image),np.uint8)
    
    result = cv2.erode(hsvseg,None,iterations = 2)
    result = cv2.dilate(result,None,iterations = 2)
    
    result=cv2.bitwise_and(image,image,mask=result)
    result = np.array(result,np.float32)
    
    return result
    

cap = cv2.VideoCapture(0)
ret,frame= cap.read()
frame=cv2.flip(frame,1)
frame=cv2.resize(frame,(320,240))
x,y,z= frame.shape
hsv=np.zeros_like(frame)
hsv[:,:,2]=255
angle=np.zeros((x,y))
uAvg=np.zeros((x,y))
vAvg=np.zeros((x,y))



Ix=np.zeros((x,y),np.float32)
Iy=np.zeros((x,y),np.float32)
It=np.zeros((x,y),np.float32)
u_tot=np.zeros((x,y),np.float32)
v_tot=np.zeros((x,y),np.float32)
alpha=5
ep=0.1

kernel1= np.array([[0,0,0],
                   [0,-1,1],
                   [0,-1,1]],np.float32)/4
kernel2= np.array([[0,0,0],
                   [0,-1,-1],
                   [0,1,1]],np.float32)/4
kernel3= np.array([[0,0,0],
                   [0,1,1],
                   [0,1,1]],np.float32)/4
kernel4= np.array([[0,0,0],
                   [0,-1,-1],
                   [0,-1,-1]],np.float32)/4

while(1):

    
    #Hue= cv2.getTrackbarPos('hue','HSVseg')
    old=HSVseg(frame,10)
    old= SegInGray(frame,old)
    
    ret,frame= cap.read()
    frame=cv2.flip(frame,1)
    frame=cv2.resize(frame,(320,240))
    new = HSVseg(frame,10)
    new= SegInGray(frame,new)

    Ix = cv2.filter2D(new,-1,kernel1)+cv2.filter2D(old,-1,kernel1)
    Iy = cv2.filter2D(new,-1,kernel2)+cv2.filter2D(old,-1,kernel2) 
    It=cv2.filter2D(new,-1,kernel3)+cv2.filter2D(old,-1,kernel4)    

    u=np.zeros((x,y),np.float32)
    v=np.zeros((x,y),np.float32)
   
    while True:    

            u_prev=np.array(u)
            v_prev=np.array(v)
            uAvg=Avg(u)
            vAvg=Avg(v)

            u=np.around(uAvg-Ix*(((Ix*uAvg)+(Iy*vAvg)+It)/
                              ((alpha**2)+(Ix**2)+(Iy**2))),1)
            v=np.around(vAvg-Iy*(((Ix*uAvg)+(Iy*vAvg)+It)/
                              ((alpha**2)+(Ix**2)+(Iy**2))),1)
            Sig=np.sum((u-u_prev)**2+(v-v_prev)**2)/(x*y)
            
            if Sig<ep**2:
                break
            
##    u_tot= u_tot+u
##    v_tot=v_tot+v



    mag,ang=cv2.cartToPolar(u[:,:],v[:,:])
    hsv[:,:,0]=(ang*(180/math.pi))/2
    hsv[:,:,1]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

    hsv=np.array(hsv,np.uint8)
    bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

    cv2.imshow('HSVseg',np.array((new),np.uint8))

    cv2.imshow('OF',bgr)
##    print(np.sum(u))
##    print(np.sum(v))
    if cv2.waitKey(1)&0xFF== ord('q'):
        break
    if cv2.waitKey(1)&0xFF== ord('s'):
        cv2.imwrite('testHSV.jpg',np.array((new),np.uint8))

cap.release()
cv2.destroyAllWindows()
