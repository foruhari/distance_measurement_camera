import os.path
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import MyData

import numpy as np
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets
from camera_calibration import calibration

# from main import MainWindow



class CalibWindow(QWidget):
    counter = 0
    def __init__(self):
        super(CalibWindow, self).__init__()
        self.setWindowTitle("کالیبراسیون")
        self.setGeometry(500, 45, 500, 500)
        self.setStyleSheet("background-color: rgb(206, 217, 255)")

        self.menuBar = QMenuBar(self)
        self.exitAction = QAction(QIcon('img_1.png'), 'back', self)
        self.menuBar.addAction(self.exitAction)
        self.menuBar.show()

        font = QtGui.QFont("B Nazanin")
        font.setPointSize(10)
        font.setWeight(61)

        self.left = QPushButton()
        self.left.setText("تصاویر دوربین سمت چپ")
        self.left.setFont(font)
        self.left.clicked.connect(self.open_left_imgs)

        self.textbox = QLineEdit(self)
        self.textbox.resize(280, 40)
        self.textbox.setEnabled(False)
        self.textbox.setText("C:/Users\Lenovo\PycharmProjects\myCalibration\images/stereoLeft")
        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(self.textbox,stretch = 1)
        hboxLayout.addWidget(self.left,stretch = 1)

        self.right = QPushButton()
        self.right.setText("تصاویر دوربین سمت راست")
        self.right.setFont(font)
        self.right.clicked.connect(self.open_right_imgs)

        self.textbox1 = QLineEdit(self)
        self.textbox1.resize(280, 40)
        self.textbox1.setEnabled(False)
        self.textbox1.setText("C:/Users\Lenovo\PycharmProjects\myCalibration\images/stereoRight")
        font1 = QtGui.QFont("B Nazanin")
        font1.setPointSize(12)
        font1.setWeight(60)

        hboxLayout1 = QHBoxLayout()
        hboxLayout1.addWidget(self.textbox1,stretch = 1)
        hboxLayout1.addWidget(self.right,stretch = 1)

        self.row = QLabel()
        self.row.setText("تعداد خانه های افقی:")
        self.row.setFont(font1)
        self.row.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.textbox2 = QLineEdit(self)
        self.textbox2.resize(280, 40)
        self.textbox2.setEnabled(True)
        self.textbox2.setMaxLength(1)
        self.textbox2.setText("8")
        self.textbox2.textChanged.connect(self.textchanged2)


        hboxLayout2 = QHBoxLayout()
        hboxLayout2.addWidget(self.textbox2,stretch = 1)
        hboxLayout2.addWidget(self.row,stretch = 1)

        self.culmn = QLabel()
        self.culmn.setText("تعداد خانه های عمودی:")
        self.culmn.setFont(font1)
        self.culmn.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.textbox3 = QLineEdit(self)
        self.textbox3.resize(280, 40)
        self.textbox3.setEnabled(True)
        self.textbox3.setMaxLength(1)
        self.textbox3.setText("7")
        self.textbox3.textChanged.connect(self.textchanged3)


        hboxLayout3 = QHBoxLayout()
        hboxLayout3.addWidget(self.textbox3,stretch = 1)
        hboxLayout3.addWidget(self.culmn,stretch = 1)

        self.size = QLabel()
        self.size.setText("اندازه خانه های شطرنجی(میلی متر):")
        self.size.setFont(font1)
        self.size.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)

        self.textbox4 = QLineEdit(self)
        self.textbox4.resize(280, 40)
        self.textbox4.setEnabled(True)
        self.textbox4.setMaxLength(4)
        self.textbox4.setText("51")

        self.textbox4.textChanged.connect(self.textchanged4)

        hboxLayout4 = QHBoxLayout()
        hboxLayout4.addWidget(self.textbox4,stretch = 1)
        hboxLayout4.addWidget(self.size,stretch = 1)

        font3 = QtGui.QFont("B Nazanin")
        font3.setPointSize(12)
        font3.setWeight(55)

        self.calibration = QPushButton()
        self.calibration.setText(" شروع کالیبراسیون")
        self.calibration.setFont(font3)
        # self.calibration.setEnabled(False)
        self.calibration.clicked.connect(self.calib)

        self.entry = QPushButton()
        self.entry.setText("ورود")
        self.entry.setFont(font3)
        self.entry.setEnabled(False)
        # self.entry.clicked.connect(self.go_to_fistwindow)

        self.save = QPushButton()
        self.save.setText("ذخیره نتایج کالیبراسیون")
        self.save.setFont(font3)
        self.save.setEnabled(False)
        self.save.clicked.connect(self.save_mat)

        hboxLayout5 = QHBoxLayout()
        hboxLayout5.addWidget(self.calibration,stretch = 1)
        hboxLayout5.addWidget(self.save, stretch=1)
        hboxLayout5.addWidget(self.entry, stretch=1)


        font4 = QtGui.QFont("B Nazanin")
        font4.setPointSize(13)
        font4.setWeight(55)

        self.label = QLabel(self)
        self.label.setAutoFillBackground(False)
        self.label.setText("برای کالیبراسیون از صفحه شطرنجی استفاده کرده و تصاویر گرفته شده\nاز دوربین ها را بارگذاری کنید:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter| QtCore.Qt.AlignLeft|QtCore.Qt.AlignJustify)
        self.label.setFont(font4)


        self.VBL = QVBoxLayout()
        self.VBL.setSpacing(20)
        self.VBL.addStretch()
        self.VBL.addWidget(self.label)
        self.VBL.addStretch()

        self.VBL.addLayout(hboxLayout)
        self.VBL.addLayout(hboxLayout1)
        self.VBL.addLayout(hboxLayout2)
        self.VBL.addLayout(hboxLayout3)
        self.VBL.addLayout(hboxLayout4)

        self.setLayout(self.VBL)
        self.VBL.addStretch()
        self.VBL.addLayout(hboxLayout5)

    def textchanged2(self,text):
        MyData.Data.row = int(text)

    def textchanged3(self,text):
        MyData.Data.culmn = int(text)

    def textchanged4(self,text):
        MyData.Data.size = int(text)

    def open_left_imgs(self):
        file = str(QFileDialog.getExistingDirectory(self, "تصاویر دوربین سمت چپ"))
        # self.lef_filename, _ = QFileDialog.getExistingDirectory(self, "تصاویر دوربین سمت چپ")
        MyData.Data.left_folder_dir = file
        self.textbox.setText(file)
        self.textbox.setEnabled(True)
        self.counter += 1
        if self.counter == 2:
            self.calibration.setEnabled(True)

    def open_right_imgs(self):
        file = str(QFileDialog.getExistingDirectory(self, "تصاویر دوربین سمت راست"))
        # self.right_filename, _ = QFileDialog.getOpenFileName(self, "تصاویر دوربین سمت راست")
        MyData.Data.Right_folder_dir = file
        self.textbox1.setText(file)
        self.textbox1.setEnabled(True)
        self.counter += 1
        if self.counter == 2:
            self.calibration.setEnabled(True)

    def calib(self):
        MyData.Data.row = int(self.textbox2.text())
        MyData.Data.culmn = int(self.textbox3.text())
        MyData.Data.size = int(self.textbox4.text())
        MyData.Data.left_folder_dir = self.textbox.text()
        MyData.Data.Right_folder_dir = self.textbox1.text()

        print(MyData.Data.left_folder_dir)
        print(MyData.Data.Right_folder_dir)
        print(MyData.Data.row)
        print(MyData.Data.culmn)
        print(MyData.Data.size)

        if (MyData.Data.left_folder_dir!="") and (MyData.Data.Right_folder_dir!=""):
            print("zz")
            calibration(MyData.Data.left_folder_dir,MyData.Data.Right_folder_dir,MyData.Data.row-1,MyData.Data.culmn-1)
            self.calibration.setEnabled(False)
            self.entry.setEnabled(True)
            self.save.setEnabled(True)
        # else:
        #     print("error")
    #
    # def go_to_fistwindow(self):
    #     self.window = MainWindow()
    #     self.window.show()
    #     self.close()

    def save_mat(self):
        print("Saving parameters to HDD!")
        filename,_ = QFileDialog.getSaveFileName(self,'save calibration result',filter=("*.xml"))

        cv_file = cv2.FileStorage(filename, cv2.FILE_STORAGE_WRITE)

        cv_file.write('stereoMapL_x', MyData.Data.leftMapX)
        cv_file.write('stereoMapL_y', MyData.Data.leftMapY)
        cv_file.write('stereoMapR_x', MyData.Data.rightMapX)
        cv_file.write('stereoMapR_y', MyData.Data.rightMapY)
        cv_file.write('Q_mat', MyData.Data.Q)

        cv_file.release()
