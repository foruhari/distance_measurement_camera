from __future__ import print_function
import argparse
import os
import random
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torch.nn.functional as F
import numpy as np
import time
import math
# from models import *
from PSMNet.models import *
import cv2
from PIL import Image


def psmnet_cpu(imageL, imageR, pos):
    # imageL = cv2.imread(imageL)
    # imageR = cv2.imread(imageR)
    # 2012 data /media/jiaren/ImageNet/data_scene_flow_2012/testing/

    parser = argparse.ArgumentParser(description='PSMNet')
    parser.add_argument('--KITTI', default='2015',
                        help='KITTI version')
    parser.add_argument('--datapath', default='/media/jiaren/ImageNet/data_scene_flow_2015/testing/',
                        help='select model')
    parser.add_argument('--loadmodel', default='PSMNet/pretrained_sceneflow_new.tar',
                        help='loading model')
    # parser.add_argument('--loadmodel', default='PSMNet/pretrained_model_KITTI2015.tar',
    #                     help='loading model')

    parser.add_argument('--model', default='stackhourglass',
                        help='select model')
    parser.add_argument('--maxdisp', type=int, default=192,
                        help='maxium disparity')
    parser.add_argument('--no-cuda', action='store_true', default=True,
                        help='enables CUDA training')
    parser.add_argument('--seed', type=int, default=1, metavar='S',
                        help='random seed (default: 1)')
    args = parser.parse_args()
    args.cuda = not args.no_cuda and torch.cuda.is_available()

    torch.manual_seed(args.seed)
    if args.cuda:
        torch.cuda.manual_seed(args.seed)

    if args.model == 'stackhourglass':
        model = stackhourglass(args.maxdisp)
    elif args.model == 'basic':
        model = basic(args.maxdisp)
    else:
        print('no model')
    device = torch.device('cpu')
    model = nn.DataParallel(model, device_ids=[0])

    if args.loadmodel is not None:
        print('load PSMNet')
        state_dict = torch.load(args.loadmodel, map_location=torch.device('cpu'))
        model.load_state_dict(state_dict['state_dict'])
        model = model.module.to(device)

    def test(imgL, imgR):
        imgL = imgL.to(device)
        imgR = imgR.to(device)
        model.eval()

        if args.cuda:
            imgL = imgL.cuda()
            imgR = imgR.cuda()

        with torch.no_grad():
            disp = model(imgL, imgR)
            disp.data.to(device)

        disp = torch.squeeze(disp)
        pred_disp = disp.data.cpu().numpy()

        return pred_disp

    # def main():
    normal_mean_var = {'mean': [0.485, 0.456, 0.406],
                       'std': [0.229, 0.224, 0.225]}
    infer_transform = transforms.Compose([transforms.ToTensor(),
                                          transforms.Normalize(**normal_mean_var)])


    imgL = infer_transform(imageL)
    imgR = infer_transform(imageR)


    # pad to width and hight to 16 times
    if imgL.shape[1] % 16 != 0:
        times = imgL.shape[1] // 16
        top_pad = (times + 1) * 16 - imgL.shape[1]
    else:
        top_pad = 0

    if imgL.shape[2] % 16 != 0:
        times = imgL.shape[2] // 16
        right_pad = (times + 1) * 16 - imgL.shape[2]
    else:
        right_pad = 0

    imgL = F.pad(imgL, (0, right_pad, top_pad, 0)).unsqueeze(0)
    imgR = F.pad(imgR, (0, right_pad, top_pad, 0)).unsqueeze(0)


    # # start_time = time.time()
    pred_disp = test(imgL, imgR)
    # # print('time = %.2f' %(time.time() - start_time))
    #
    if top_pad != 0 and right_pad != 0:
        img = pred_disp[top_pad:, :-right_pad]
    elif top_pad == 0 and right_pad != 0:
        img = pred_disp[:, :-right_pad]
    elif top_pad != 0 and right_pad == 0:
        img = pred_disp[top_pad:, :]
    else:
        img = pred_disp

    depth = img[pos[1], pos[0]]

    # for test
    img = (img * 256).astype('uint16')
    img = Image.fromarray(img)
    img.save('Test_disparity2.png')
    # print('1')


    return depth

    # if __name__ == '__main__':
    # start_time = time.time()
    # main()
    # print('time = %.2f' % (time.time() - start_time))