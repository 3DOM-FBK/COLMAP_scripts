### BRUTE-FORCE OPENCV2
#
# >python BruteForce.py -i C:/Users/Luscias/Desktop/3DOM/07_LFNet/provaGCP/desc_LFNet/LEO_8588_acr.jpg.npz -g C:/Users/Luscias/Desktop/3DOM/07_LFNet/provaGCP/imgs/LEO_8588_acr.jpg

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os


# Show matches
def ShowMatches(img1, kp1, img2, kp2, matches, nmatches = 100000):
    img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2 ,matchColor=[0,255,0], flags=2)   # Show top nmatches matches
    plt.figure(figsize=(16, 16))
    plt.title('img_matches')
    plt.imshow(img_matches); plt.show()

# Brute-Force openCV2
def BrForce(des1, des2, check, matching_distance, crossCheck_bool, matching_strategy, print_debug = True, ratio_thresh=0.8):
    if check == 'without_Lowe_ratio_test' and matching_distance=='L2':
        print('Ratio Treshold: {}'.format(ratio_thresh))
        bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck_bool)
        matches = bf.match(des1,des2)
        #matches = sorted(matches, key = lambda x: x.distance)   # Sort matches by distance.  Best come first.

        if print_debug == True :
            print('type(matches) : '), print(type(matches))
            print('shape(matches) : '), print(len(matches))
            print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
            print(matches[0].queryIdx)
            print(matches[0].trainIdx)
            print(matches[0].distance)

        return matches
            
    elif check == 'without_Lowe_ratio_test' and matching_distance=='NORM_HAMMING':

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=crossCheck_bool)
        matches = bf.match(des1,des2)

        if print_debug == True :
            print('type(matches) : '), print(type(matches))
            print('shape(matches) : '), print(len(matches))
            print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
            print(matches[0].queryIdx)
            print(matches[0].trainIdx)
            print(matches[0].distance)

        return matches
    
    elif check == 'Lowe_ratio_test' and matching_distance=='L2':
    
        print('check: {}'.format(check))
        print('matching_distance: {}'.format(matching_distance))
        print('matching_strategy: {}'.format(matching_strategy))
        print('ratio_thresh: {}'.format(ratio_thresh))

        bf = cv2.BFMatcher(cv2.NORM_L2, False)

        # Ratio Test
        def ratio_test(matches, ratio_thresh):
            prefiltred_matches = []
            for m,n in matches:
                #print('m={} n={}'.format(m,n))
                if m.distance < ratio_thresh * n.distance:
                    prefiltred_matches.append(m)
            return prefiltred_matches
        
        if matching_strategy == 'unidirectional':
            matches01 = bf.knnMatch(des1,des2,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            return good_matches01
            
        elif matching_strategy == 'intersection':
            matches01 = bf.knnMatch(des1,des2,k=2)
            matches10 = bf.knnMatch(des2,des1,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            good_matches10 = ratio_test(matches10, ratio_thresh)
            good_matches10_ = {(m.trainIdx, m.queryIdx) for m in good_matches10}
            prefiltred_matches = [m for m in good_matches01 if (m.queryIdx, m.trainIdx) in good_matches10_]
            return prefiltred_matches
            
        elif matching_strategy == 'union':
            matches01 = bf.knnMatch(des1,des2,k=2)
            matches10 = bf.knnMatch(des2,des1,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            good_matches10 = ratio_test(matches10, ratio_thresh)
            good_matches10_ = {(m.trainIdx, m.queryIdx) for m in good_matches10}
            other_matches = [m for m in good_matches01 if not (m.queryIdx, m.trainIdx) in good_matches10_]
            prefiltred_matches = good_matches10 + other_matches
            return prefiltred_matches
            
    elif check == 'Lowe_ratio_test' and matching_distance=='NORM_HAMMING':
    
        print('check: {}'.format(check))
        print('matching_distance: {}'.format(matching_distance))
        print('matching_strategy: {}'.format(matching_strategy))
        print('ratio_thresh: {}'.format(ratio_thresh))
        
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, False)

        # Ratio Test
        def ratio_test(matches, ratio_thresh):
            prefiltred_matches = []
            for m,n in matches:
                #print('m={} n={}'.format(m,n))
                if m.distance < ratio_thresh * n.distance:
                    prefiltred_matches.append(m)
            return prefiltred_matches
        
        if matching_strategy == 'unidirectional':
            matches01 = bf.knnMatch(des1,des2,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            return good_matches01
            
        elif matching_strategy == 'intersection':
            matches01 = bf.knnMatch(des1,des2,k=2)
            matches10 = bf.knnMatch(des2,des1,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            good_matches10 = ratio_test(matches10, ratio_thresh)
            good_matches10_ = {(m.trainIdx, m.queryIdx) for m in good_matches10}
            prefiltred_matches = [m for m in good_matches01 if (m.queryIdx, m.trainIdx) in good_matches10_]
            return prefiltred_matches
            
        elif matching_strategy == 'union':
            matches01 = bf.knnMatch(des1,des2,k=2)
            matches10 = bf.knnMatch(des2,des1,k=2)
            good_matches01 = ratio_test(matches01, ratio_thresh)
            good_matches10 = ratio_test(matches10, ratio_thresh)
            good_matches10_ = {(m.trainIdx, m.queryIdx) for m in good_matches10}
            other_matches = [m for m in good_matches01 if not (m.queryIdx, m.trainIdx) in good_matches10_]
            prefiltred_matches = good_matches10 + other_matches
            return prefiltred_matches
  
    
# Write raw matches in a txt file
def WriteRawMatches(raw_matches_file,imageID_1,imageID_2,matches):
                 
    raw_matches_file.write('{} {}\n'.format(imageID_1,imageID_2))
    for j in range (0,len(matches)):
        #print('{} {} {}'.format(matches[j].queryIdx,matches[j].trainIdx,matches[j].distance))
        raw_matches_file.write('{} {}\n'.format(matches[j].queryIdx,matches[j].trainIdx))
    #raw_matches_file.write('\n')
    
    
# Prepare keypoints for COLMAP
def ColmapKeypoints(raw_keypoints_path, kp):

    raw_keypoints_file = open(raw_keypoints_path,"w")
    raw_keypoints_file.write('{} 128\n'.format(len(kp)))
    for j in range (0,len(kp)):
        raw_keypoints_file.write('{:.6f} {:.6f} 0.000000 0.000000\n'.format(cv2.KeyPoint_convert(kp)[j][0],cv2.KeyPoint_convert(kp)[j][1]))
    raw_keypoints_file.close()
