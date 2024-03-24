import cv2
# import MyData
import numpy as np


class calibrateimg:
    def __init__(self, imageL,imageR,matrixname='stereoMap.xml'): #matrixname is string

        self.imgL = imageL
        self.imgR = imageR
        self.xml_matrix = matrixname

    def cal(self):
        cv_file = cv2.FileStorage()
        cv_file.open(self.xml_matrix, cv2.FileStorage_READ)


        stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        self.imgL = cv2.imread(self.imgL) #برداشته شود (فقط برای تست هست)
        self.imgR = cv2.imread(self.imgR) #برداشته شود (فقط برای تست هست)


        Left_nice= cv2.remap(self.imgL,stereoMapL_x,stereoMapL_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)
        Right_nice= cv2.remap(self.imgR,stereoMapR_x,stereoMapR_y, cv2.INTER_LANCZOS4, cv2.BORDER_CONSTANT, 0)

        # out = Right_nice.copy()
        # out[:,:,0] = Right_nice[:,:,0]
        # out[:,:,1] = Right_nice[:,:,1]
        # out[:,:,2] = Left_nice[:,:,2]
        #
        # cv.imshow("Output image", out)
        # cv.waitKey(0)


        return Left_nice, Right_nice
