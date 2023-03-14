
import cv2
import threading
import time
import os

#to capture video class
class StreamingVideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update).start() #ran as a different thread to avoid getting stuck in the while true

    def __del__(self):
        self.video.release() #release all resources once object is destroyed

    def get_frame(self,id):
        image = self.frame #recieve the frame
        os.chdir(os.getcwd()+'\images')
        cv2.imwrite("data"+str(id)+".jpg",image)
        os.chdir(os.getcwd()+'\..')
        _, jpeg = cv2.imencode('.jpg', image) #converts (encodes) image formats into streaming data and stores it in-memory cache. It is mostly used to compress image data formats in order to make network transfer easier.
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read() #func to read from the video camera so that it can be displayed

def gen(camera):
    i=0
    while i<10:
        time.sleep(1)
        i+=1
        frame = camera.get_frame(i)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')