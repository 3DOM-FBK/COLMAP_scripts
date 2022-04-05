import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import multiprocessing
import math
from PIL import Image
#from skimage.feature import match_descriptors
#from skimage.measure import ransac
#from skimage.transform import ProjectiveTransform
from multiprocessing import Pool

from lib import RearrangeKpts
from lib import BruteForce

from config import image_folder
from config import desc_folder
from config import colmap_desc_folder
from config import matches_folder
from config import tile_folder
from config import cross_check
from config import pool_N
from config import local_feature
from config import check
from config import matching_distance
from config import matching_strategy
from config import ratio_thresh
from config import dict_with_custom_pairs
from config import matching_approach

global image_list
image_list = os.listdir(image_folder)

################################################################################
def HalfRange(a, N):
################################################################################
    c = round(-(math.sqrt(2*a*a-2*a*(2*N-1)+2*N*N-2*N+1)-2*N+1)/2)
    print(c)
    return c

################################################################################
def PoolRanges(N_images, N_process):
################################################################################
    pool_ranges = []
    new_pool_ranges = []
    pool_ranges.append(range(0, N_images))
    N = N_images
    a = 1
    for n in range(0, int(N_process/2)):
        for r in pool_ranges:
            r_list = list(r)
            a = r_list[0]
            N = r_list[-1]+1
            c = HalfRange(a, N)
            new_pool_ranges.append(range(a, c))
            new_pool_ranges.append(range(c, N))
        pool_ranges = new_pool_ranges
        new_pool_ranges = []
    print(pool_ranges)
    return pool_ranges

################################################################################
#def matcherBF(desc_1, desc_2, cross_check):
################################################################################
    #matches = match_descriptors(desc_1, desc_2, cross_check=cross_check)
    #return matches

################################################################################
def subset(img_range):
################################################################################
    matches_dict = {}
    keypoints_dict = {}
    iteration = 0
    for img1 in img_range:
        kpts_1, desc_1, kpts_numb_1 = RearrangeKpts.rearrangeKpts(  image_list[img1],
                                                                    image_folder,
                                                                    desc_folder,
                                                                    colmap_desc_folder,
                                                                    matches_folder,
                                                                    tile_folder,
                                                                    local_feature
                                                                    )
        
        keypoints_dict[image_list[img1]] = cv2.KeyPoint_convert(kpts_1)
        for img2 in range(img1+1, len(image_list)):
            print("Image pair:", image_list[img1], image_list[img2])
            kpts_2, desc_2, kpts_numb_2 = RearrangeKpts.rearrangeKpts(  image_list[img2],
                                                                        image_folder,
                                                                        desc_folder,
                                                                        colmap_desc_folder,
                                                                        matches_folder,
                                                                        tile_folder,
                                                                        local_feature
                                                                    )
            #matches_dict["{} {}".format(image_list[img1], image_list[img2])] = matcherBF(desc_1, desc_2, cross_check)
            opencv_matches = BruteForce.BrForce(desc_1, desc_2, check, matching_distance, cross_check, matching_strategy, print_debug=False, ratio_thresh=0.8)
            matches_matrix = np.zeros((len(opencv_matches), 2))
            for l in range(0,len(opencv_matches)):
                matches_matrix[l][0] = int(opencv_matches[l].queryIdx)
                matches_matrix[l][1] = int(opencv_matches[l].trainIdx)
            matches_dict["{} {}".format(image_list[img1], image_list[img2])] = matches_matrix
            iteration += 1
    print("ITERATIONS:\t\t\t", iteration)
    return keypoints_dict, matches_dict

################################################################################
# MAIN STARTS HERE
if __name__ == "__main__":

    if len(image_list) < 20:
        ris = subset(range(0, len(image_list)))
        with open("{}/matches.txt".format(matches_folder), "w") as matches_file:
            for key in ris[1]:
                matches_file.write("{}\n".format(key))
                for row in range(0,len(ris[1][key])):
                    matches_file.write("{:.0f} {:.0f}\n".format(ris[1][key][row][0], ris[1][key][row][1]))
                matches_file.write("\n\n")
                        
        for key in ris[0]:
            with open("{}/{}.txt".format(colmap_desc_folder, key), "w") as kps_file:
                kps_file.write('{} 128\n'.format(len(ris[0][key])))
                for k in range(0,len(ris[0][key])):
                    kps_file.write("{:.6f} {:.6f} 0.000000 0.000000\n".format(ris[0][key][k][0],ris[0][key][k][1]))


    else:
        pool_ranges = PoolRanges(len(image_list), pool_N)
        start = np.zeros((len(pool_ranges),))
        end = np.zeros((len(pool_ranges),))
        print(start,end)
        for r in range(0,len(pool_ranges)):
            r_list = list(pool_ranges[r])
            start[r] = min(r_list)
            end[r] = max(r_list)+1
        print(start,end)
        start[0] = 0
        end[pool_N-1] = len(image_list)
        for i in range(0, pool_N-1):
            end[i] = start[i+1]
        print(start,end)
        for i in range(0, pool_N):
            pool_ranges[i] = range(int(start[i]), int(end[i]))
        print(pool_ranges)
        
        image_list = os.listdir(image_folder)
        print("nunmber_of_images\t", len(image_list))
        print("image_list\t\t", image_list)
        print("image_folder\t\t", image_folder)
        print("desc_folder\t\t", desc_folder)
        print("colmap_desc_folder\t", colmap_desc_folder)
        print("matches_folder\t\t", matches_folder)
        print("cross_check\t\t", cross_check)
        print("number_of_CPUs\t\t", multiprocessing.cpu_count())
        print("pool_ranges\t\t", pool_ranges)
        
        if input("Do you want to continue?") != "y":
            quit()  

        with Pool (pool_N) as p:
            #ris = p.map(subset, [range(0,1), range(1,3)])
            ris = p.map(subset, pool_ranges)    

            #print(type(ris), len(ris))
            #print(type(ris)[0], len(ris[0]))
            #print(type(ris)[1], len(ris[1]))
            #print(ris[0])
            #print(ris[1])
            
        with open("{}/matches.txt".format(matches_folder), "w") as matches_file:
            for r in ris:
                for key in r[1]:
                    matches_file.write("{}\n".format(key))
                    for row in range(0,len(r[1][key])):
                        matches_file.write("{:.0f} {:.0f}\n".format(r[1][key][row][0], r[1][key][row][1]))
                    matches_file.write("\n\n")
                        
        for r in ris:
            for key in r[0]:
                with open("{}/{}.txt".format(colmap_desc_folder, key), "w") as kps_file:
                    kps_file.write('{} 128\n'.format(len(r[0][key])))
                    for k in range(0,len(r[0][key])):
                        kps_file.write("{:.6f} {:.6f} 0.000000 0.000000\n".format(r[0][key][k][0],r[0][key][k][1]))
            
            #final_kps = ris[0][0]
            #final_matches = ris[0][1]
        
        #matches_dict, keypoints_dict = subset(range(0,2))
        #print(len(matches_dict))
        #print(len(keypoints_dict)) 
    

