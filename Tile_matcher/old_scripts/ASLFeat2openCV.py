### KEYPOINTS CONVERTER ASLFeat -> OPENCV FORMAT
#
# >python ASLFeat2openCV.py -i F:/3DOM/VENTIMIGLIA/SUBMODEL/model_1500x1000/ASLFeat/desc/IMG_9001.jpg -g F:/3DOM/VENTIMIGLIA/SUBMODEL/model_1500x1000/imgs_1500x1000/IMG_9001.jpg

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Convert LF-Net descriptors in openCV format
def ASLFeat2openCV(desc_path):
    
    # Import keypoints and descriptors from files .feat and .desc
    desc_path = desc_path.replace('.jpg','')
    kp = np.loadtxt('{}.feat'.format(desc_path), dtype=float, delimiter=",")
    opencv_descriptors = np.loadtxt('{}.desc'.format(desc_path), dtype=float, delimiter=",")
    opencv_descriptors = np.asarray(opencv_descriptors, np.float32)
    kp_numb = kp.shape[0]
    
    # Convert keypoints in openCV format
    opencv_keypoints = []
    for i in range (0,kp.shape[0]):
        opencv_keypoints.append(cv2.KeyPoint(kp[i][0],kp[i][1],0,0))
    
    return opencv_keypoints, opencv_descriptors, kp_numb


    #np_desc_path = "{}.npz".format(desc_path)
    ## Import LFNet keypoints and descriptors
    #with np.load(np_desc_path) as data:
    #    d = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (data[k] for k in data)))
    #kp = d['keypoints']
    #kp_numb = d['keypoints'].shape[0]
    #opencv_descriptors = d['descriptors']
    #
    ## Convert keypoints in openCV format
    #opencv_keypoints = []
    #for i in range (0,kp.shape[0]):
    #    opencv_keypoints.append(cv2.KeyPoint(kp[i][0],kp[i][1],0,0))
    #    
    #return opencv_keypoints, opencv_descriptors, kp_numb


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
    
    opencv_keypoints, opencv_descriptors, kp_numb = ASLFeat2openCV(desc_path)
    
    image = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
    plt.imshow(image)
    plt.show()
    
    print('Number of Keypoints:  {}'.format(len(opencv_keypoints)))
    print('Descriptors shape:  {}'.format(opencv_descriptors.shape))
    print('Descriptor ID 0: \n{}'.format(opencv_descriptors[0]))
    print('Descriptor ID 1: \n{}'.format(opencv_descriptors[1]))


# Driver function
if __name__=="__main__": 
    main()