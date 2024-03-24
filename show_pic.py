from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2
import time
# from test import MainWindow
import MyData


class show_cap(QThread):
    def __init__(self):
        super().__init__()
        # self.cap = None
        # self.cap_R = None

    imageUpdate = pyqtSignal(QImage)
    num = 0

    def set_info(self, capL,capR):
        self.cap = capL
        self.cap_R = capR
        self.convertToQtFormat = None

    def run(self):
        self.ThreadActive = True
        # self.ret, self.frame = self.cap.read()
        # self.retR, self.frameR = self.cap_R.read()

        image=self.cap
        imageR=self.cap_R
        # image = cv2.imread('images/stereoLeft/imageL0.jpg')
        # print(image)
        # imageR = cv2.imread('images/stereoRight/imageR0.jpg')
        # if self.ret and self.ThreadActive:
        #     image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        #     imageR = cv2.cvtColor(self.frameR, cv2.COLOR_BGR2RGB)
            # MainWindow.imgMat = image
            # dim = (640,360)
            # image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

        height, width, channel = image.shape
        bytesPerLine = channel * width
        self.convertToQtFormat = QImage(image.copy(), width, height, bytesPerLine, QImage.Format_RGB888)
        MyData.Data.img = self.convertToQtFormat
        MyData.Data.imgMat = image
        MyData.Data.imgMatR = imageR
        self.imageUpdate.emit(self.convertToQtFormat)
        # t1 = time.time()
        # print(t1-t0)
        # self.ThreadActive = False

