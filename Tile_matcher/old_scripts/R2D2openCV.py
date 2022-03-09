### KEYPOINTS CONVERTER LF-NET -> OPENCV FORMAT
#
# >python r2d2openCV.py -i F:/3DOM/VENTIMIGLIA/SUBMODEL/model_1500x1000/R2D2/desc/IMG_9001.jpg -g F:/3DOM/VENTIMIGLIA/SUBMODEL/model_1500x1000/imgs_1500x1000/IMG_9001.jpg

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Convert LF-Net descriptors in openCV format
def R2D2openCV(desc_path):

    np_desc_path = "{}.r2d2".format(desc_path)
    # Import R2D2 keypoints and descriptors
    with np.load(np_desc_path) as data:
        d = dict(zip(("resolution","keypoints","descriptors","scores"), (data[k] for k in data)))
    kp = d['keypoints']
    kp_numb = d['keypoints'].shape[0]
    opencv_descriptors = d['descriptors']
    
    # Convert keypoints in openCV format
    opencv_keypoints = []
    for i in range (0,kp.shape[0]):
        opencv_keypoints.append(cv2.KeyPoint(kp[i][0],kp[i][1],0,0))
        
    return opencv_keypoints, opencv_descriptors, kp_numb


# Main function
def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = "Input LFNet descriptor path without .npz extension")
    parser.add_argument("-g", "--Image", help = "Input image path")
    args = parser.parse_args()

    if args.Image:
        print("Diplaying image path as: % s" % args.Image)
    if args.Input:
        print("Diplaying image descriptors path as: % s" % args.Input)
    
    desc_path = args.Input
    image_path = args.Image
    
    # Show image with features
    img = cv2.imread(image_path)
    plt.figure(figsize=(10, 10))
    plt.title('Image 1')
    plt.imshow(img)
    plt.show()
    
    opencv_keypoints, opencv_descriptors, kp_numb = R2D2openCV(desc_path)
    
    image = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
    plt.imshow(image)
    plt.show()
    
    print('Descriptors:  {}'.format(opencv_descriptors.shape))
    print(opencv_descriptors)


# driver function 
if __name__=="__main__": 
    main()