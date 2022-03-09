### SIFT OPENCV
#
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM
# >python SIFTopenCV.py -g  F:/3DOM/VENTIMIGLIA/SUBMODEL/model_1500x1000/imgs_1500x1000/IMG_9001.jpg -k 8000

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Convert LF-Net descriptors in openCV format
def SIFTopenCV(image_path, n_kp_input):
    
    # Detect and Compute
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sift = cv2.SIFT_create(n_kp_input)
    opencv_keypoints, opencv_descriptors = sift.detectAndCompute(img, None)
    kp_numb = len(opencv_keypoints)   
            
    return opencv_keypoints, opencv_descriptors, kp_numb


# Main function
def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--Image", help = "Input image path")
    parser.add_argument("-k", "--Keypoints_numb", help = "N keypoints")
    args = parser.parse_args()

    if args.Image:
        print("Diplaying image path as: % s" % args.Image)
    if args.Keypoints_numb:
        print("Diplaying number of keypoints: % s" % args.Keypoints_numb)
    
    image_path = args.Image
    n_kp_input = int(args.Keypoints_numb)
    
    # Show image with features
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow('Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    opencv_keypoints, opencv_descriptors, kp_numb = SIFTopenCV(image_path, n_kp_input)
    
    image = cv2.drawKeypoints(img,opencv_keypoints,img,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    
    print('Descriptors:  {}'.format(opencv_descriptors.shape))
    print(opencv_descriptors)
    print(len(opencv_keypoints))


# driver function 
if __name__=="__main__": 
    main()