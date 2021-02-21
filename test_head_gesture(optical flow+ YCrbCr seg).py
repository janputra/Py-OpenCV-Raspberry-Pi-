import numpy as np
import math
import cv2



bin_h = np.arange((360))

##for i in range(360):
##    bin_h[i]=i
direction=" "
def Avg(arr):
    arr= np.array(arr, np.float32)  
    kernel= np.array([[1/12,1/6,1/12],
                      [1/6,0,1/6],
                      [1/12,1/6,1/12]],np.float32)

    res=cv2.filter2D(arr,-1,kernel)
    return res

def YCCseg(image):
    image=  cv2.GaussianBlur(image, (11, 11), 0)
    ycc =cv2.cvtColor(image,cv2.COLOR_BGR2YCrCb)
    ycc=np.array(ycc,np.float32)
    ymin=np.amin(ycc[:,:,0])
    ymax=np.amax(ycc[:,:,0])
    Cb_min= (-11.098)-(4.265**2)
    Cb_max= (-11.098)+(4.265**2)
    Cr_min= (21.927)-(4.143**2)
    Cr_max= (21.927)+(4.143**2)
    ycc[:,:,1]=ycc[:,:,1]-128
    ycc[:,:,2]=ycc[:,:,2]-128
    lower=[ymin,Cr_min,Cb_min]
    upper=[ymax,Cr_max,Cb_max]
    lower=np.array(lower)
    upper=np.array(upper)
    result= cv2.inRange(ycc,lower,upper)
   
    return result 

def SegInGray(image, yccseg):
    image=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    result=np.zeros_like((image),np.uint8)
    result = cv2.erode(yccseg,None,iterations = 3)
    result = cv2.dilate(result,None,iterations = 3)
    
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
ep=0.01

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

old=np.zeros((x,y))

if __name__ == '__main__':

    while True:
##        old=YCCseg(frame)
##        old= SegInGray(frame,old)

        ret,frame= cap.read()
        frame=cv2.flip(frame,1)
        frame=cv2.resize(frame,(320,240))

        new = YCCseg(frame)
        new = SegInGray(frame,new)

        Ix = cv2.filter2D(new,-1,kernel1)+cv2.filter2D(old,-1,kernel1)
        Iy = cv2.filter2D(new,-1,kernel2)+cv2.filter2D(old,-1,kernel2) 
        It = cv2.filter2D(new,-1,kernel3)+cv2.filter2D(old,-1,kernel4)    
        old=new
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


        mag,ang=cv2.cartToPolar(u[:,:],v[:,:])
        hsv[:,:,0]=(ang*(180/math.pi))/2
        hsv[:,:,1]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)


        hsv=np.array(hsv,np.uint8)
        bgr = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        ang=np.round(ang*(180/math.pi))
        mag=np.round(mag)

        ang=np.where(mag==0,np.nan,ang) 

        hist,bin_edges= np.histogram(ang,bin_h)


        dir_ang= np.argmax(hist)

        if np.sum(mag) > 2000:
            if dir_ang==0:
                direction="Right"
            elif dir_ang==90:
                direction="Down"
            elif dir_ang==180:
                direction="Left"
            elif dir_ang==270:
                direction="Up"
        else:
            direction ="No"

        cv2.putText(frame,"Gesture : "+direction+" "+"angle :" + str(dir_ang) ,(10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (0, 0, 255), 3)
        cv2.imshow('YCCseg',frame)#np.array((new),np.uint8))
        cv2.imshow('OF',bgr)
        ##    if direction=="Left":
        ##        cv2.imwrite('left.jpg',frame)
        ##    elif direction=="Right":
        ##        cv2.imwrite('right.jpg',frame)
        ##    elif direction=="Down":
        ##        cv2.imwrite('down.jpg',frame)
        ##    elif direction=="Up":
        ##        cv2.imwrite('up.jpg',frame)
        #print(np.sum(mag))#,hist[90],hist[180],hist[270])


        if cv2.waitKey(1)&0xFF== ord('q'):
            break
        if cv2.waitKey(1)&0xFF== ord('s'):
            cv2.imwrite('testYcc.jpg',np.array((new),np.uint8))
    

cap.release()
cv2.destroyAllWindows()
