from tkinter import *
from tkinter.filedialog import askopenfilename

import sys
# sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2
import time

from siamFC_method_test.yolo import yolo
from siamFC_method_test.tracker import TrackerSiamFC

def siamfc(imageL,imageR,BB):
    # bb = ()
    tracker = TrackerSiamFC("siamFC_method_test/SiamFC.pth")
    # dim = (960, 540)
    # img_L = cv2.imread('remapL.jpg')
    img_L=imageL
    # img_L = cv2.resize(img_L, dim, interpolation=cv2.INTER_AREA)


    # img_R = cv2.imread('remapR.jpg')
    img_R = imageR
    # img_R = cv2.resize(img_R, dim, interpolation=cv2.INTER_AREA)
    start = time.time()
    # x, y, w, h = cv2.selectROI('model_name', img_L, False, False)
    # bb = [x, y, w, h]
    # bb = yolo(img_L)

    # print(bb)
    if BB != ():

        tracker.init(img_L,BB)



        pred = tracker.update(img_R)

        x_min = int(pred[0])
        y_min = int(pred[1])
        w = int(pred[2])
        h = int(pred[3])
        X2 = x_min + int(w / 2)
        Y2 = y_min + int(h / 2)
        # print(f"X''2={X2 - int(w / 4), Y2}")
        # print(f"X2={X2,Y2}")
        # print(f"X'2={X2 + int(w / 4), Y2}")
        cv2.rectangle(img_R, (int(pred[0]), int(pred[1])), (int(pred[0] + pred[2]), int(pred[1] + pred[3])), (0, 255, 255),3)
        cv2.imwrite('testtt.jpg', img_R)
        # stop = time.time()
        # print(stop - start)
    return X2




