# Copyright Niantic 2019. Patent Pending. All rights reserved.
#
# This software is licensed under the terms of the Monodepth2 licence
# which allows for non-commercial use only, the full terms of which are made
# available in the LICENSE file.

from __future__ import absolute_import, division, print_function

import os
import sys
import glob
import argparse
import numpy as np
import PIL.Image as pil
import matplotlib as mpl
import matplotlib.cm as cm

import torch
from torchvision import transforms, datasets

from monodepth2 import networks
from monodepth2.layers import disp_to_depth
from monodepth2.utils import download_model_if_doesnt_exist
from monodepth2.evaluate_depth import STEREO_SCALE_FACTOR
import cv2


def monodepth2(image,pos):
    print(image.shape)
    print(image)
    """Function to predict for a single image or folder of images
    """
    model_name = "mono_1024x320"
    assert model_name is not None, \
        "You must specify the --model_name parameter; see README.md for an example"

    no_cuda=True
    if torch.cuda.is_available() and not no_cuda:
            device = torch.device("cuda")
    else:
            device = torch.device("cpu")

    model_path = os.path.join("monodepth2\models", model_name)
    print("-> Loading model from ", model_path)
    encoder_path = os.path.join(model_path, "encoder.pth")
    depth_decoder_path = os.path.join(model_path, "depth.pth")

    # LOADING PRETRAINED MODEL
    print("   Loading pretrained encoder")
    encoder = networks.ResnetEncoder(18, False)
    loaded_dict_enc = torch.load(encoder_path, map_location=device)

    # extract the height and width of image that this model was trained with
    feed_height = loaded_dict_enc['height']
    feed_width = loaded_dict_enc['width']
    filtered_dict_enc = {k: v for k, v in loaded_dict_enc.items() if k in encoder.state_dict()}
    encoder.load_state_dict(filtered_dict_enc)
    encoder.to(device)
    encoder.eval()

    print("   Loading pretrained decoder")
    depth_decoder = networks.DepthDecoder(
        num_ch_enc=encoder.num_ch_enc, scales=range(4))

    loaded_dict = torch.load(depth_decoder_path, map_location=device)
    depth_decoder.load_state_dict(loaded_dict)

    depth_decoder.to(device)
    depth_decoder.eval()

    output_directory = './'

    # PREDICTING ON EACH IMAGE IN TURN
    with torch.no_grad():

        original_width = image.shape[1]
        original_height=image.shape[0]

        # input_image = input_image.resize((feed_width, feed_height), pil.LANCZOS)
        input_image = cv2.resize(image,(feed_width, feed_height),interpolation=cv2.INTER_AREA)
        input_image = transforms.ToTensor()(input_image).unsqueeze(0)


        # PREDICTION
        input_image = input_image.to(device)
        features = encoder(input_image)
        outputs = depth_decoder(features)

        disp = outputs[("disp", 0)]
        disp_resized = torch.nn.functional.interpolate(
            disp, (original_height, original_width), mode="bilinear", align_corners=False)

        output_name='name'
        scaled_disp, depth = disp_to_depth(disp, 0.1, 100)
        # if args.pred_metric_depth:
        #     name_dest_npy = os.path.join(output_directory, "{}_depth.npy".format(output_name))
        #     metric_depth = STEREO_SCALE_FACTOR * depth.cpu().numpy()
        #     np.save(name_dest_npy, metric_depth)
        # else:
        #     name_dest_npy = os.path.join(output_directory, "{}_disp.npy".format(output_name))
        #     np.save(name_dest_npy, scaled_disp.cpu().numpy())

        # Saving colormapped depth image
        disp_resized_np = disp_resized.squeeze().cpu().numpy()

        #predict depth
        depth=disp_resized_np[pos[1],pos[0]]

        vmax = np.percentile(disp_resized_np, 95)
        normalizer = mpl.colors.Normalize(vmin=disp_resized_np.min(), vmax=vmax)
        mapper = cm.ScalarMappable(norm=normalizer, cmap='magma')
        colormapped_im = (mapper.to_rgba(disp_resized_np)[:, :, :3] * 255).astype(np.uint8)
        im = pil.fromarray(colormapped_im)

        name_dest_im = os.path.join(output_directory, "{}_disp.jpeg".format(output_name))
        im.save(name_dest_im)

    print('-> Done!')
    return depth

