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
N_keypoints = 8000
images_folder = r"./imgs_sample"
output_folder = r"./outs"


# MAIN STARTS HERE
kn = KF.KeyNetAffNetHardNet(N_keypoints).eval().to(device)
matcher = KF.LocalFeatureMatcher(kn, KF.DescriptorMatcher('smnn', 0.98)).to(device)

def load_torch_image(fname):
    img = K.image_to_tensor(cv2.imread(fname), False).float() /255.
    img = K.color.rgb_to_grayscale(K.color.bgr_to_rgb(img))
    return img

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

    # salvare in output directory i numpy arrays
    # usare la GPU