import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cv2.namedWindow('test')
def nothing(x):
    pass

#cv2.createTrackbar('val','test',0,179,nothing)

def YCCseg(image):
    ycc =cv2.cvtColor(image,cv2.COLOR_BGR2YCrCb)
    ycc=np.array(ycc,np.float32)
    ymin=np.amin(ycc)
    ymax=np.amax(ycc)
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


ret,frame=cap.read()
old = YCCseg(frame)


while(1):
    ret,frame= cap.read()

    new=YCCseg(frame)
    old=new

    result=cv2.bitwise_or(old,new)

    #result = cv2.GaussianBlur(frame, (3, 3), 0)
    
   
    #val= cv2.getTrackbarPos('val','test')
    
 
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
##  result = np.zeros((480,640),np.uint8)
##  result = np.where(mask<=0,0,gray)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    result = cv2.erode(result,kernel,iterations = 2)
    result = cv2.dilate(result,kernel,iterations = 2)
    result = cv2.GaussianBlur(result, (3, 3), 0)
    result=cv2.bitwise_and(gray,gray,mask=result)
    result = np.array(result,np.uint8)
    cv2.imshow('frame',frame)
    
    cv2.imshow('test',result)
    if cv2.waitKey(1)&0xFF== ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
