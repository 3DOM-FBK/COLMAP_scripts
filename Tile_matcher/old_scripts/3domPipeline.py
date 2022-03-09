### 3DOM PIPELINE

### Create a conda environment named opencv2
# In fase di installazione aprire anaconda prompt come amministratore
# >conda create --name opencv
# >conda activate opencv
# >conda install -c conda-forge opencv
# >conda install -c anaconda pandas
# >conda install -c conda-forge matplotlib
# >conda deactivate opencv

### Utilizzo
# Set images and options in config.py
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM
# >python 3domPipeline.py



# Libraries 
print('\nImporting libraries ...')
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Import other scripts
print('Importing other scripts and variables ...')
from config import image_set
from config import desc_path_folder
from config import image_path_folder
from config import converted_desc_path_folder
from config import print_debug
from config import descriptor
from config import matching
from config import check
from config import nmatches
from config import crossCheck_bool
from config import raw_matches_folder
from config import gcp_path_folder
from config import gcp_bool
from config import res_factor
from config import n_kp_input_SIFT
from config import n_kp_input_ORB
from config import matching_distance
from config import ratio_thresh_LRT
from config import matching_strategy
import SuperPoint2openCV
import LFNet2openCV
import ASLFeat2openCV
import R2D2openCV
import KeyNet2openCV
import D2NetopenCV
import photomatch2openCV
import BruteForce
import SIFTopenCV
import ORBopenCV

print('\n')
print('Number of images:\t\t\t{}'.format(len(image_set)))
print('Image dataset:\t\t\t\t{}'.format(image_set))

print('\nI/O folders:')
print('Path to images folder:\t\t\t{}'.format(image_path_folder))
print('Path to descriptors folder:\t\t{}'.format(desc_path_folder))
print('Path to converted descriptors:\t\t{}'.format(converted_desc_path_folder))
print('Path to raw-matches folder:\t\t{}'.format(raw_matches_folder))

print('\nOptions :')
print('Descriptor type :\t\t\t{}'.format(descriptor))
print('Use *** GCP *** :\t\t\t{}'.format(gcp_bool))
print('Image ratio (img/GCPimg) :\t\t{:.3f}'.format(res_factor))
print('Matcher :\t\t\t\t{}'.format(matching))
print('Matching distance : \t\t\t{}'.format(matching_distance))
print('Cross-Check :\t\t\t\t{}'.format(crossCheck_bool))
print('matching_strategy : \t\t\t{}'.format(matching_strategy))
print('Lowe Ratio Test :\t\t\t{}'.format(check))
print('Lowe Ratio Test treshold : \t\t{}'.format(ratio_thresh_LRT))
print('Show DEBUG:\t\t\t\t{}'.format(print_debug))
print('')

user_input = input('Do you want to continue? y/n   ')
if user_input == 'n' :
    quit()


# GCP management
if gcp_bool == True :
    gcp_set = {}
    gcp_global_key = -1
    print('GCP dictionary:')
    
    # Import GCP from text and store them to dictionary
    for k in range(0, len(image_set)) :
        gcp_path = '{}/{}.txt'.format(gcp_path_folder,image_set[k]) 
        try :
            with open(gcp_path) as data:
                for line in data:
                    gcp_global_key = gcp_global_key + 1
                    gcp_id, x, y, kp_id, no = line.split(' ', 4)
                    x = '{:.6f}'.format(int(x) * res_factor)
                    y = '{:.6f}'.format(int(y) * res_factor)
                    gcp_set[gcp_global_key] = { 'image':image_set[k], 'gcp_id' : gcp_id, 'x' : x, 'y' : y, 'kp_id' : kp_id }
                    print(gcp_set[gcp_global_key])
                    
                    # Show GCP location on images
                    if print_debug == True :
                        img = cv2.imread(os.path.join(image_path_folder,image_set[k]))
                        cv2.imshow('image', img)
                        cv2.circle(img,(np.float32(x),np.float32(y)),0,(0,0,255),2)
                        cv2.circle(img,(np.float32(x),np.float32(y)),10,(0,0,255),2)
                        cv2.circle(img,(np.float32(x),np.float32(y)),50,(0,0,255),2)
                        cv2.circle(img,(np.float32(x),np.float32(y)),100,(0,0,255),2)
                        cv2.imshow('image', img)
                        cv2.waitKey(0)
                        cv2.destroyAllWindows()
                    
                    
        except: print('{} GCP do not exist. It is not an error.'.format(gcp_path))
    print('')
    
    
    

    # Extract number of keypoints from descriptors file to assign an ID to GCPs bigger than the biggest keypoint ID :  
    if descriptor == 'LFNet' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = LFNet2openCV.LFNet2openCV(desc_path)
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'ASLFeat' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = ASLFeat2openCV.ASLFeat2openCV(desc_path)
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'R2D2' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = R2D2openCV.R2D2openCV(desc_path)
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])  
            
    elif descriptor == 'D2Net' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = D2NetopenCV.D2NetopenCV(desc_path)
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])   

    elif descriptor == 'KeyNet' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = KeyNet2openCV.KeyNet2openCV(desc_path)
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'SIFTopenCV' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = SIFTopenCV.SIFTopenCV('{}/{}'.format(image_path_folder,gcp_set[n]['image']),n_kp_input_SIFT)
            print('n keypoints {}'.format(len(opencv_keypoints)))
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'SuperPoint' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = SuperPoint2openCV.SuperPoint2openCV(desc_path)
            print('n keypoints {}'.format(len(opencv_keypoints)))
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'ORBopenCV' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = ORBopenCV.ORBopenCV('{}/{}'.format(image_path_folder,gcp_set[n]['image']),n_kp_input_ORB)
            print('n keypoints {}'.format(len(opencv_keypoints)))
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            
    elif descriptor == 'PhotoMatch3DOM' :
        for n in gcp_set.keys() :
            desc_path = os.path.join(desc_path_folder, gcp_set[n]['image'])
            opencv_keypoints, opencv_descriptors, kp_numb = photomatch2openCV.PhMatch2openCV(desc_path)
            print('n keypoints {}'.format(len(opencv_keypoints)))
            gcp_set[n]['kp_id'] = int(gcp_set[n]['kp_id']) + kp_numb - 1
            print(gcp_set[n])
            

    else :
        print('Insert one of these descriptors: PhotoMatch3DOM, LFNet, ASLFeat, R2D2, KeyNet, , SIFTopenCV, ORBopenCV')
        quit()


def image_show(img_path,img_name):
    img = cv2.imread(img_path)
    plt.figure(figsize=(10, 10))
    plt.title(img_name)
    plt.imshow(img)
    plt.show()
    return img

# Create raw matches file
path_raw_matches_file = os.path.join(raw_matches_folder,'raw_matches.txt')
raw_matches_file = open(path_raw_matches_file,"w")

# Loop on image dataset for matching (Brute-Force, FLANN)
print('Match images: {}'.format(matching))
for cycle1 in range (0, len(image_set)-1) :
    image_path_1 = os.path.join(image_path_folder,image_set[cycle1])
    if print_debug == True : image_1 = image_show(image_path_1,image_path_1)
    desc_path_1 = os.path.join(desc_path_folder,image_set[cycle1])
    
    # Convert own descriptors in openCV format
    if descriptor == 'LFNet':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = LFNet2openCV.LFNet2openCV(desc_path_1)
    elif descriptor == 'ASLFeat':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = ASLFeat2openCV.ASLFeat2openCV(desc_path_1)
    elif descriptor == 'R2D2':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = R2D2openCV.R2D2openCV(desc_path_1)
    elif descriptor == 'D2Net':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = D2NetopenCV.D2NetopenCV(desc_path_1)
    elif descriptor == 'KeyNet':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = KeyNet2openCV.KeyNet2openCV(desc_path_1)
    elif descriptor == 'SIFTopenCV':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = SIFTopenCV.SIFTopenCV(image_path_1,n_kp_input_SIFT)  
    elif descriptor == 'SuperPoint':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = SuperPoint2openCV.SuperPoint2openCV(desc_path_1)        
    elif descriptor == 'ORBopenCV':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = ORBopenCV.ORBopenCV(image_path_1,n_kp_input_ORB)   
    elif descriptor == 'PhotoMatch3DOM':
        opencv_keypoints_1, opencv_descriptors_1, kp_numb_1 = photomatch2openCV.PhMatch2openCV(desc_path_1)
    else :
        print('Insert one of these descriptors: PhotoMatch3DOM, LFNet, ASLFeat, R2D2, KeyNet, , SIFTopenCV, ORBopenCV')
        quit()
    
    # Print image with features    
    if print_debug == True :
        plt.figure(figsize=(10, 10))
        plt.title('Image 1')
        image1 = cv2.drawKeypoints(image_1,opencv_keypoints_1,image_1,color=[255,0,0],flags=0)    
        plt.imshow(image1); plt.show()
    
    # Export keypoints for COLMAP elaborations
    raw_keypoints_path = '{}/{}.txt'.format(converted_desc_path_folder,image_set[cycle1])
    if gcp_bool == False :
        BruteForce.ColmapKeypoints(raw_keypoints_path, opencv_keypoints_1)
        
    elif gcp_bool == True :
        gcp_numb = 0
        for key in gcp_set.keys():
            if gcp_set[key]['image'] == image_set[cycle1] :  
                gcp_numb = gcp_numb + 1
        kp = opencv_keypoints_1
        raw_keypoints_file = open(raw_keypoints_path,"w")
        raw_keypoints_file.write('{} 128\n'.format(len(kp)+gcp_numb))
        for j in range (0,len(kp)):
            raw_keypoints_file.write('{:.6f} {:.6f} 0.000000 0.000000\n'.format(cv2.KeyPoint_convert(kp)[j][0],cv2.KeyPoint_convert(kp)[j][1])) 
        
        
        for key in gcp_set.keys():
            if gcp_set[key]['image'] == image_set[cycle1] :       
                raw_keypoints_file.write('{:.6f} {:.6f} 0.000000 0.000000\n'.format(float(gcp_set[key]['x']), float(gcp_set[key]['y'])))        
        raw_keypoints_file.close()
    

    for cycle2 in range (cycle1+1, len(image_set)) :
        print('{} {}'.format(image_set[cycle1],image_set[cycle2]))
        image_path_2 = os.path.join(image_path_folder,image_set[cycle2])
        if print_debug == True : image_2 = image_show(image_path_2,image_path_2)
        desc_path_2 = os.path.join(desc_path_folder,image_set[cycle2])
        # Convert LF-Net descriptors in openCV format
        if descriptor == 'LFNet':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = LFNet2openCV.LFNet2openCV(desc_path_2)
        elif descriptor == 'ASLFeat':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = ASLFeat2openCV.ASLFeat2openCV(desc_path_2)
        elif descriptor == 'R2D2':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = R2D2openCV.R2D2openCV(desc_path_2)
        elif descriptor == 'D2Net':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = D2NetopenCV.D2NetopenCV(desc_path_2)
        elif descriptor == 'KeyNet':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = KeyNet2openCV.KeyNet2openCV(desc_path_2)
        elif descriptor == 'SIFTopenCV':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = SIFTopenCV.SIFTopenCV(image_path_2,n_kp_input_SIFT)  
        elif descriptor == 'SuperPoint':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = SuperPoint2openCV.SuperPoint2openCV(desc_path_2)            
        elif descriptor == 'ORBopenCV':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = ORBopenCV.ORBopenCV(image_path_2,n_kp_input_ORB)    
        elif descriptor == 'PhotoMatch3DOM':
            opencv_keypoints_2, opencv_descriptors_2, kp_numb_2 = photomatch2openCV.PhMatch2openCV(desc_path_2) 
        else :
            print('Insert one of these descriptors: PhotoMatch3DOM, LFNet, ASLFeat, R2D2, D2Net, KeyNet, , SIFTopenCV, ORBopenCV')
            quit()
            
        # Print image with features
        if print_debug == True :
            plt.figure(figsize=(10, 10))
            plt.title('Image 2')
            image2 = cv2.drawKeypoints(image_2,opencv_keypoints_2,image_2,color=[255,0,0],flags=0)    
            plt.imshow(image1); plt.show()
            
        # Convert descriptors in type LIKE_SIFT (int [0,255])
        #opencv_descriptors_1 = np.absolute(opencv_descriptors_1) * 512
        #opencv_descriptors_2 = np.absolute(opencv_descriptors_2) * 512
        #aggiungere troncamento!!!
            
        # DEBUG on keypoints and features
               
        if print_debug == True :
            print('Shape opencv_descriptors_1: {}'.format(opencv_descriptors_1.shape))
            print('Shape opencv_descriptors_2: {}'.format(opencv_descriptors_2.shape))
            print('opencv_descriptors_1[0]: \n{}'.format(opencv_descriptors_1[0]))
            print('opencv_descriptors_1[1]: \n{}'.format(opencv_descriptors_1[1]))
            print('opencv_descriptors_2[0]: \n{}'.format(opencv_descriptors_2[0]))
            print('opencv_descriptors_2[1]: \n{}'.format(opencv_descriptors_2[1]))
            

        # Brute-Force Matching -> matches in openCV format
                
        if matching == 'BruteForce' : 
            matches = BruteForce.BrForce(opencv_descriptors_1,
                                        opencv_descriptors_2,
                                        check,
                                        matching_distance,
                                        crossCheck_bool,
                                        matching_strategy,
                                        print_debug,
                                        ratio_thresh = ratio_thresh_LRT
                                        )

        else :
            print('FLANN or other matching strategies are not implemented yet ...')
                                       
        #elif matching == 'FLANN' :
        #   matches = ...
                                        
        if print_debug == True : 
            BruteForce.ShowMatches(image_1, opencv_keypoints_1, image_2, opencv_keypoints_2, matches, nmatches)
        
        
        # Export keypoints for COLMAP elaborations
        if cycle1 == len(image_set)-2 and cycle2 == len(image_set)-1:
            raw_keypoints_path = '{}/{}.txt'.format(converted_desc_path_folder,image_set[cycle2])
            
            if gcp_bool == False :
                BruteForce.ColmapKeypoints(raw_keypoints_path, opencv_keypoints_2)
            
            elif gcp_bool == True :
                gcp_numb = 0
                for key in gcp_set.keys():
                    if gcp_set[key]['image'] == image_set[cycle2] :  
                        gcp_numb = gcp_numb + 1
                kp = opencv_keypoints_2
                raw_keypoints_file = open(raw_keypoints_path,"w")
                raw_keypoints_file.write('{} 128\n'.format(len(kp)+gcp_numb))
                for j in range (0,len(kp)):
                    raw_keypoints_file.write('{:.6f} {:.6f} 0.000000 0.000000\n'.format(cv2.KeyPoint_convert(kp)[j][0],cv2.KeyPoint_convert(kp)[j][1])) 
                
                
                for key in gcp_set.keys():
                    if gcp_set[key]['image'] == image_set[cycle2] :
                        raw_keypoints_file.write('{:.6f} {:.6f} 0.000000 0.000000\n'.format(float(gcp_set[key]['x']), float(gcp_set[key]['y'])))       
                raw_keypoints_file.close() 

   
     
        # Write matches in a txt file
        BruteForce.WriteRawMatches(raw_matches_file,image_set[cycle1],image_set[cycle2],matches)
        if gcp_bool == False : raw_matches_file.write('\n')
        
        if gcp_bool == True :
            for j in gcp_set.keys():
                if gcp_set[j]['image'] == image_set[cycle1] :
                    match1 = gcp_set[j]['kp_id']
                    
                    
                    for m in gcp_set.keys():
                        
                        if gcp_set[m]['image'] == image_set[cycle2] and gcp_set[m]['gcp_id'] == gcp_set[j]['gcp_id'] :
                            match2 = gcp_set[m]['kp_id']
                            raw_matches_file.write('{} {}\n'.format(match1, match2))
                            print(gcp_set[m]['kp_id'])
                            print(kp_numb_2)

        raw_matches_file.write('\n')
                


raw_matches_file.close()

print('')
#for k in gcp_set.keys() :
#    print(gcp_set[k])