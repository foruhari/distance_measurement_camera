import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore

import MyData
import cv2

from PyQt5 import QtCore, QtGui, QtWidgets

from main import MainWindow
from calib_window import CalibWindow


class FirstWindow(QWidget):
    def __init__(self):
        super(FirstWindow, self).__init__()
        self.setWindowTitle("فاصله یابی")
        self.setGeometry(500, 45, 500, 450)
        self.setStyleSheet("background-color: rgb(206, 217, 255)")

        # self.menuBar = QMenuBar(self)
        # self.exitAction = QAction(QIcon('img_1.png'), 'back', self)
        # self.menuBar.addAction(self.exitAction)
        # # self.exitAction.triggered.connect(self.close)
        # self.menuBar.show()




        font = QtGui.QFont("B Nazanin")
        font.setPointSize(12)
        font.setWeight(55)

        self.entry = QPushButton()
        self.entry.setText("ادامه")
        self.entry.setFont(font)
        # self.entry.clicked.connect(self.go_to_mainWindow)
        self.entry.setEnabled(False)

        hboxLayout_l = QHBoxLayout()
        hboxLayout_l.addWidget(self.entry, stretch=1)

        self.label = QLabel(self)
        self.label.setAutoFillBackground(False)
        self.label.setText("مشخصات دوربین و ماتریس حاصل از کالیبراسیون را وارد کنید و یا\nوارد صفحه کالیبراسیون شوید:")
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        font1 = QtGui.QFont("B Nazanin")
        font1.setPointSize(13)
        font1.setWeight(55)
        self.label.setFont(font1)

        font2 = QtGui.QFont("B Nazanin")
        font2.setPointSize(12)
        font2.setWeight(60)

        self.focal = QLabel(self)
        self.focal.setAutoFillBackground(False)
        self.focal.setText("فاصله کانونی (میلی متر):")
        self.focal.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.focal.setFont(font2)

        self.textbox1 = QLineEdit(self)
        # self.textbox1.setPlaceholderText("2.88")
        self.textbox1.setText("2.88")
        self.textbox1.setMaxLength(4)
        self.textbox1.resize(280, 40)
        # self.textbox1.textChanged.connect(self.textchanged)

        hboxLayout1 = QHBoxLayout()
        hboxLayout1.addWidget(self.textbox1, stretch=1)
        hboxLayout1.addWidget(self.focal, stretch=1)

        self.baseLine = QLabel(self)
        self.baseLine.setAutoFillBackground(False)
        self.baseLine.setText("فاصله بین دو دوربین (سانتی متر):")
        self.baseLine.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        self.baseLine.setFont(font2)
        # self.baseLine.setEnabled(False)

        self.textbox2 = QLineEdit(self)
        # self.textbox2.setPlaceholderText("33")
        self.textbox2.setText("33")
        self.textbox2.setMaxLength(5)
        self.textbox2.resize(280, 40)
        # self.textbox2.textChanged.connect(self.textchanged2)

        hboxLayout2 = QHBoxLayout()
        hboxLayout2.addWidget(self.textbox2, stretch=1)
        hboxLayout2.addWidget(self.baseLine, stretch=1)

        font3 = QtGui.QFont("B Nazanin")
        font3.setPointSize(10)
        font3.setWeight(61)

        self.load = QRadioButton()
        self.load.setText("بارگذاری")
        self.load.setFont(font3)
        self.load.toggled.connect(self.load_mat)
        # self.load.setEnabled(False)

        hboxLayout3 = QHBoxLayout()
        hboxLayout3.addWidget(self.load,stretch = 1,alignment = QtCore.Qt.AlignRight)

        self.calib_radiobtn = QRadioButton()
        self.calib_radiobtn.setText("کالیبراسیون")
        self.calib_radiobtn.setFont(font3)
        self.calib_radiobtn.toggled.connect(self.calib_window)
        # self.calib_radiobtn.setEnabled(False)

        hboxLayout3.addWidget(self.calib_radiobtn,stretch = 1,alignment = QtCore.Qt.AlignRight)

        self.calib_btn = QPushButton()
        self.calib_btn.setText("ماتریس کالیبراسیون")
        self.calib_btn.setFont(font3)
        self.calib_btn.clicked.connect(self.open_calib_mat)
        self.calib_btn.setEnabled(False)

        self.textbox3 = QLineEdit(self)
        self.textbox3.resize(280, 40)
        self.textbox3.setEnabled(False)

        hboxLayout5 = QHBoxLayout()
        hboxLayout5.addWidget(self.textbox3,stretch = 1)
        hboxLayout5.addWidget(self.calib_btn,stretch = 1)

        self.VBL = QVBoxLayout()
        self.VBL.setSpacing(20)
        self.VBL.addWidget(self.label)
        self.VBL.addStretch()

        self.VBL.addLayout(hboxLayout1)
        self.VBL.addLayout(hboxLayout2)
        self.VBL.addLayout(hboxLayout3)
        self.VBL.addLayout(hboxLayout5)

        self.setLayout(self.VBL)
        self.VBL.addStretch()
        self.VBL.addLayout(hboxLayout_l)

    def load_mat(self):
        if self.load.isChecked() == True:
            self.calib_btn.setEnabled(True)
            self.entry.setEnabled(True)

    def calib_window(self):
        if self.calib_radiobtn.isChecked() == True:
            self.calib_btn.setEnabled(False)
            self.entry.setEnabled(True)


    #
    # def go_to_mainWindow(self):
    #
    #     print(self.load.isChecked())
    #     MyData.Data.focal_length = float(self.textbox.text())
    #     MyData.Data.FOV = int(self.textbox1.text())
    #     MyData.Data.baseLine = float(self.textbox2.text())
    #     # if (self.load.isChecked() == True):
    #     #     self.window = MainWindow()
    #     #     self.window.show()
    #     #     self.close()
    #     # elif (self.calib_radiobtn.isChecked() == True):
    #     #     self.window1 = CalibWindow()
    #     #     self.window1.show()
    #     #     self.close()

    # def go_to_calibWindow(self):
    #     self.window1 = CalibWindow()
    #     self.window1.show()
    #     self.close()

    def open_calib_mat(self):
        file, _= QFileDialog.getOpenFileName(self, "ماتریس کالیبراسیون")
        cv_file = cv2.FileStorage()
        cv_file.open(file, cv2.FileStorage_READ)
        MyData.Data.leftMapX = cv_file.getNode('stereoMapL_x').mat()
        MyData.Data.leftMapY = cv_file.getNode('stereoMapL_y').mat()
        MyData.Data.rightMapX = cv_file.getNode('stereoMapR_x').mat()
        MyData.Data.rightMapY = cv_file.getNode('stereoMapR_y').mat()
        MyData.Data.Q = cv_file.getNode('Q_mat').mat()
        print(MyData.Data.size)
        print(MyData.Data.Q)
        self.textbox3.setText(file)
        self.textbox3.setEnabled(True)
        self.entry.setEnabled(True)

    # def textchanged(self,text):
    #     MyData.Data.focal_length = int(text)
    #
    # def textchanged2(self,text):
    #     MyData.Data.baseLine = int(text)



