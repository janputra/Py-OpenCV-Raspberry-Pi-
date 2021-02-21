import cv2
import numpy as np
import math


class Operation:
    def __init__(self):
        super(Operation,self).__init__()
        self.kernel1= np.array([[0,0,0],
                               [0,-1/4,1/4],
                               [0,-1/4,1/4]],np.float32)
        self.kernel2= np.array([[0,0,0],
                               [0,-1/4,-1/4],
                               [0,1/4,1/4]],np.float32)
        self.kernel3= np.array([[0,0,0],
                               [0,1/4,1/4],
                               [0,1/4,1/4]],np.float32)
        self.kernel4= np.array([[0,0,0],
                                [0,-1/4,-1/4],
                                [0,-1/4,-1/4]],np.float32)
        
        self.kernelAvg =np.array([[1/12,1/6,1/12],
                                  [1/6,0,1/6],
                                  [1/12,1/6,1/12]],np.float32)
        self.capture=None
        
        
    
      
        
    def start(self):
        self.capture=cv2.VideoCapture(1)
        return self

    def get_frame(self,size):
        ret,frame=self.capture.read() 
        frame=cv2.flip(frame,1)
        x,y=size
        frame=cv2.resize(frame,(x,y))
        return frame
    
    def stop(self):
        #self.capture.release()
        cv2.destroyAllWindows()

    def KeyAct(self, key):
        if cv2.waitKey(1)&0xFF==ord(key):
            return True

        
    
    def YCCSeg(self,image,mode): #input image bgr, mode=binary or gray
        G=cv2.GaussianBlur(image,(11,11),0)
        ycc=cv2.cvtColor(G,cv2.COLOR_BGR2YCrCb)
        
        ymin=np.amin(ycc[:,:,0])
        ymax=np.amax(ycc[:,:,0])
        Cb_min= 77
        Cb_max= 127
        Cr_min= 133
        Cr_max= 173
        
        lower=[ymin,Cr_min,Cb_min]
        upper=[ymax,Cr_max,Cb_max]
        lower=np.array(lower)
        upper=np.array(upper)
        result= cv2.inRange(ycc,lower,upper)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        temp=cv2.dilate(result,None,iterations=3)
        temp=cv2.erode(temp,None,iterations=3)
        if mode=="binary":
            return temp
        if mode=="gray":         
            resgray=cv2.bitwise_and(gray,gray,mask=temp)
            return resgray
        
    def HSVSeg(self,image,mode):
        #G=cv2.GaussianBlur(image,(7,7),0)
        hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

        lower=[0,70,0]
        upper=[15,150,255]
        lower=np.array(lower)
        upper=np.array(upper)
        result=cv2.inRange(hsv,lower,upper)
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        temp=cv2.dilate(result,None,iterations=3)
        temp=cv2.erode(temp,None,iterations=3)
        if mode=="binary":
            return temp
        if mode=="gray":           
            resgray=cv2.bitwise_and(gray,gray,mask=temp)
            return resgray
        
    
    def OpticalFlowHS(self,frame1,frame2,alpha,ep):
        x,y=frame1.shape
        old=np.array(frame1,np.float32)
        new=np.array(frame2,np.float32)
        Ix = cv2.filter2D(new,-1,self.kernel1)+cv2.filter2D(old,-1,self.kernel1)
        Iy = cv2.filter2D(new,-1,self.kernel2)+cv2.filter2D(old,-1,self.kernel2) 
        It = cv2.filter2D(new,-1,self.kernel3)+cv2.filter2D(old,-1,self.kernel4)

        u=np.zeros((x,y),np.float32)
        v=np.zeros((x,y),np.float32)

        while True:
            u_prev=u
            v_prev=v

            uAvg=cv2.filter2D(u,-1,self.kernelAvg)
            vAvg=cv2.filter2D(v,-1,self.kernelAvg)
            
            temp=(((Ix*uAvg)+(Iy*vAvg)+It)/
                              ((alpha**2)+(Ix**2)+(Iy**2)))
            u=np.around(uAvg-Ix*temp,1)
            v=np.around(vAvg-Iy*temp,1)
            Sig=np.sum((u-u_prev)**2+(v-v_prev)**2)/(x*y)
            if Sig<ep**2:
                break
        return u,v
    


    def OpticalFlowLK(self,frame1,frame2,win):
        
        x,y=frame1.shape
        old=np.array(frame1,np.float32)
        new=np.array(frame2,np.float32)
        Ix = cv2.filter2D(new,-1,self.kernel1)+cv2.filter2D(old,-1,self.kernel1)
        Iy = cv2.filter2D(new,-1,self.kernel2)+cv2.filter2D(old,-1,self.kernel2) 
        It = (cv2.filter2D(new,-1,self.kernel3)+cv2.filter2D(old,-1,self.kernel4))*-1

        kernelWin=np.ones((win,win))
                          
        A=Ix**2
        B=Ix*Iy
        C=B
        D=Iy**2
        E=Ix*It
        F=Iy*It
        #inx,iny=np.indices((x,y))

        
        
        winA=cv2.filter2D(A,-1,kernelWin)
        winB=cv2.filter2D(B,-1,kernelWin)
        winC=winB
        winD=cv2.filter2D(D,-1,kernelWin)
        winE=cv2.filter2D(E,-1,kernelWin)
        winF=cv2.filter2D(F,-1,kernelWin)
        
        det=(winA*winD)-(winB*winC)
        
        u=np.where(np.logical_and(det!=0,det!=np.nan),(((winD*winE)/det)-((winC*winF)/det)),0)
        v=np.where(np.logical_and(det!=0,det!=np.nan),(((winB*winE)/det)-((winA*winF)/det)),0)
        return u,v
        
                                        
    
    def DrawOF(self,u,v,mode): #mode: 1."draw"-->return bgr
                                     #2."dir"--> return dominan ang & mag in total
                                     #3."all"--> return both 
        mag,ang=cv2.cartToPolar(u,v)
        
        ang=ang*(180/math.pi)
       
        
        x,y=u.shape
        hsv=np.zeros((x,y,3),np.uint8)
        hsv[:,:,0]=ang/2
        hsv[:,:,1]=cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        hsv[:,:,2]=255
        
        bgr=cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)
        return bgr
        
            

    
