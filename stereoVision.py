from PSMNet.psmnet import psmnet_cpu
from siamFC_method_test.siamFC_method import siamfc
from siamFC_method_test.yolo import yolo
import MyData
import cv2


class stereo_vision:
    def __init__(self, imageL,imageR,pos,B,F):

        self.imgL = imageL
        self.imgR = imageR
        self.position = pos
        self.baseline = B
        self.f_pixel = F

        # if self.method == 'dens_depth':
        #     dis=self.method1()

    def method1(self): #psmnet
        print(self.position)
        disp=psmnet_cpu(self.imgL, self.imgR,self.position)
        print(disp)
        depth = (self.f_pixel * self.baseline) /(disp*1000)
        return depth

    def yolo_out(self): #yolo
        MyData.Data.boxes = yolo(self.imgL)

    def method2(self,BB):  #siamFC
        X2 = siamfc(self.imgL, self.imgR,BB) #check position input and output?
        return X2
