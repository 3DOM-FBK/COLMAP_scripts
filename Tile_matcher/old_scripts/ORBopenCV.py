### ORB OPENCV
#
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM
# >python ORBopenCV.py -i1  C:/Users/Luscias/Desktop/buttare_subito/imgs/IMG_0515.jpg -i2 C:/Users/Luscias/Desktop/buttare_subito/imgs/IMG_0515.jpg -k 8000

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Convert LF-Net descriptors in openCV format
def ORBopenCV(image_path, n_kp_input):
    
    # Detect and Compute
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(n_kp_input) #n_kp_input
    opencv_keypoints, opencv_descriptors = orb.detectAndCompute(img, None)
    kp_numb = len(opencv_keypoints)   
            
    return opencv_keypoints, opencv_descriptors, kp_numb


# Main function
def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", "--Image1", help = "Input image1 path")
    parser.add_argument("-i2", "--Image2", help = "Input image2 path")
    parser.add_argument("-k", "--Keypoints_numb", help = "N keypoints")
    args = parser.parse_args()

    if args.Image1:
        print("Diplaying image1 path as: % s" % args.Image1)
    if args.Image2:
        print("Diplaying image2 path as: % s" % args.Image2)
    if args.Keypoints_numb:
        print("Diplaying number of keypoints: % s" % args.Keypoints_numb)
    
    image1_path = args.Image1
    image2_path = args.Image2
    n_kp_input = int(args.Keypoints_numb)
    
    # Show image with features
    img1 = cv2.imread(image1_path)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    
    img2 = cv2.imread(image2_path)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)    
    
    cv2.imshow('Image1', img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    cv2.imshow('Image2', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    opencv_keypoints1, opencv_descriptors1, kp_numb1 = ORBopenCV(image1_path, n_kp_input)
    
    opencv_keypoints2, opencv_descriptors2, kp_numb2 = ORBopenCV(image2_path, n_kp_input)
    
    image1 = cv2.drawKeypoints(img1,opencv_keypoints1,img1,flags=0)
    cv2.imshow('Image1', image1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    image2 = cv2.drawKeypoints(img2,opencv_keypoints2,img1,flags=0)
    cv2.imshow('Image2', image2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    print('Descriptors image1:  {}'.format(opencv_descriptors1.shape))
    print('Descriptors image2:  {}'.format(opencv_descriptors2.shape))
    print(opencv_descriptors1)
    print(opencv_descriptors2)
    print(opencv_descriptors1[0][0])
    print(type(opencv_descriptors1[0][0]))
    print(len(opencv_keypoints1))
    print(len(opencv_keypoints2))
    
    # Brute-Force
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(opencv_descriptors1, opencv_descriptors2)
    matches = sorted(matches, key = lambda x:x.distance)
    img_matches = cv2.drawMatches(img1,opencv_keypoints1,img2,opencv_keypoints2,matches[:200],None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    plt.imshow(img_matches),plt.show()

# driver function 
if __name__=="__main__": 
    main()