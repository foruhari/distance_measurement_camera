from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import cv2
import time
from show_pic import show_cap
import qimage2ndarray

class camera_reader(QThread):
    def __init__(self):
        super().__init__()
        self.doRun = True

    fps = 0
    duration = 0

    signal1 = pyqtSignal(QImage)
    # mutex = QMutex()
    frame_counter = 0
    frame_count = 0

    cap = None
    #
    # def set_path(self,path):
    #     self.path = path

    def run(self):
        self.ThreadActive = True
        print("xx")
        t = time.time()
        # self.cap = cv2.VideoCapture("rtsp://admin:12345678aA@169.254.101.20:554/Streaming/Channels/1/")         #left camera
        # self.cap_R = cv2.VideoCapture("rtsp://admin:12345678Aa@169.254.101.21:554/Streaming/Channels/1/")         #righ camera
        self.cap = cv2.imread('images/stereoLeft/imageL0.jpg')

        self.cap_R = cv2.imread('images/stereoRight/imageR0.jpg')
        # print(self.cap)
        # self.fps = self.cap.get(5)
        # print(self.fps)
        t2 = time.time()
        print('read',t2 - t)


        while self.ThreadActive:
            # t0 = time.time()
            # self.mutex.lock()
            # self.frame_counter +=1
            vid = show_cap()
            vid.set_info(self.cap,self.cap_R)
            vid.imageUpdate.connect(self.ImageUpdateSlot1)
            vid.start()
            t1 = time.time()

            time.sleep(0.032)
            # time.sleep(1/self.fps)
            # self.mutex.unlock()

    def ImageUpdateSlot1(self,image):
        self.signal1.emit(image)
