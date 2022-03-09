### KEYPOINTS CONVERTER PHOTOMATCH -> OPENCV FORMAT
#
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM
# >python photomatch2openCV.py -i C:/Users/Luscias/Desktop/prova_photomatch/export/DSC_4317.xml -g C:/Users/Luscias/Desktop/prova_photomatch/imgs_1500x1000/DSC_4317.jpg

# Libraries 
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Convert descriptors in openCV format
def PhMatch2openCV(desc_path):

    if desc_path[-3:] == 'jpg':
        desc_path = desc_path[0:-3] + 'xml'
        
    print(desc_path)

    # Import keypoints and descriptors
    fs = cv2.FileStorage(desc_path, cv2.FILE_STORAGE_READ)
    kpFromXML = fs.getNode('keypoints')
    kp_numb = kpFromXML.size()
    opencv_descriptors = fs.getNode('descriptors').mat()
    opencv_keypoints = []
    for i in range(0, kp_numb):
        x = kpFromXML.at(i).at(0).real()
        y = kpFromXML.at(i).at(1).real()
        opencv_keypoints.append(cv2.KeyPoint(x, y, 0, 0))
    print('1 keypoint:  {}'.format(kpFromXML.at(0).at(0).real()), kpFromXML.at(0).at(1).real())
    print('2 keypoint:  {}'.format(kpFromXML.at(1).at(0).real()), kpFromXML.at(1).at(1).real())
    fs.release()
    
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
    
    opencv_keypoints, opencv_descriptors, kp_numb = PhMatch2openCV(desc_path)
    
    image = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
    plt.imshow(image)
    plt.show()
    
    print('1 keypoint:  {}'.format(opencv_keypoints[0]))
    print('2 keypoint:  {}'.format(opencv_keypoints[1]))
    print('Descriptors:  {}'.format(opencv_descriptors.shape))
    print('1 descriptor:')
    print(opencv_descriptors[0])
    print('2 descriptor:')
    print(opencv_descriptors[1])


# driver function 
if __name__=="__main__": 
    main()