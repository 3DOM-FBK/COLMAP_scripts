import numpy as np
import pydegensac
import os

error_threshold = 10.0

colmap_desc = r'C:\Users\User\Desktop\Luca\Projects\Storiche_austria\RoRD\colmap_desc'
matches = r'C:\Users\User\Desktop\Luca\Projects\Storiche_austria\RoRD\matches\matches.txt'

verified_kpts_folder = r"C:\Users\User\Desktop\Luca\Projects\Storiche_austria\RoRD\verified_desc"
verified_matches_folder = r"C:\Users\User\Desktop\Luca\Projects\Storiche_austria\RoRD\verified_matches"

# MAIN STARTS HERE
kpts_dict = {}
matches_dict = {}

imgs_list = os.listdir(colmap_desc)
for c, item in enumerate(imgs_list):
    imgs_list[c] = item[:-4]

# Importing keypoints from file
for img in imgs_list:
    with open("{}/{}.txt".format(colmap_desc, img),'r') as kpt_file:
        kpts_dict[img] = np.loadtxt(kpt_file, delimiter=' ', skiprows=1, usecols=(0,1))
        #print(kpts_dict)

# Importing matches from file
controller = True
with open(matches, 'r') as match_file:
    lines = match_file.readlines()
    for line in lines:
        if line == '\n':
            controller = False
        else:
            line = line.strip()
            elem1, elem2 = line.split(' ', 1)
            if elem1 in imgs_list:
                img1 = elem1
                img2 = elem2
                pair = '{} {}'.format(img1, img2)
                matches_dict[pair] = np.empty((2,2), dtype=float)
            else:
                matches_dict[pair] = np.vstack((matches_dict[pair], np.array([elem1, elem2], ndmin=2)))

for m in matches_dict:
    matches_dict[m] = matches_dict[m][2:, :]

# Geometric verification
verified_kpts = {}
verified_matches = {}
for key in matches_dict:
    match1 = matches_dict[key][:, 0]
    match2 = matches_dict[key][:, 1]
    match1 = match1.astype(np.int)
    match2 = match2.astype(np.int)
    img1, img2 = key.split(" ", 1)
    feat1 = kpts_dict[img1]
    feat2 = kpts_dict[img2]

    #print(match2[:5])
    #print(feat2[:5, :])
    

    kpt_left = feat1[match1, :]
    kpt_right = feat2[match2, :]
    #print(kpt_right[:5, :])
    #quit()
    H, inliers = pydegensac.findHomography(kpt_left, kpt_right, error_threshold, 0.99, 10000)

    if img1 not in verified_kpts.keys():
        verified_kpts[img1] =  kpt_left[inliers]
    if img2 not in verified_kpts.keys():
        verified_kpts[img2] =  kpt_right[inliers]
    verified_matches[key] = np.array([(m, m) for m in range(kpt_left[inliers].shape[0])])
    print(verified_matches[key])
    print(kpt_left[inliers].shape, kpt_left[inliers].shape)

for img in imgs_list:
    with open("{}/{}.txt".format(verified_kpts_folder, img), "w") as colmap_desc_file:
        colmap_desc_file.write("{} {}\n".format(verified_kpts[img].shape[0], 128))
        for row in range(verified_kpts[img].shape[0]):
            colmap_desc_file.write("{} {} 0.000000 0.000000\n".format(verified_kpts[img][row, 0], verified_kpts[img][row, 1]))
        colmap_desc_file.write("\n")    

with open("{}/verified_matches.txt".format(verified_matches_folder), "w") as colmap_matches:
    for math_pair in verified_matches:
        colmap_matches.write("{}\n".format(math_pair))
        for row in range(verified_matches[math_pair].shape[0]):
            colmap_matches.write("{} {}\n".format(verified_matches[math_pair][row, 0], verified_matches[math_pair][row, 1]))
        colmap_matches.write("\n")


