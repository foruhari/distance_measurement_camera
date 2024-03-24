import numpy as np
from first_window import FirstWindow
from second_window import SecondWindow
from calib_window import CalibWindow
from main import MainWindow
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Manager:
    status= None
    def __init__(self):
        self.first = FirstWindow()
        self.calib = CalibWindow()
        # self.second = SecondWindow()
        self.mainW = MainWindow()

        ##first -> main or calib
        self.first.entry.clicked.connect(self.fun)
        self.first.entry.clicked.connect(self.first.close)


        #calib -> first
        self.calib.exitAction.triggered.connect(self.first.show)
        self.calib.exitAction.triggered.connect(self.calib.close)

        #second -> main
        # self.second.exitAction.triggered.connect(self.mainW.show)
        # self.second.exitAction.triggered.connect(self.second.close)

        ##calib -> main
        self.calib.entry.clicked.connect(self.calib_to_main)
        self.calib.entry.clicked.connect(self.calib.close)

        #main -> first
        self.mainW.exitAction.triggered.connect(self.back_of_main)
        self.mainW.exitAction.triggered.connect(self.mainW.close)

        self.first.show()
    def fun(self):
        if self.first.calib_radiobtn.isChecked():
            self.calib.show()
        elif self.first.load.isChecked():
            self.mainW.show()
            Manager.status = "first"

    def back_of_main(self):
        if Manager.status == "first":
            self.first.show()
        elif Manager.status == "calib":
            self.calib.show()

    def calib_to_main(self):
        Manager.status = "calib"
        self.mainW.show()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    app_icon = QIcon("logo-distance.png")
    App.setWindowIcon(app_icon)
    # Root = FirstWindow()
    # Root.show()
    manager = Manager()
    sys.exit(App.exec())
