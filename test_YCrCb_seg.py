import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow('test')
def nothing(x):
    pass

#cv2.createTrackbar('val','test',0,179,nothing)

coorX=np.zeros((480,640))
coorY=np.zeros((480,640))

for x in range(480):
    coorX[x,:]=x

for y in range(640):
    coorY[:,y]=y
    
while(1):
    ret,frame= cap.read()
    frame=  cv2.GaussianBlur(frame, (11, 11), 0)
    #result = cv2.GaussianBlur(frame, (3, 3), 0)
    
    mask=np.zeros((480,640),np.uint8)
    #val= cv2.getTrackbarPos('val','test')
    
    ycc =cv2.cvtColor(frame,cv2.COLOR_BGR2YCrCb)
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

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    result= cv2.inRange(ycc,lower,upper)

##  result = np.zeros((480,640),np.uint8)
##  result = np.where(mask<=0,0,gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    result = cv2.erode(result,None,iterations = 2)
    result = cv2.dilate(result,None,iterations = 2)
    
##    posX=np.where(result==0,0,coorX)
##    posY=np.where(result==0,0,coorY)
##
##    Xmax=np.amax(posX)
##    Ymax=np.amax(posY)
##
##    posX=np.where(result==0,1000,coorX)
##    posY=np.where(result==0,1000,coorY) 
##    Xmin=np.amin(posX)
##    Ymin=np.amin(posY)
##
##    x= int(((Xmax-Xmin)/2)+Xmin)
##    y=int(((Ymax-Ymin)/2)+Ymin)
##    circle=np.zeros((480,640,3),np.uint8)
##    cv2.circle(circle, (x,y), 100, (255, 255, 255), -1)
##    mask=cv2.cvtColor(circle,cv2.COLOR_BGR2GRAY)
    result=cv2.bitwise_and(gray,gray,mask=result)
    result = np.array(result,np.uint8)
    cv2.imshow('frame',frame)
    
    cv2.imshow('test',result)
    if cv2.waitKey(1)&0xFF== ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
