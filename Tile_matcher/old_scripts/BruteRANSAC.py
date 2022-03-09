### INSTLLAZIONE DELL'AMBIENTE PYTHON CON CONDA
# Create a conda environment named opencv2
# In fase di installazione aprire anaconda prompt come amministratore
# >conda create --name opencv
# >conda activate opencv
# >conda install -c conda-forge opencv
# >conda install -c anaconda pandas
# >conda install -c conda-forge matplotlib
# >conda deactivate opencv
#
# Tutorial - Image Feature Extraction and Matching (https://www.kaggle.com/wesamelshamy/tutorial-image-feature-extraction-and-matching)
# Brute Force - https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html
# https://stackoverflow.com/questions/39940766/bfmatcher-match-in-opencv-throwing-error
#
### RUN THE SCRIPT
# >conda activate opencv
# >cd <script directory>

import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import os

# Versione OpenCV 4.5.1
print('Versione OpenCV installata :')
print(cv2.__version__)

# INPUT

image_set = []
### Specifica le immagini nome per nome
#image_set = ["_DSC5588_1.jpg","_DSC5589_1.jpg","_DSC5590_1.jpg"] # set di immagini da elaborare

### Oppure utilizza un ciclo
#Primo dataset
for n in range(9001,9006):
    image_set.append("IMG_{placeholder}.jpg".format(placeholder = n)) 
#Secondo dataset
for n in range(8540,8566):
    image_set.append("LEO_{placeholder}_acr.jpg".format(placeholder = n)) 
#Terzo dataset
for n in range(8585,8611):
    image_set.append("LEO_{placeholder}_acr.jpg".format(placeholder = n)) 
#Quarto dataset
for n in range(9065,9072):
    image_set.append("IMG_{placeholder}.jpg".format(placeholder = n)) 



print("image_set :")
print(image_set)

user_input = input('Continuare? s/n   ')
if user_input == 'n' :
    quit()


### I/O FOLDERS :
dataset_path = 'F:/3DOM/DATASETS/20miglia_submodel/LFNet_2500pix/all_imgs'    # IMAGES PATH
descriptors_path = 'F:/3DOM\DATASETS/20miglia_submodel/LFNet_2500pix/all_desc_from_LFNet'    # DESCRIPTORS PATH
raw_keypoints_path = 'F:/3DOM/DATASETS/20miglia_submodel/LFNet_2500pix/all_raw_keypoints'
path_raw_matches_file = 'F:/3DOM/DATASETS/20miglia_submodel/LFNet_2500pix/all_raw_matches/raw_matches_file.txt'

### ALTRI PARAMETRI :
nmatches = 100000
MIN_MATCH_COUNT = 15
ratio_threshold_value = 0.8
matches_verification = "crossCheck" # "crossCheck" or "Lowe_ratio_test"
detector_and_descriptor = "LFNet_features"  # Choose "SIFT" or "ORB" or "R2D2_features" or "LFNet_features"
crossCheck_bool = True # Parametro utilizzato solo se si è scelto : matches_verification = "crossCheck"
like_SIFT = False
print_report = False
DEBUG = False
create_raw_matches_file = True
RANSAC = False


###########################################################################
###########################################################################
###########################################################################

raw_matches_file = open(path_raw_matches_file,"w")

for cycle1 in range (0, len(image_set)-1) :
    image_1 = image_set[cycle1]
    desc_1 = os.path.join('{}.npz'.format(image_1))
    for cycle2 in range (cycle1+1, len(image_set)) :
        print('{} {}'.format(image_set[cycle1], image_set[cycle2]))
        image_2 = image_set[cycle2]
        desc_2 = os.path.join('{}.npz'.format(image_2))


        
        path_raw_keypoints_img1 = os.path.join(raw_keypoints_path,'{}.txt'.format(image_1))
        path_raw_keypoints_img2 = os.path.join(raw_keypoints_path,'{}.txt'.format(image_2))



        orb = cv2.ORB_create()
        sift = cv2.SIFT_create() #sift = cv2.xfeatures2d.SIFT_create()


        det_and_desc_library = {
            "ORB" : orb,
            "SIFT" : sift
        }


        def image_detect_and_compute(detector,folder_path,img_name):
            img = cv2.imread(os.path.join(dataset_path, img_name),cv2.IMREAD_GRAYSCALE)
            kp, des = detector.detectAndCompute(img, None)
            return img, kp, des
    
    
        if detector_and_descriptor == "ORB" or detector_and_descriptor == "SIFT" :
            img1, kp1, des1 = image_detect_and_compute(det_and_desc_library[detector_and_descriptor],dataset_path,image_1)
            img2, kp2, des2 = image_detect_and_compute(det_and_desc_library[detector_and_descriptor],dataset_path,image_2)
            print('kp1 e kp2 type = '), print(type(kp1))
            print('des1 e des2 type = '), print(type(des1))
            
            # Plot img1 with features
            plt.figure(figsize=(10, 10))
            plt.title('Interest Points')
            image = cv2.drawKeypoints(img1,kp1,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS) # For Python API, flags are modified as cv.DRAW_MATCHES_FLAGS_DEFAULT, cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
            plt.imshow(image); plt.show()
            converted_keypoints = cv2.KeyPoint_convert(kp1)
    
            print(type(converted_keypoints))
            print('Keypoint1 1 :'), print(converted_keypoints[0])
            print('Keypoint1 2 :'), print(converted_keypoints[1])
            print('Keypoint shape :'), print(converted_keypoints.shape)
            print('Descriptor 1'), print(des1)
            print('Descriptor 2'), print(des2)
            print('Descriptor1 shape :'), print(des1.shape)
            print('Descriptor2 shape :'), print(des2.shape)
    
            # Brute Force
            bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
            matches = bf.match(des1,des2)
            matches = sorted(matches, key = lambda x: x.distance) # Sort matches by distance.  Best come first.
    
            img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2, flags=2) # Show top 10 matches
            plt.figure(figsize=(16, 16))
            plt.title('Inserire Titolo')
            plt.imshow(img_matches); plt.show()
    
        elif detector_and_descriptor == "LFNet_features" :

            # Carichiamo l'immagine 1 e i keypoints (formato LFNet)
            with np.load(os.path.join(descriptors_path, desc_1)) as data1:
                a1 = data1
                d1 = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (a1[k] for k in a1))) 
            img1 = cv2.imread(os.path.join(dataset_path, image_1),cv2.IMREAD_GRAYSCALE)
            kp1 = d1['keypoints']
            des1 = d1['descriptors']
            if DEBUG == True : print('Primo descrittore estratto da R2D2 (type=float) :'), print(des1[0])
    
    
            # Carichiamo l'immagine 2 e i keypoints (formato .r2d2)
            with np.load(os.path.join(descriptors_path, desc_2)) as data2:
                a2 = data2
                d2 = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (a2[k] for k in a2)))
            img2 = cv2.imread(os.path.join(dataset_path, image_2),cv2.IMREAD_GRAYSCALE)
            kp2 = d2['keypoints']
            des2 = d2['descriptors']

            # Convertiamo i keypoints dell'immagine 1 in un oggetto di classe KeyPoint
            converted_keypoints_1 = []
            for i in range (0,kp1.shape[0]) :
                converted_keypoints_1.append(cv2.KeyPoint(kp1[i][0],kp1[i][1],0,0))
            if DEBUG == True : print('converted_keypoints_1 = {}'.format(type(converted_keypoints_1)))
    
            # Convertiamo i keypoints dell'immagine 2 in un oggetto di classe KeyPoint
            converted_keypoints_2 = []
            for i in range (0,kp2.shape[0]) :
                converted_keypoints_2.append(cv2.KeyPoint(kp2[i][0],kp2[i][1],0,0))
            if DEBUG == True : print('converted_keypoints_1 = {}'.format(type(converted_keypoints_2)))
    
            # Plot img1 with features
            if print_report == True :
                plt.figure(figsize=(10, 10))
                plt.title('Image 1')
                image1 = cv2.drawKeypoints(img1,converted_keypoints_1,img1,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
                plt.imshow(image1); plt.show()
    
            # Plot img2 with features
            if print_report == True :
                plt.figure(figsize=(10, 10))
                plt.title('Image 2')
                image2 = cv2.drawKeypoints(img2,converted_keypoints_2,img2,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
                plt.imshow(image2); plt.show()
    
            kp1 = converted_keypoints_1
            kp2 = converted_keypoints_2
    
            ### Brute Force
            #https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    
            if matches_verification == "crossCheck" :
    
                bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck_bool)
                matches = bf.match(des1,des2)
                numb_matches_not_filtred = None
                numb_matches_filtred = len(matches)
                #matches = sorted(matches, key = lambda x: x.distance)   # Sort matches by distance.  Best come first.
                img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2 ,matchColor=[0,255,0], flags=2)   # Show top nmatches matches
                if print_report == True :
                    plt.figure(figsize=(16, 16))
                    plt.title('Inserire Titolo')
                    plt.imshow(img_matches); plt.show()
                if DEBUG == True :
                    print('type(matches) : '), print(type(matches))
                    print('shape(matches) : '), print(len(matches))
                    print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
                    print('ciao')
                    print(matches[0].queryIdx)
                    print(matches[0].trainIdx)
                    print(matches[0].distance)
                if create_raw_matches_file == True :                 
                    raw_matches_file.write('{} {}\n'.format(image_1,image_2))
                    for j in range (0,len(matches)):
                        #print('{} {} {}'.format(matches[j].queryIdx,matches[j].trainIdx,matches[j].distance))
                        raw_matches_file.write('{} {}\n'.format(matches[j].queryIdx,matches[j].trainIdx))
                    raw_matches_file.write('\n')
                    raw_keypoints_img1 = open(path_raw_keypoints_img1,"w")
                    raw_keypoints_img1.write('{} 128\n'.format(len(kp1)))
                    for j in range (0,len(kp1)):
                        raw_keypoints_img1.write('{:.6f} {:.6f} 0.000000 0.000000 '.format(cv2.KeyPoint_convert(kp1)[j][0],cv2.KeyPoint_convert(kp1)[j][1]))
                        for k in range (0,128) : raw_keypoints_img1.write('0 ')
                        raw_keypoints_img1.write('\n')
                    raw_keypoints_img2 = open(path_raw_keypoints_img2,"w")
                    raw_keypoints_img2.write('{} 128\n'.format(len(kp2)))
                    for j in range (0,len(kp2)):
                        raw_keypoints_img2.write('{:.6f} {:.6f} 0.000000 0.000000 '.format(cv2.KeyPoint_convert(kp2)[j][0],cv2.KeyPoint_convert(kp2)[j][1]))
                        for k in range (0,128) : raw_keypoints_img2.write('0 ')
                        raw_keypoints_img2.write('\n')
                good_matches = matches
                    
    
            elif matches_verification == "Lowe_ratio_test" :

                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1,des2,k=2) # k=2 indica che vengono scritti in matches il primo e il secondo match, sarà utile per il Lowe Ratio Test
                numb_matches_not_filtred = len(matches)
                img_matches = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches[:nmatches],None,matchColor=[0,255,0],flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                if print_report == True :
                    plt.figure(figsize=(16, 16))
                    plt.title('Inserire Titolo')
                    plt.imshow(img_matches); plt.show()
                if DEBUG == True :
                    print('type(matches) : '), print(type(matches))
                    print('shape(matches) : '), print(len(matches))
                    print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
    
                ### Lowe Ratio Test
                # https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html

                ratio_thresh = ratio_threshold_value
                good_matches = []
                for m,n in matches:
                    #print('m={} n={}'.format(m,n))
                    if m.distance < ratio_thresh * n.distance:
                        good_matches.append(m)
                numb_matches_filtred = len(good_matches)
        
    
            ### RANSAC
            # https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html
    
            if len(good_matches)>MIN_MATCH_COUNT and RANSAC == True :
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                matchesMask = mask.ravel().tolist()
                numb_matches = len(matchesMask)
                h,w = img1.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)
                img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
                draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                                   singlePointColor = None,
                                   matchesMask = matchesMask, # draw only inliers
                                   flags = 2)
                img3 = cv2.drawMatches(img1,kp1,img2,kp2,good_matches,None,**draw_params)
                if print_report == True :
                    plt.imshow(img3, 'gray'),plt.show()
            else :
                print( "Not enough matches are found - {}/{} or parameter RANSAC = False".format(len(good_matches), MIN_MATCH_COUNT) )
                matchesMask = None


        elif detector_and_descriptor == "R2D2_features" :
            if DEBUG == True : print("detector_and_descriptor = R2D2_features")
    
            # Carichiamo l'immagine 1 e i keypoints (formato .r2d2)
            with np.load(os.path.join(descriptors_path, desc_1)) as data1:
                a1 = data1
                d1 = dict(zip(("resolution","keypoints","descriptors","scores"), (a1[k] for k in a1)))
            img1 = cv2.imread(os.path.join(dataset_path, image_1),cv2.IMREAD_GRAYSCALE)
            kp1 = d1['keypoints'][:,(0,1)]
            des1 = d1['descriptors']
            if DEBUG == True : print('Primo descrittore estratto da R2D2 (type=float) :'), print(des1[0])
            if like_SIFT == True : des1 = np.around(np.absolute(des1)*512)
            print('Primo descrittore moltiplicato per 512 e convertito in valori assoluti interi :'), print(des1[0])
    
            # Carichiamo l'immagine 2 e i keypoints (formato .r2d2)
            with np.load(os.path.join(descriptors_path, desc_2)) as data2:
                a2 = data2
                d2 = dict(zip(("resolution","keypoints","descriptors","scores"), (a2[k] for k in a2)))
            img2 = cv2.imread(os.path.join(dataset_path, image_2),cv2.IMREAD_GRAYSCALE)
            kp2 = d2['keypoints'][:,(0,1)]
            des2 = d2['descriptors']
            if like_SIFT == True : des2 = np.around(np.absolute(des2)*512)
            
            # Convertiamo i keypoints dell'immagine 1 in un oggetto di classe KeyPoint
            converted_keypoints_1 = []
            for i in range (0,kp1.shape[0]) :
                converted_keypoints_1.append(cv2.KeyPoint(kp1[i][0],kp1[i][1],0,0))
            if DEBUG == True : print('converted_keypoints_1 = {}'.format(type(converted_keypoints_1)))
    
            # Convertiamo i keypoints dell'immagine 2 in un oggetto di classe KeyPoint
            converted_keypoints_2 = []
            for i in range (0,kp2.shape[0]) :
                converted_keypoints_2.append(cv2.KeyPoint(kp2[i][0],kp2[i][1],0,0))
            if DEBUG == True : print('converted_keypoints_1 = {}'.format(type(converted_keypoints_2)))
            
            # Plot img1 with features
            plt.figure(figsize=(10, 10))
            plt.title('Image 1')
            image1 = cv2.drawKeypoints(img1,converted_keypoints_1,img1,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
            plt.imshow(image1); plt.show()
    
            # Plot img2 with features
            plt.figure(figsize=(10, 10))
            plt.title('Image 2')
            image2 = cv2.drawKeypoints(img2,converted_keypoints_2,img2,color=[255,0,0],flags=0) # For Python API, flags are modified as cv2.DRAW_MATCHES_FLAGS_DEFAULT, cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS, cv2.DRAW_MATCHES_FLAGS_DRAW_OVER_OUTIMG, cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS
            plt.imshow(image2); plt.show()
    
            kp1 = converted_keypoints_1
            kp2 = converted_keypoints_2
    
            ### Brute Force
            #https://docs.opencv.org/master/dc/dc3/tutorial_py_matcher.html
    
            if matches_verification == "crossCheck" :
    
                bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=crossCheck_bool)
                matches = bf.match(des1,des2)
                numb_matches_not_filtred = None
                numb_matches_filtred = len(matches)
                #matches = sorted(matches, key = lambda x: x.distance)   # Sort matches by distance.  Best come first.
                img_matches = cv2.drawMatches(img1, kp1, img2, kp2, matches[:nmatches], img2 ,matchColor=[0,255,0], flags=2)   # Show top nmatches matches
                plt.figure(figsize=(16, 16))
                plt.title('Inserire Titolo')
                plt.imshow(img_matches); plt.show()
                if DEBUG == True :
                    print('type(matches) : '), print(type(matches))
                    print('shape(matches) : '), print(len(matches))
                    print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
                    print('ciao')
                    print(matches[0].queryIdx)
                    print(matches[0].trainIdx)
                    print(matches[0].distance)
                if create_raw_matches_file == True :
                    raw_matches_file = open(path_raw_matches_file,"w")
                    raw_matches_file.write('{} {}\n'.format(image_1,image_2))
                    for j in range (0,len(matches)):
                        print('{} {} {}'.format(matches[j].queryIdx,matches[j].trainIdx,matches[j].distance))
                        raw_matches_file.write('{} {}\n'.format(matches[j].queryIdx,matches[j].trainIdx))
                    raw_keypoints_img1 = open(path_raw_keypoints_img1,"w")
                    raw_keypoints_img1.write('{} 128\n'.format(len(kp1)))
                    for j in range (0,len(kp1)):
                        raw_keypoints_img1.write('{:.6f} {:.6f} 0.000000 0.000000 '.format(cv2.KeyPoint_convert(kp1)[j][0],cv2.KeyPoint_convert(kp1)[j][1]))
                        for k in range (0,128) : raw_keypoints_img1.write('0 ')
                        raw_keypoints_img1.write('\n')
                    raw_keypoints_img2 = open(path_raw_keypoints_img2,"w")
                    raw_keypoints_img2.write('{} 128\n'.format(len(kp2)))
                    for j in range (0,len(kp2)):
                        raw_keypoints_img2.write('{:.6f} {:.6f} 0.000000 0.000000 '.format(cv2.KeyPoint_convert(kp2)[j][0],cv2.KeyPoint_convert(kp2)[j][1]))
                        for k in range (0,128) : raw_keypoints_img2.write('0 ')
                        raw_keypoints_img2.write('\n')
                good_matches = matches
                    
    
            elif matches_verification == "Lowe_ratio_test" :

                bf = cv2.BFMatcher()
                matches = bf.knnMatch(des1,des2,k=2) # k=2 indica che vengono scritti in matches il primo e il secondo match, sarà utile per il Lowe Ratio Test
                numb_matches_not_filtred = len(matches)
                img_matches = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches[:nmatches],None,matchColor=[0,255,0],flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
                plt.figure(figsize=(16, 16))
                plt.title('Inserire Titolo')
                plt.imshow(img_matches); plt.show()
                if DEBUG == True :
                    print('type(matches) : '), print(type(matches))
                    print('shape(matches) : '), print(len(matches))
                    print(matches[0]),print(matches[1]),print(matches[2]),print(matches[3])
    
                ### Lowe Ratio Test
                # https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html

                ratio_thresh = ratio_threshold_value
                good_matches = []
                for m,n in matches:
                    #print('m={} n={}'.format(m,n))
                    if m.distance < ratio_thresh * n.distance:
                        good_matches.append(m)
                numb_matches_filtred = len(good_matches)
        
    
            ### RANSAC
            # https://docs.opencv.org/master/d1/de0/tutorial_py_feature_homography.html
    
            if len(good_matches)>MIN_MATCH_COUNT:
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good_matches ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good_matches ]).reshape(-1,1,2)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
                matchesMask = mask.ravel().tolist()
                numb_matches = len(matchesMask)
                h,w = img1.shape
                pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)
                img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)
                draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                                   singlePointColor = None,
                                   matchesMask = matchesMask, # draw only inliers
                                   flags = 2)
                img3 = cv2.drawMatches(img1,kp1,img2,kp2,good_matches,None,**draw_params)
                plt.imshow(img3, 'gray'),plt.show()
            else :
                print( "Not enough matches are found - {}/{}".format(len(good_matches), MIN_MATCH_COUNT) )
                matchesMask = None

     
        else :
            print("Errore - Inserire un descrittore valido : ORB, SIFT, R2D2_features")
            quit()
   
   
        if print_report == True :
            print('Img1 - Numero keypoints = {}'.format(d1['keypoints'].shape[0]))
            print('Img2 - Numero keypoints = {}'.format(d2['keypoints'].shape[0]))
            print('Numero matches non ancora filtrati = {}'.format(numb_matches_not_filtred))
            print('Metodo verifica dei matches = {}'.format(matches_verification))
            print('crossCheck_bool = {}'.format(crossCheck_bool))
            print('Numero matches filtrati = {}'.format(numb_matches_filtred))
            print('Numero matches verificati con RANSAC = {}'.format(numb_matches))

raw_matches_file.close()