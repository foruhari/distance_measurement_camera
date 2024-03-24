import numpy as np
import cv2
import glob
from PIL import Image

import MyData


def calibration(lef_dir,right_dir,row,culmn):
    print(lef_dir)
    print(right_dir)


    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)
    criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)

    objp = np.zeros((row * culmn, 3), np.float32)
    objp[:, :2] = np.mgrid[0:row, 0:culmn].T.reshape(-1, 2)

    # Arrays to store object points and image points from all images
    objpoints = []  # 3d points in real world space
    imgpointsR = []  # 2d points in image plane
    imgpointsL = []

    # Start calibration from the camera
    print('Starting calibration for the 2 cameras... ')

    left_imgs = []
    for filename in glob.glob(lef_dir+"/*"):
        img = cv2.imread(filename)
        left_imgs.append(img)

    right_imgs = []
    for filename in glob.glob(right_dir+"/*"):
        img = cv2.imread(filename)
        right_imgs.append(img)

    number_og_imgs = len(right_imgs)
    print(number_og_imgs)

    for i in range(0,number_og_imgs):
        ChessImaR = right_imgs[i][:,:,0]
        ChessImaL = left_imgs[i][:,:,0]
        retR, cornersR = cv2.findChessboardCorners(ChessImaR,
                                                   (row, culmn), cv2.CALIB_CB_ADAPTIVE_THRESH|cv2.CALIB_CB_FILTER_QUADS)
        retL, cornersL = cv2.findChessboardCorners(ChessImaL,
                                                   (row, culmn), cv2.CALIB_CB_ADAPTIVE_THRESH|cv2.CALIB_CB_FILTER_QUADS)
        if (True == retR) & (True == retL):
            objpoints.append(objp)
            cv2.cornerSubPix(ChessImaR, cornersR, (11, 11), (-1, -1), criteria)
            cv2.cornerSubPix(ChessImaL, cornersL, (11, 11), (-1, -1), criteria)
            imgpointsR.append(cornersR)
            imgpointsL.append(cornersL)

    retR, mtxR, distR, rvecsR, tvecsR = cv2.calibrateCamera(objpoints,
                                                            imgpointsR,
                                                            ChessImaR.shape[::-1], None, None)
    retL, mtxL, distL, rvecsL, tvecsL = cv2.calibrateCamera(objpoints,
                                                            imgpointsL,
                                                            ChessImaL.shape[::-1], None, None)
    # imgR = cv2.undistort(imgR,mtxR,distR)
    # cv2.imwrite('testR.png',imgR)

    # imgL = cv2.undistort(imgL,mtxL,distL)
    # cv2.imwrite('testL.png',imgL)
    ret, K1, D1, K2, D2, R, T, E, F = cv2.stereoCalibrate(objpoints,
                                                               imgpointsL,
                                                               imgpointsR,
                                                               mtxL,
                                                               distL,
                                                               mtxR,
                                                               distR,
                                                               ChessImaR.shape[::-1],
                                                               criteria_stereo,
                                                               cv2.CALIB_SAME_FOCAL_LENGTH|cv2.CALIB_ZERO_TANGENT_DIST)

    rectify_scale = 0  # if 0 image croped, if 1 image nor croped
    R1, R2, P1, P2, Q, roi_left, roi_right= cv2.stereoRectify(K1, D1, K2, D2,
                                                      ChessImaR.shape[::-1],
                                                      R, T,
                                                      flags=cv2.CALIB_ZERO_DISPARITY)

    leftMapX, leftMapY = cv2.initUndistortRectifyMap(K1, D1, R1, P1, ChessImaL.shape[::-1], cv2.CV_32FC1)
    rightMapX, rightMapY = cv2.initUndistortRectifyMap(K2, D2, R2, P2, ChessImaR.shape[::-1], cv2.CV_32FC1)

    Q [3][2] = (float(abs(1 / Q[3][2])))*(MyData.Data.size)

    print("Saving parameters to MyData!")

    MyData.Data.leftMapX = leftMapX
    MyData.Data.leftMapY = leftMapY
    MyData.Data.rightMapX = rightMapX
    MyData.Data.rightMapY = rightMapY
    MyData.Data.Q = Q
    print(Q)
    print("end of calibration")
    return
