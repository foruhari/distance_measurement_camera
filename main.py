import sys

import cv2
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import MyData
from camera_reader import camera_reader

from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
from second_window import SecondWindow


class MainWindow(QWidget):
    picPix = None
    pause = False
    img = None
    imgMat = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("فاصله یابی")
        # self.resize(728, 660)
        self.setGeometry(0, 45, 1300, 850)
        self.setStyleSheet("background-color: rgb(206, 217, 255);")

        self.menuBar = QMenuBar(self)
        self.exitAction = QAction(QIcon('11.png'), 'back', self)
        self.menuBar.addAction(self.exitAction)
        self.menuBar.show()

        self.output = QLabel()
        self.output.setGeometry(QtCore.QRect(40, 30, 640, 480))
        # self.output.setStyleSheet("\n""background-color: rgb(255, 255, 255);")
        self.output.setObjectName("video")
        self.output.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        #add QComboBox for choosing camera
        self.camera = QComboBox()
        self.camera.addItem("")
        self.camera.addItem("")
        self.camera.setItemText(0,"یک دوربین")
        self.camera.setItemText(1,"دو دوربین")

        font = QtGui.QFont("B Nazanin")
        font.setPointSize(12)
        font.setWeight(60)
        self.camera.setFont(font)

        #add QComboBox for choosing method
        self.method = QComboBox()
        self.method.addItem("")
        self.method.addItem("")
        self.method.setItemText(0,"روش یک")
        self.method.setItemText(1,"روش دو")
        self.method.setFont(font)

        #create button for distance measurement
        self.Distance = QPushButton()
        self.Distance.setText("فاصله یابی")
        self.Distance.clicked.connect(self.open_window)
        font1 = QtGui.QFont("B Nazanin")
        font1.setPointSize(13)
        font1.setBold(True)
        font1.setWeight(60)
        self.Distance.setFont(font1)

        # create button for playing
        self.play = QPushButton()
        self.play.setText("پخش")
        self.play.clicked.connect(self.play_video)
        self.play.setFont(font)

        # create button for pausing
        self.pause = QPushButton()
        self.pause.setText("توقف")
        self.pause.setEnabled(False)
        self.pause.clicked.connect(self.pause_video)
        self.pause.setFont(font)


        # set widgets to the hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout1 = QHBoxLayout()
        hboxLayout.addWidget(self.play)
        hboxLayout.addWidget(self.pause)
        hboxLayout1.addWidget(self.camera)
        hboxLayout1.addWidget(self.method)
        hboxLayout1.addWidget(self.Distance)
        # hboxLayout.setContentsMargins(0, 0, 0, 0)
        # hboxLayout1.setContentsMargins(0, 0, 0, 0)

        #create vbox layout
        self.VBL = QVBoxLayout()
        self.VBL.addStretch()
        self.VBL.addWidget(self.output)
        # self.VBL.addStretch()
        self.VBL.addLayout(hboxLayout)
        self.setLayout(self.VBL)
        self.VBL.addLayout(hboxLayout1)

        self.video = None
        self.pix = None

        self.setMouseTracking(True)




    def play_video(self):
        # print(MainWindow.pause)
        self.start_video()
            # self.pause = False

    def pause_video(self):
        # self.video.mutex.lock()
        MainWindow.pause = True
        self.video.ThreadActive = False

    def start_video(self):
        self.pause.setEnabled(True)
        self.video = camera_reader()
        self.video.signal1.connect(self.ImageUpdateSlot)
        self.video.start()

    def ImageUpdateSlot(self, image):
        MainWindow.img = image
        self.picPix = image.copy()
        self.pix = QPixmap.fromImage(self.picPix)
        # scaled = pix.scaled(640, 480, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.set_pic(self.pix)

    def set_pic(self,pic):
        self.output.setPixmap(pic)
        self.output.setScaledContents(True)



    def open_window(self):
        self.video.ThreadActive = False
        # scaled = MyData.Data.img.scaled(640, 480, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.window = SecondWindow(self.method.currentText(),self.camera.currentText())
        self.window.getFrame()
        # self.window = QtWidgets.QMainWindow()
        # self.ui = Ui_MainWindow()
        # self.ui.setupUi(self.window)
        # scaled = MainWindow.img.scaled(640, 480, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        # self.ui.getFrame(MainWindow.img)
        self.window.show()

        # self.window = Ui_MainWindow()
        # self.window.getFrame(MainWindow.img)
        # self.window.show()


