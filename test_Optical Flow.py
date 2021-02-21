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
    mask=np.zeros_like((image),np.uint8)
    image=np.array(image)
    hsv= cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
    lower = [hue-4,10,10]
    upper = [hue+4,255,255]
    lower = np.array(lower,np.uint8)
    upper = np.array(upper,np.uint8)
    mask = cv2.inRange(hsv,lower,upper)
    return mask  


frame1= cv2.imread("test0049.bmp")
x,y,z= frame1.shape

hsv=np.zeros_like(frame1)
hsv[:,:,2]=255
angle=np.zeros((x,y))
uAvg=np.zeros((x,y))
vAvg=np.zeros((x,y))


Ix=np.zeros((x,y),np.float32)
Iy=np.zeros((x,y),np.float32)
It=np.zeros((x,y),np.float32)
u_tot=np.zeros((x,y),np.float32)
v_tot=np.zeros((x,y),np.float32)
alpha=10


frame=np.zeros((x,y,37),np.float16)
for i in range (37):
    frame[:,:,i]=cv2.cvtColor(cv2.imread("test00"+str(29+i)+".bmp"),cv2.COLOR_BGR2GRAY)


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


n=0
ep=0.01
for a in range(5):
    old=np.array(frame[:,:,17+a],np.float32)
    new = np.array(frame[:,:,17+a+1],np.float32)
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
            n+=1
            if Sig<ep**2:
                break
            
    u_tot= u_tot+u
    v_tot=v_tot+v



mag,ang=cv2.cartToPolar(u_tot[:,:],v_tot[:,:])
hsv[:,:,0]=(ang*(180/math.pi))/2
hsv[:,:,1]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)

hsv=np.array(hsv,np.uint8)
bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
print(n)
print(np.sum(u_tot))
print(np.sum(v_tot))
cv2.imshow('frame',bgr)
cv2.imwrite('test4.png',bgr)
