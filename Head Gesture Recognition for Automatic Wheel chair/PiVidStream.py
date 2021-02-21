from threading import Thread
import cv2



class vidstream:
    def __init__(self, resolution):
        self.capture=cv2.VideoCapture(0)
        self.resolution=resolution
        self.stopped=False
        self.frame=None
        
    def start(self):
        Thread(target=self.update,args=()).start()
        return self

    def update(self):
        while True:
            
            ret,self.frame=self.capture.read()
            
            if self.stopped:
                
                return
            
    def read(self):
        temp=cv2.flip(self.frame,1)
        temp=cv2.resize(temp,self.resolution)
        return temp

    def stop(self):
        self.stopped=True
        self.capture.release()
        
