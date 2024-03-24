import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

# from camera_reader import camera_reader
import MyData
# import test
from monoVision import mono_vision
from stereoVision import stereo_vision
from siamFC_method_test.yolo import yolo
from siamFC_method_test.measurement import measurement

import numpy as np
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets


class SecondWindow(QDialog):
    picPix = None
    pause = False
    # np_image = None
    # np_imageR = None

    def __init__(self,method,num_of_cams):
        super(SecondWindow, self).__init__()
        self.setWindowTitle("فاصله یابی")
        # self.setGeometry(500, 45, 740, 680)
        self.setGeometry(500, 45, 1300, 850)
        self.setStyleSheet("background-color: rgb(200, 200, 250);")

        self.menuBar = QMenuBar(self)
        self.exitAction = QAction(QIcon('img_1.png'), 'back', self)
        self.menuBar.addAction(self.exitAction)
        self.menuBar.show()

        self.output = QLabel(self)
        # self.output.setGeometry(50, 100, 640, 480)
        self.output.setGeometry(10, 65, 1280, 720)
        self.output.setStyleSheet("\n""background-color: rgb(255, 255, 255);")
        self.output.setObjectName("video")
        # self.output.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.output,stretch=1)

        self.distance = QLabel(self)
        # self.distance.setGeometry(QtCore.QRect(50, 810, 1280, 60))
        # self.distance.setGeometry(QtCore.QRect(65, 785, 1280, 65))
        self.distance.setAutoFillBackground(False)
        self.distance.setText("")
        self.distance.setScaledContents(False)
        self.distance.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.distance.setObjectName("distance")
        self.distance.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        font3 = QtGui.QFont("B Nazanin")
        font3.setBold(True)
        font3.setPointSize(15)
        font3.setWeight(60)
        self.distance.setFont(font3)

        hboxLayout2 = QHBoxLayout()
        hboxLayout2.addWidget(self.distance, stretch=1)


        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 20, 1280, 31))
        font = QtGui.QFont("B Nazanin")
        font.setPointSize(15)
        font.setWeight(55)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("روی یک نقطه کلیک کنید:")
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)


        self.setMouseTracking(True)

        # self.img = image
        MyData.Data.left_nice = cv2.remap(MyData.Data.imgMat, MyData.Data.leftMapX, MyData.Data.leftMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        MyData.Data.right_nice = cv2.remap(MyData.Data.imgMatR, MyData.Data.rightMapX, MyData.Data.rightMapY, cv2.INTER_LINEAR, cv2.BORDER_CONSTANT)
        # self.np_imageR = right_rectified
        self.img = QImage(MyData.Data.left_nice,1280, 720, 3840, QImage.Format_RGB888)
        self.method = method
        self.cams = num_of_cams

        if (self.method == 'روش دو') & (self.cams == 'دو دوربین'):
            MyData.Data.boxes , MyData.Data.left_nice= yolo(MyData.Data.left_nice)

        if (self.method == 'روش دو') and (self.cams == 'یک دوربین'):
            MyData.Data.boxes, MyData.Data.left_nice = yolo(MyData.Data.left_nice)
            self.label3 = QLabel(self)
            self.label3.setText("اندازه واقعی جسم را وارد کنید:(متر):")
            self.label3.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            font1 = QtGui.QFont("B Nazanin")
            font1.setPointSize(12)
            font1.setWeight(60)
            self.label3.setFont(font1)

            self.textbox=QLineEdit(self)
            self.textbox.setMaxLength(3)
            self.textbox.resize(280, 40)
            self.textbox.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
            self.textbox.textChanged.connect(self.textchange)

            hboxLayout2.addWidget(self.textbox, stretch=1)
            hboxLayout2.addWidget(self.label3, stretch=1)

        self.VBL = QVBoxLayout()
        self.VBL.addWidget(self.label,stretch=1)
        # self.VBL.addStretch()

        self.VBL.addLayout(hboxLayout, stretch=1)

        # self.VBL.addStretch()
        self.VBL.addLayout(hboxLayout2,stretch=1)
        self.setLayout(self.VBL)


        if MyData.Data.boxes != []:
            self.img = QImage(MyData.Data.left_nice,1280, 720, 3840, QImage.Format_RGB888)

        # if self.img != None:
        #     self.convertQImageToMat(self.img.copy())


    def getFrame(self):
        # scaled = image.scaled(640, 480, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # self.picPix = scaled.copy()
        self.picPix = self.img.copy()
        pix = QPixmap.fromImage(self.picPix)
        self.set_pic(pix)

    def set_pic(self,pic):
        self.output.setPixmap(pic)
        self.output.setScaledContents(True)


    def mousePressEvent(self, event):
        # SecondWindow.np_image = test.MainWindow.imgMat
        q=MyEvent(self.method,self.cams)
        depth = q.pos(event)
        if depth == "None":
            self.distance.setText("ناحیه نامعتبر")
        else:
            self.distance.setText('فاصله = %.2f متر' %(depth))

    def textchange(self, text):
        MyData.Data.objHeight=text

class MyEvent(QThread):
    def __init__(self, method,cams):
        self.method = method
        self.num_of_cams = cams
    def pos(self,event):
        depth = 0
        # SecondWindow.np_image = MyData.Data.imgMat
        # SecondWindow.np_image = cv2.resize(SecondWindow.np_image,(640,480))

        if event.button() == Qt.LeftButton:
            if (event.x()<=10) or (event.x()>=1290) or ((event.y()<=65) or (event.y()>=785)):
                return "None"

            else:
                if not(np.all((MyData.Data.Q == 0))):
                    print("1111")
                    baseLine_Q = MyData.Data.Q[3][2]
                    print(baseLine_Q)
                    f_pixel = float(MyData.Data.Q[2][3])
                    print(f_pixel)
                else:
                    print("5555")
                    baseLine_Q = MyData.Data.baseLine
                    print(baseLine_Q)
                    f_pixel = (MyData.Data.imgMat.shape[0])/(2*np.tan( (MyData.Data.FOV/2) *np.pi/180 ))
                    print(f_pixel)

                if self.num_of_cams == 'یک دوربین':
                    print(MyData.Data.left_nice)
                    x = mono_vision(MyData.Data.left_nice,[event.x()-10,event.y()-65])
                    if self.method == 'روش یک':
                        print("mono depth")
                        disp = x.method1()
                        depth = (1/disp)*1.84
                    elif self.method == 'روش دو':
                        print("second method")
                        if MyData.Data.boxes != []:
                            for j in range(len(MyData.Data.boxes)):
                                x_min, y_min = MyData.Data.boxes[j][0], MyData.Data.boxes[j][1]
                                w, h = MyData.Data.boxes[j][2], MyData.Data.boxes[j][3]
                                x_max = x_min + w
                                y_max = y_min + h
                                if (event.x() - 10 > x_min) and (event.x() - 10 < x_max) and (
                                        event.y() - 65 > y_min) and (event.y() - 65 < y_max):
                                    MyData.Data.BB = [x_min, y_min, w, h]
                            if MyData.Data.BB != ():
                                MyData.Data.objHeight = float(MyData.Data.objHeight)
                                depth = x.method2(MyData.Data.BB,f_pixel)
                                MyData.Data.boxes = []
                                MyData.Data.BB = ()
                    return depth
                elif self.num_of_cams == 'دو دوربین':
                    print("stereo")
                    print(baseLine_Q,f_pixel)
                    x = stereo_vision(MyData.Data.left_nice, MyData.Data.right_nice,[event.x()-10,event.y()-65],baseLine_Q,f_pixel)
                    if self.method == 'روش یک':
                        print("psmnet")
                        depth = x.method1()
                    elif self.method == 'روش دو':
                        print("siamFC")
                        if MyData.Data.boxes != []:
                            for j in range(len(MyData.Data.boxes)):
                                x_min, y_min = MyData.Data.boxes[j][0], MyData.Data.boxes[j][1]
                                w, h = MyData.Data.boxes[j][2], MyData.Data.boxes[j][3]
                                x_max = x_min +w
                                y_max = y_min +h
                                if (event.x()-10>x_min) and (event.x()-10<x_max) and (event.y()-65>y_min) and (event.y()-65<y_max):
                                    MyData.Data.BB=(x_min,y_min,w,h)
                            if MyData.Data.BB != ():
                                X1 = MyData.Data.BB[0] + (MyData.Data.BB[2]/2)
                                X2 = x.method2(MyData.Data.BB)
                                w = (np.arctan(640/f_pixel)*2)*180/np.pi
                                print(w)
                                # depth = (measurement(X2,X1,baseLine_Q,w))/1000
                                print(baseLine_Q,f_pixel)
                                depth = (baseLine_Q*f_pixel)/(abs(X2-X1)*1000)
                                MyData.Data.boxes = []
                                MyData.Data.BB = ()
                    return depth
