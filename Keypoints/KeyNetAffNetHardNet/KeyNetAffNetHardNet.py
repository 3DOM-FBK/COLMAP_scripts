import matplotlib.pyplot as plt
import torch
import kornia as K
import inspect
import numpy as np
import cv2
import kornia.feature as KF
from kornia_moons.feature import *
import os

device=torch.device('cpu') # 'cpu' or 'cuda'
N_keypoints = 40
images_folder = r"./tiles"
output_folder = r"./outs"


# MAIN STARTS HERE
#kn = KF.KeyNetAffNetHardNet(num_features = N_keypoints).eval().to(device)

def load_torch_image(fname):
    img = K.image_to_tensor(cv2.imread(fname), False).float() /255.
    img = K.color.rgb_to_grayscale(K.color.bgr_to_rgb(img))
    return img

images = os.listdir(images_folder)
for image in images:
    img = load_torch_image(r"{}/{}".format(images_folder,image)).to(device)
    keypts = KF.KeyNetAffNetHardNet(num_features = N_keypoints).forward(img)
    
    print(keypts[0].size())
    keypts_locations = keypts[0].cpu().detach().numpy()[-1,:,:,-1]
    print(keypts_locations.shape)

    print(keypts[2].size())
    keypts_descriptors = keypts[2].cpu().detach().numpy()[-1,:,:]
    print(keypts_descriptors.shape)

    out_loc = r"{}/{}.kpt.npy".format(output_folder, image)
    out_desc = r"{}/{}.dsc.npy".format(output_folder, image)
    np.save(out_loc, keypts_locations)
    np.save(out_desc, keypts_descriptors)
    

"""
images = os.listdir(images_folder)
for image in images:
    img = load_torch_image(r"{}/{}".format(images_folder,image)).to(device)
    keypts = kn.forward(img)

    print(type(keypts))
    print(keypts[0].size())
    print(keypts[1].size())
    print(keypts[2].size())
    kpts_locations = keypts[0].cpu().detach().numpy()
    descriptors_locations = keypts[2].cpu().detach().numpy()
    print("...conversion to numpy arrays")
    print("kpts_locations: ", kpts_locations.shape)
    print("descriptors_locations: ", descriptors_locations.shape)
"""