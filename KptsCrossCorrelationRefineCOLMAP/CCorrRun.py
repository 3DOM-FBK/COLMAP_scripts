'''
Keypoints refinement with Cross Correlation

'''

import os
import time
import cv2
#import imageio.v3 as iio
#import shutil
#import sqlite3
#import argparse
#import numpy as np
#from pathlib import Path
#from lib.COLMAPDatabase import COLMAPDatabase
#from lib.COLMAPDatabase import pair_id_to_image_ids
#from lib.COLMAPDatabase import blob_to_array
#from lib.patch_correlation import SSD
#from lib.patch_correlation import NCC
#from PIL import Image, ImageDraw

SHIFT_PIXEL_COLMAP = 0.5
#Image.MAX_IMAGE_PIXELS = 933120000

#start = time.time()
#img = Image.open(r"C:\Users\fbk3d\Documents\Projects\Graz\Imgs_jpg\Imgs_resized\0147-RGB.jpg")
#img = img.convert('L')
#img = img.crop((0,0,129,129))
#img = np.array(img)
#end=time.time()
#print("Pillow execution time:", end-start)

start = time.time()
#im = iio.imread(r"C:\Users\fbk3d\Documents\Projects\Graz\Imgs_jpg\Imgs_resized\0147-RGB.jpg")
#print(im.shape)
#print(type(im))
img = cv2.imread(r"C:\Users\fbk3d\Documents\Projects\Graz\Imgs_jpg\Imgs_resized\0147-RGB.jpg", 0)
print(type(img))
end=time.time()
print("ImageIO execution time:", end-start)
quit()

def MatchesFromDatabase(database_path):

    db = COLMAPDatabase.connect(database_path)

    images = dict(
        (image_id, name)
        for image_id, name in db.execute(
            "SELECT image_id, name FROM images"))

    pairID_and_pairs = dict(
                                    (pair[0], pair_id_to_image_ids(pair[0]))
                                    for pair in db.execute(
                                    "SELECT pair_id FROM two_view_geometries"
                                    )
                                    ) 

    pairID_N_matches = dict(
                                    (pair, matches_shape)
                                    for pair, matches_shape in db.execute(
                                    "SELECT pair_id, rows FROM two_view_geometries"
                                    )
                                    )
    
    pairID_and_matches = dict(
                                    (pair, blob_to_array(data, dtype=np.uint32))
                                    for pair, data in db.execute(
                                    "SELECT pair_id, data FROM two_view_geometries"
                                    )
                                    )
    
    image_id_and_keypoints = dict(
                                    (image_id, blob_to_array(data, dtype=np.float32))
                                    for image_id, data in db.execute(
                                    "SELECT image_id, data FROM keypoints"
                                    )
                                    )
    
    db.close
    
    #print(pairID_and_pairs[2147483649]) # The image pair
    #print(pairID_N_matches[2147483649]) # The total N of matches
    #print(len(pairID_and_matches[2147483649])) # Pairs of matches in sequence
    #print(len(pairID_and_keypoints[1])/6) # N of keypoints
    
    return images, pairID_and_pairs, pairID_N_matches, pairID_and_matches, image_id_and_keypoints


###############################################################################
# Main function
def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--Point3d", help = "Input points3D.txt COLMAP output")
    parser.add_argument("-d", "--Database", help = "Input path to the COLMAP database")
    parser.add_argument("-i", "--Images", help = "Input path to the image folder")
    parser.add_argument("-pw", "--PatchWidth", help = "Input patch width")
    parser.add_argument("-ph", "--PatchHight", help = "Input patch hight")
    parser.add_argument("-a", "--Amplification", help = "Input aplification factor for the patches to be refined")
    parser.add_argument("-m", "--Mode", help = "Input SSD or NCC for template matching")
    parser.add_argument("-o", "--Output", help = "Path to the output database")
    parser.add_argument("-s", "--Silent", help = "Silent mode")
    parser.add_argument("-f", "--Factor", help = "Scale factor when keypoints are extracted on smaller images")
    args = parser.parse_args()
    
    p3d_file_path = Path(args.Point3d)
    database_path = Path(args.Database)
    out_database_path = Path(args.Output)
    images_path = Path(args.Images)
    patch_width = int(args.PatchWidth)
    patch_hight = int(args.PatchHight)
    assert(patch_width % 2 != 0)
    assert(patch_hight % 2 != 0)
    A = int(args.Amplification)
    mode = args.Mode
    silent = args.Silent
    scale_factor = int(args.Factor)


    # Storing 3D points and tracks
    print("\nStoring 3D points and tracks ...")
    track_dic = {}
    with open(p3d_file_path, 'r') as p3d_file:
        for line in p3d_file:
            ini, _ = line.split(" ", 1)
            if ini != "#":
                POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK = line.split(" ", 8)
                track_dic[POINT3D_ID] = TRACK
    N_3D_pts = len(track_dic.keys())
    print("N of 3D points: {}".format(N_3D_pts))
    
    
    # Extracting valid matches from the database
    print("\nExtracting valid matches from the database ...")
    imgID_name, pairID_and_pairs, pairID_N_matches, pairID_and_matches, image_id_and_keypoints = MatchesFromDatabase(database_path)
    
    # Rearrange matches
    valid_matches = {}
    for pairID in pairID_and_pairs.keys():
    
        i1, i2 = pairID_and_pairs[pairID]
        i1 = int(i1)
        i2 = int(i2)
        i1_name = imgID_name[i1]
        i2_name = imgID_name[i2]
        
        tie_point_im1 = pairID_and_matches[pairID][0::2].tolist()
        tie_point_im2 = pairID_and_matches[pairID][1::2].tolist()
        assert(len(tie_point_im1)==len(tie_point_im2))
        
        kpt1 = np.asarray(image_id_and_keypoints[i1]).reshape(-1,6) * scale_factor
        kpt2 = np.asarray(image_id_and_keypoints[i2]).reshape(-1,6) * scale_factor
        #images = os.listdir(images_path)
        #image1_name = images[1]
        #print(image1_name)
        #image1 = Image.open(images_path / image1_name)
        #image1 = image1.convert('L')
        #draw = ImageDraw.Draw(image1) 
        #for r in range(kpt2.shape[0]):
        #    draw.point((kpt2[r,0],kpt2[r,1]),fill=250)
        #image1.show()
        #quit()
        
        for c in range(len(tie_point_im1)):
            tie_point_im1[c] = (kpt1[tie_point_im1[c],0], kpt1[tie_point_im1[c],1])
            tie_point_im2[c] = (kpt2[tie_point_im2[c],0], kpt2[tie_point_im2[c],1])
           
        
        valid_matches["{}_{}".format(i1_name, i2_name)] = (tie_point_im1, tie_point_im2)
        #print(valid_matches["{}_{}".format(i1_name, i2_name)])

    
    # Display tie points of the first pair
    #images = os.listdir(images_path)
    #image1_name = images[0]
    #image2_name = images[1]
    #key = "{}_{}".format(image1_name, image2_name)
    #image1 = Image.open(images_path / image1_name)
    #image2 = Image.open(images_path / image2_name)
    #image1 = np.array(image1.convert('L'))
    #image2 = np.array(image2.convert('L'))
    #image = np.hstack((image1, image2))
    #image = Image.fromarray(image)
    #draw = ImageDraw.Draw(image) 
    #
    #for m1, m2 in zip(valid_matches[key][0], valid_matches[key][1]):
    #    #print(m1, m2)
    #    draw.line((m1[0], m1[1], m2[0]+image1.shape[1], m2[1]), fill=250, width = 1)
    #if silent == 'False': print("key", key)
    #image.show()
    
    
    # Refining each track
    c=0
    
    # Preparing a new dict for storing the refined keypoints
    refined_keypoints = {}
    for key in image_id_and_keypoints:
        kp_matrix = np.asarray(image_id_and_keypoints[key]).reshape(-1,6)
        refined_keypoints[imgID_name[key]] = kp_matrix * scale_factor
    
    #Processing each track
    for track_key in track_dic:
        track_dic[track_key] = track_dic[track_key].strip()
        current_track_list = track_dic[track_key]
        if silent == 'False': print(current_track_list)
        current_track_list = current_track_list.split(" ")
        current_track_list = [int(i) for i in current_track_list]
        
        # Rewriting the track inserting the coordinates of the keypoints instead of the id
        current_track = []
        for t in range(int(len(current_track_list)/2)):
            im_id = current_track_list[t*2]
            kpt = np.asarray(image_id_and_keypoints[im_id]).reshape(-1,6) * scale_factor
            #print(kpt[0:5,:])
            current_track.append((im_id, imgID_name[im_id], kpt[current_track_list[t*2+1], 0], kpt[current_track_list[t*2+1], 1], current_track_list[t*2+1]))
            #print(im_id)
            #print(imgID_name[im_id])
            #print(current_track[im_id])
        
        if silent == 'False': print(current_track)
        
        # Checking corresponding patches
        #for current_ktp in current_track:
        #    image_name = current_ktp[1]
        #    x = current_ktp[2]
        #    y = current_ktp[3]
        #    img = Image.open(images_path / image_name)
        #    patch = img.crop((x-patch_width//2, y-patch_hight//2, x+patch_width//2, y+patch_hight//2))
        #    patch.show()

        # Template matching refinement
        filled_template = False
        for current_ktp in current_track:
            image_name = current_ktp[1]
            x = current_ktp[2]
            y = current_ktp[3]
            kp_id = current_ktp[4]
            
            if filled_template == False:
                img = Image.open(images_path / image_name)
                if (x-patch_width//2) < 0 or (y-patch_hight//2) < 0 or (x+patch_width//2+1) > img.width or (y+patch_hight//2+1) > img.height:
                    break
                else:
                    patch = img.crop((x-patch_width//2, y-patch_hight//2, x+patch_width//2+1, y+patch_hight//2+1))
                    if silent == 'False': patch.show()
                    template = np.array(patch.convert('L'))
                    filled_template = True
            else:
                if x-patch_width//2*A < 0 or y-patch_hight//2*A < 0 or x+patch_width//2*A+1 > img.width or y+patch_hight//2*A+1 > img.height:
                    break
                else:
                    img = Image.open(images_path / image_name)
                    patch = img.crop((x-patch_width//2*A, y-patch_hight//2*A, x+patch_width//2*A+1, y+patch_hight//2*A+1))
                    if silent == 'False': patch.show()
                    ref_patch = np.array(patch.convert('L'))
                    
                    if mode == 'SSD':
                        yp, xp = SSD(ref_patch, template, silent) # Refined coordinates in the ref_patch ref system
                        delta_yp = yp - (patch_hight//2*A)
                        delta_xp = xp - (patch_width//2*A)

                        assert(x == refined_keypoints[image_name][kp_id][0])
                        assert(y == refined_keypoints[image_name][kp_id][1])
                        refined_keypoints[image_name][kp_id][0] = x + delta_xp + SHIFT_PIXEL_COLMAP
                        refined_keypoints[image_name][kp_id][1] = y + delta_yp + SHIFT_PIXEL_COLMAP
                        
                    elif mode == 'NCC':
                        if silent == 'False': print("ref_patch.shape, template.shape", ref_patch.shape, template.shape)
                        yp, xp = NCC(ref_patch, template, silent) # Refined coordinates in the ref_patch ref system
                        delta_yp = yp - (patch_hight//2*A)
                        delta_xp = xp - (patch_width//2*A)
                        
                        assert(x == refined_keypoints[image_name][kp_id][0])
                        assert(y == refined_keypoints[image_name][kp_id][1])
                        refined_keypoints[image_name][kp_id][0] = x + delta_xp + SHIFT_PIXEL_COLMAP
                        refined_keypoints[image_name][kp_id][1] = y + delta_yp + SHIFT_PIXEL_COLMAP

                    
            
        print("Processed track {} / {}".format(c, N_3D_pts)) #, end='\r'
        
        
        c += 1
        #if c==1000:
            #quit()
    
    
    # Export refined keypoints in a COLMAP database
    print("Saving new database ...")
    shutil.copyfile(database_path, out_database_path)
    db_out = COLMAPDatabase.connect(out_database_path)
    for key_im_name in refined_keypoints:
        for value in imgID_name:
            if imgID_name[value] == key_im_name:
                key_id = value           
                db_out.substitute_keypoints(key_id, refined_keypoints[key_im_name])
                if silent == 'False': print(refined_keypoints[key_im_name])
    
    # Check database
    image_id_and_keypoints = dict(
                                (image_id, blob_to_array(data, dtype=np.float32))
                                for image_id, data in db_out.execute(
                                "SELECT image_id, data FROM keypoints"
                                )
                                )
    if silent == 'False': print(image_id_and_keypoints)
    
    db_out.commit()
    db_out.close

###############################################################################
# Driver function 
if __name__=="__main__": 
    main()