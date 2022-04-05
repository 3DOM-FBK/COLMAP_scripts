from config import image_folder
from config import desc_folder
from config import colmap_desc_folder
from config import matches_folder
from config import tile_folder
from config import custom_pairs

from config import tiling
from config import matching_approach
from config import local_feature
from config import cross_check
from config import check
from config import matching_distance
from config import matching_strategy
from config import ratio_thresh
from config import pool_N
from config import debug
from config import max_kpts_per_tile
from config import multhreading

from lib import BruteForce

from multiprocessing import Pool
from pathlib import Path
import numpy as np
import json
import os
import cv2

### D2Net
def D2Net(img_name, desc_folder, N_kpts):
    np_dsc_path = Path("{}.d2-net".format(img_name))
    abs_np_dsc_path = desc_folder / np_dsc_path
    
    # Import D2Net keypoints and descriptors
    with np.load(abs_np_dsc_path) as data:
        d = dict(zip(("keypoints","scores","descriptors"), (data[k] for k in data)))
    
    kp = d['keypoints']
    kp = kp[:N_kpts, :2]
    kp_numb = kp.shape[0]
    desc = d['descriptors']
    desc = desc[:N_kpts, :]
    
    return kp, desc, kp_numb

### RoRD
def RoRD(img_name, desc_folder, N_kpts):
    np_dsc_path = Path("{}.npy".format(img_name))
    abs_np_dsc_path = desc_folder / np_dsc_path
    
    # Import D2Net keypoints and descriptors
    with np.load(abs_np_dsc_path) as data:
        d = dict(zip(("keypoints","scores","descriptors"), (data[k] for k in data)))
    
    kp = d['keypoints']
    kp = kp[:N_kpts, :2]
    kp_numb = kp.shape[0]
    desc = d['descriptors']
    desc = desc[:N_kpts, :]
    
    return kp, desc, kp_numb

### FUNCTION TO GENERATE ALL IMAGE PAIRS TO BE MATCHED
def ImagePairs(matching_approach, image_list):

    image_pairs = []
    
    if matching_approach == "exhaustive":
        # Generating a list with all pairs
        for img1_index in range(len(image_list)-1):
            for img2_index in range(img1_index+1, len(image_list)):
                image_pairs.append((image_list[img1_index], image_list[img2_index]))

    elif matching_approach == "custom":
        # Importing pairs as a dictionary
        scene_graph_file = open(custom_pairs)
        scene_graph = json.load(scene_graph_file)
        scene_graph_file.close()
        
        # Generating a list with the custom pairs
        for img1 in scene_graph.keys():
            for img2 in scene_graph[img1]:
                image_pairs.append((img1, img2))
    
    return image_pairs


### FUNCTION TO MATCH A PAIR OF IMAGES
def Matcher(pair_range): 

    matches_dict = {}
    keypoints_dict = {}
    iteration = 0
    total_iterations = len(pair_range)

    # Matching a pair
    for pair in pair_range:
        img1_name = pair[0]
        img2_name = pair[1]
        
        print("\n")
        print("{} {}".format(img1_name, img2_name), end='\r')
        print("\n")
        # Retrieving and joining local features from tiles
        if tiling == True:
            kpts_1, desc_1, kpts_numb_1 = rearrangeKpts(img1_name, image_folder, desc_folder, colmap_desc_folder, matches_folder, tile_folder, local_feature)
            kpts_2, desc_2, kpts_numb_2 = rearrangeKpts(img2_name, image_folder, desc_folder, colmap_desc_folder, matches_folder, tile_folder, local_feature)
            
            # Storing keypoints in a dictionary
            if img1_name not in keypoints_dict.keys():
                keypoints_dict[img1_name] = cv2.KeyPoint_convert(kpts_1)
            if img2_name not in keypoints_dict.keys():
                keypoints_dict[img2_name] = cv2.KeyPoint_convert(kpts_2)
            
            # Brute-force on the pair
            opencv_matches = BruteForce.BrForce(desc_1, desc_2, check, matching_distance, cross_check, matching_strategy, print_debug=False, ratio_thresh=ratio_thresh)
            
            # Storing matches
            matches_matrix = np.zeros((len(opencv_matches), 2))

            for l in range(0,len(opencv_matches)):
                matches_matrix[l][0] = int(opencv_matches[l].queryIdx)
                matches_matrix[l][1] = int(opencv_matches[l].trainIdx)
                
            matches_dict["{} {}".format(img1_name, img2_name)] = matches_matrix
            iteration += 1
            print("ITERATIONS:\t\t\t{}/{}".format(iteration, total_iterations))
        
        
        elif tiling == False:
            if local_feature == "D2Net":
                kpts_1, desc_1, kpts_numb_1 = D2Net(img1_name, desc_folder, max_kpts_per_tile)
                kpts_2, desc_2, kpts_numb_2 = D2Net(img2_name, desc_folder, max_kpts_per_tile)

            elif local_feature == "RoRD":
                kpts_1, desc_1, kpts_numb_1 = RoRD(img1_name, desc_folder, max_kpts_per_tile)
                kpts_2, desc_2, kpts_numb_2 = RoRD(img2_name, desc_folder, max_kpts_per_tile)
            
            else:
                print("Other local features to be implemented ...")

            ## Convert keypoints in openCV format
            opencv_kpts_1 = []
            for i in range (0,kpts_1.shape[0]):
                opencv_kpts_1.append(cv2.KeyPoint(kpts_1[i][0],kpts_1[i][1],0,0))
            opencv_kpts_2 = []
            for i in range (0,kpts_2.shape[0]):
                opencv_kpts_2.append(cv2.KeyPoint(kpts_2[i][0],kpts_2[i][1],0,0))
            kpts_1 = opencv_kpts_1
            kpts_2 = opencv_kpts_2

            # Storing keypoints in a dictionary
            if img1_name not in keypoints_dict.keys():
                keypoints_dict[img1_name] = cv2.KeyPoint_convert(kpts_1)
            if img2_name not in keypoints_dict.keys():
                keypoints_dict[img2_name] = cv2.KeyPoint_convert(kpts_2)
            print(keypoints_dict)

            # Brute-force on the pair
            opencv_matches = BruteForce.BrForce(desc_1, desc_2, check, matching_distance, cross_check, matching_strategy, print_debug=False, ratio_thresh=ratio_thresh)

            # Storing matches
            matches_matrix = np.zeros((len(opencv_matches), 2))

            for l in range(0,len(opencv_matches)):
                matches_matrix[l][0] = int(opencv_matches[l].queryIdx)
                matches_matrix[l][1] = int(opencv_matches[l].trainIdx)
                
            matches_dict["{} {}".format(img1_name, img2_name)] = matches_matrix
            iteration += 1
            print("ITERATIONS:\t\t\t{}/{}".format(iteration, total_iterations))
            
    
    return keypoints_dict, matches_dict

### REARRANGE KEYPOINTS FROM TILES
def rearrangeKpts(  img1,
                    image_folder,
                    desc_folder,
                    colmap_desc_folder,
                    matches_folder,
                    tile_folder,
                    local_feature):
    
    image_list = os.listdir(image_folder)
    tile_list = os.listdir(tile_folder)
    desc_list = os.listdir(desc_folder)
    
    # Rearrange keypoints coordinates and descriptors to obtain an unique file for each image
    total_numb_kpts = 0

    for tile in tile_list:
        if img1[:-4] in tile:

            image_name_len = len(img1[:-4])
            tile_info = tile[image_name_len+1:-4]
            row, col, ox, oy, tw, th = tile_info.split("_")
            row, col, ox, oy, tw, th = int(row[1:]), int(col[1:]), int(ox[2:]), int(oy[2:]), int(tw[2:]), int(th[2:])
            
            # Import keypoints from file
            if local_feature == "LFNet":
                np_desc_path = Path("{}.npz".format(tile))
                abs_np_desc_path = desc_folder / np_desc_path
                with np.load(abs_np_desc_path) as data:
                    d = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (data[k] for k in data)))
                kp = d['keypoints']
                kp_numb = d['keypoints'].shape[0]
                total_numb_kpts += kp_numb
                desc = d['descriptors']
            
            elif local_feature == "KeyNet" or local_feature == "RootSIFT":

                np_kpt_path = Path("{}.kpt.npy".format(tile))
                abs_np_kpt_path = desc_folder / np_kpt_path
                np_dsc_path = Path("{}.dsc.npy".format(tile))
                abs_np_dsc_path = desc_folder / np_dsc_path

                kp = np.load(abs_np_kpt_path)
                desc = np.load(abs_np_dsc_path)
                kp_numb = kp.shape[0]
                total_numb_kpts += kp_numb
                
            elif local_feature == "photomatch":

                if tile[-3:] == 'jpg':
                    tile = tile[0:-3] + 'xml'
                
                tile_path = Path("{}".format(tile))
                absolute_tile_path = r"{}/{}".format(desc_folder,tile_path)

                fs = cv2.FileStorage(absolute_tile_path, cv2.FILE_STORAGE_READ)
                kpFromXML = fs.getNode('keypoints')
                kp_numb = kpFromXML.size()
                total_numb_kpts += kp_numb
                desc = fs.getNode('descriptors').mat()
                kp = np.array([0, 0])
                for i in range(0, kp_numb):
                    x = kpFromXML.at(i).at(0).real()
                    y = kpFromXML.at(i).at(1).real()
                    kp = np.vstack((kp, np.array([x, y])))
                kp = kp[1:, :]
                fs.release()
            
            elif local_feature == "D2Net":
                np_dsc_path = Path("{}.d2-net".format(tile))
                abs_np_dsc_path = desc_folder / np_dsc_path

                # Import D2Net keypoints and descriptors
                with np.load(abs_np_dsc_path) as data:
                    d = dict(zip(("keypoints","scores","descriptors"), (data[k] for k in data)))
                
                kp = d['keypoints']
                kp = kp[:max_kpts_per_tile, :2]
                kp_numb = kp.shape[0]
                desc = d['descriptors']
                desc = desc[:max_kpts_per_tile, :]
                total_numb_kpts += kp_numb


            else:
                print("Invalid local_feature parameter. Exit.")
                quit()
            
            # Translate keypoints coordinates
            translated_kpts = np.empty((kp_numb,2), dtype=float)
            for r in range(kp_numb):
                translated_kpts[r,0] = kp[r,0] + col * tw - col * ox
                translated_kpts[r,1] = kp[r,1] + row * th - row * oy
            
            # Stack keypoints in a unique file
            if row == 0 and col == 0:
                image_kps = translated_kpts
                image_desc = desc
            else:
                image_kps = np.concatenate((image_kps, translated_kpts), axis=0)
                image_desc = np.concatenate((image_desc, desc), axis=0)

    
    ## Convert keypoints in openCV format
    opencv_keypoints = []
    for i in range (0,image_kps.shape[0]):
        opencv_keypoints.append(cv2.KeyPoint(image_kps[i][0],image_kps[i][1],0,0))
    
    # Show keypoints on image
    #if INFO:
    #    img = cv2.imread(str(image_folder / Path(img1)))
    #    plt.figure(figsize=(10, 10))
    #    plt.title(f'Image {img1}')
    #    image_with_kpts = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0)
    #    plt.imshow(image_with_kpts)
    #    plt.show()
    
    return opencv_keypoints, image_desc, total_numb_kpts

### MAIN STARTS HERE
if __name__ == "__main__":
    
    image_list = os.listdir(image_folder)
    
    ### Generate image pairs according to the matching_approach
    print("\nGenerating image pairs according to the matching_approach '{}' ...".format(matching_approach))
    image_pairs_list = ImagePairs(matching_approach, image_list)
    if debug: print("matching_approach:\t", matching_approach), print("len(image_pairs_list):\t", len(image_pairs_list))
    
    ### Matching pairs
    # Matching all pairs with a multi threads approach
    image_pairs = np.array(image_pairs_list)
    pool_ranges = np.array_split(image_pairs, pool_N)
    
    print("\nMultithreading ranges:")
    for r in pool_ranges:
        print(r.shape)

    if multhreading == True:
        with Pool (pool_N) as p:
            ris = p.map(Matcher, pool_ranges) 
    
    elif multhreading == False:
        ris = Matcher(pool_ranges[0])
        ris = [ris] # for compatibility with the multithreading approach
        
    else:
        print("Error! Multithreading must be True or False ...")
        quit()
    
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


