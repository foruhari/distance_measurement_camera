import numpy as np


class Data:

    #parameters of camera
    focal_length = 0
    FOV = 0
    baseLine = 0

    #parameters for calibration
    left_folder_dir = ""
    Right_folder_dir = ""
    row = 0
    culmn = 0
    size = 0

    #calibration parameters
    Q = np.zeros((4,4))
    leftMapX = None
    leftMapY = None
    rightMapX = None
    rightMapY = None

    #Qimage
    img = None

    #numpy array
    imgMatR = None
    imgMat = None

    #rectified imgs
    left_nice = None
    right_nice = None

    #boxes of yolo object detection
    boxes = []
    BB =()

    #parameter for second method of mono vision
    objHeight = 0