from pathlib import Path
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Print more info for an easier debug
INFO = False

# Paths to input folders
image_folder = Path(r"C:\Users\Luscias\Desktop\3DOM\Python_scripts\Aerial-Imgs\imgs")
tile_folder = Path(r"C:\Users\Luscias\Desktop\3DOM\Python_scripts\Aerial-Imgs\tiles")
desc_folder = Path(r"C:\Users\Luscias\Desktop\3DOM\Python_scripts\Aerial-Imgs\desc")

################################################################################
def rearrangeKpts(  img1,
                    image_folder,
                    desc_folder,
                    colmap_desc_folder,
                    matches_folder,
                    tile_folder):
    image_list = os.listdir(image_folder)
    tile_list = os.listdir(tile_folder)
    desc_list = os.listdir(desc_folder)
    
    # Rearrange keypoints coordinates and descriptors to obtain an unique file for each image

    total_numb_kpts = 0
    print("\n\n\nimg1", img1)
    for tile in tile_list:
        if img1[:-4] in tile:
            print(f"\nProcessing {img1} {tile}")
            image_name_len = len(img1[:-4])
            tile_info = tile[image_name_len+1:-4]
            row, col, ox, oy, tw, th = tile_info.split("_")
            row, col, ox, oy, tw, th = int(row[1:]), int(col[1:]), int(ox[2:]), int(oy[2:]), int(tw[2:]), int(th[2:])
            
            # Import keypoints from file (LFNet format)
            np_desc_path = Path("{}.npz".format(tile))
            abs_np_desc_path = desc_folder / np_desc_path
            with np.load(abs_np_desc_path) as data:
                d = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (data[k] for k in data)))
            kp = d['keypoints']
            kp_numb = d['keypoints'].shape[0]
            total_numb_kpts += kp_numb
            desc = d['descriptors']
            
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
    
    print(f"\n{img1}")
    print("Total number of keypoints processed:", total_numb_kpts)
    print("Keypoint coordinates shape:", image_kps.shape)
    print("Descriptor matrix shape:", image_desc.shape)
    
    ## Convert keypoints in openCV format
    opencv_keypoints = []
    for i in range (0,image_kps.shape[0]):
        opencv_keypoints.append(cv2.KeyPoint(image_kps[i][0],image_kps[i][1],0,0))
    
    # Show keypoints on image
    if INFO:
        img = cv2.imread(str(image_folder / Path(img1)))
        plt.figure(figsize=(10, 10))
        plt.title(f'Image {img1}')
        image_with_kpts = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0)
        plt.imshow(image_with_kpts)
        plt.show()
    
    return opencv_keypoints, image_desc, total_numb_kpts

################################################################################
# MAIN STARTS HERE
def main():
    image_list = os.listdir(image_folder)
    tile_list = os.listdir(tile_folder)
    desc_list = os.listdir(desc_folder)
    
    if INFO :
        print("\nImage list:", image_list)
        print("Number of tiles:", len(tile_list))
        print("Number of files in desc folder:", len(desc_list))
    
    # Rearrange keypoints coordinates and descriptors to obtain an unique file for each image
    for image in image_list:
        total_numb_kpts = 0
        for tile in tile_list:
            if image[:-4] in tile:
                print(f"\nProcessing {image} {tile}")
                image_name_len = len(image[:-4])
                tile_info = tile[image_name_len+1:-4]
                row, col, ox, oy, tw, th = tile_info.split("_")
                row, col, ox, oy, tw, th = int(row[1:]), int(col[1:]), int(ox[2:]), int(oy[2:]), int(tw[2:]), int(th[2:])
                if INFO:
                    print('row\t', 'col\t', 'ox\t', 'oy\t', 'tw\t', 'th\t')
                    print(row, '\t', col, '\t', ox, '\t', oy, '\t', tw, '\t', th)
                
                # Import keypoints from file (LFNet format)
                np_desc_path = Path("{}.npz".format(tile))
                abs_np_desc_path = desc_folder / np_desc_path
                with np.load(abs_np_desc_path) as data:
                    d = dict(zip(("keypoints","descriptors","resolution","scale","orientation"), (data[k] for k in data)))
                kp = d['keypoints']
                kp_numb = d['keypoints'].shape[0]
                total_numb_kpts += kp_numb
                desc = d['descriptors']
                if INFO:
                    print("kp_numb:\n", kp_numb)
                    print("kpts first two rows:\n", kp[0:2,:])
                    print("Descriptor matrix shape:\n", desc.shape)
                
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
        
        print(f"\n{image}")
        print("Total number of keypoints processed:", total_numb_kpts)
        print("Keypoint coordinates shape:", image_kps.shape)
        print("Descriptor matrix shape:", image_desc.shape)
        
        # Convert keypoints in openCV format
        opencv_keypoints = []
        for i in range (0,image_kps.shape[0]):
            opencv_keypoints.append(cv2.KeyPoint(image_kps[i][0],image_kps[i][1],0,0))
        
        # Show keypoints on image
        img = cv2.imread(str(image_folder / Path(image)))
        plt.figure(figsize=(10, 10))
        plt.title(f'Image {image}')
        image_with_kpts = cv2.drawKeypoints(img,opencv_keypoints,img,color=[255,0,0],flags=0)
        plt.imshow(image_with_kpts)
        plt.show()
    
################################################################################
# DRIVER FUNCTION 
if __name__=="__main__": 
    main()
                
