# Usage example
# python SequentialCrossCorr.py -pw 99 -ph 99 -i ./tests/three_imgs/imgs -k ./tests/three_imgs/kpts -o ./tests/three_imgs/colmap_kpts -s True 

from numba import jit
import os
import numpy as np
import argparse
from pathlib import Path
from PIL import Image, ImageDraw
from scipy import signal
from scipy import ndimage
#from lib.prova import NCC
#from lib.prova import SSD


STATIC_KPTS_THRESHOLD = 0
SEARCHING_WINDOW_WIDTH_AMPLIFICATION_FACTOR = 2.5
SEARCHING_WINDOW_HEIGHT_AMPLIFICATION_FACTOR= 18

@jit(nopython=True, cache=True) 
def NCC(ref, templ, silent):
    '''
    Normalized Cross Correlation
    https://www.researchgate.net/profile/Wen-Gao-11/publication/224641323_Image_Matching_by_Normalized_Cross-Correlation/links/54bd11b40cf218da939104e0/Image-Matching-by-Normalized-Cross-Correlation.pdf?_sg%5B0%5D=qZzyt3qsKS2Kg4gAL54pYHhZZIB8cWBRHcSn3oWGuhOw6o6P-IS_9ZXQR9vAKMvN2wkYaZtXdRQ8Xq5W9Jfi9w.ldWU6W6eYOJSXpIDeayWWUJynXRI6OZsrVESkcvhU8jOag4-6WzOFgrj304tLXxI7Krpd3cQIp7bDT71bLMVTA&_sg%5B1%5D=TbrqXOluFMOFLDUiKsVKrjcanxWzzfGKtmCl857vQqJoOsAkarKbCxeYKYou5eUpU9pQoBlo3OGQzaLRZ5MlamYYKZJfqyER5SUC_j-8MY9Z.ldWU6W6eYOJSXpIDeayWWUJynXRI6OZsrVESkcvhU8jOag4-6WzOFgrj304tLXxI7Krpd3cQIp7bDT71bLMVTA&_iepl=
    '''
    EPSILON = 0.001 # To avoid division by zero

    if silent == 'False': print("np.max(ref)", np.max(ref))
    if silent == 'False': print("np.min(ref)", np.min(ref))
    if silent == 'False': print("np.max(templ)", np.max(templ))
    if silent == 'False': print("np.min(templ)", np.min(templ))
    
    ref_row = ref.shape[0]
    ref_col = ref.shape[1]
    templ_row = templ.shape[0]
    templ_col = templ.shape[1]
    
    ncc_matrix = np.empty((ref_row-templ_row+1, ref_col-templ_col+1))
    ssd_row = ncc_matrix.shape[0]
    ssd_col = ncc_matrix.shape[1]
    
    for r in range(0, ssd_row):
        for c in range(0, ssd_col):
            ref_cut = ref[r:r+templ_row, c:c+templ_col]
           
            #ref_cut -= ref_cut.mean()
            #ref_cut = ref_cut / np.std(ref_cut)
            #print("ref_cut.mean(), ref_cut.std()", ref_cut.mean(), ref_cut.std())
            #templ -= templ.mean()
            #templ = templ / np.std(templ)            
            #print("templ.mean(), templ.std()", templ.mean(), templ.std())

            ncc = np.sum((ref_cut-ref_cut.mean())*(templ-templ.mean()))/(ref_cut.std()*templ.std()+EPSILON) # Manca normalizzazione rispetto alla dimensione della finestra al denominatore, vedere paper
            ncc_matrix[r,c] = ncc
    
    if silent == 'False': print("ncc_matrix.shape", ncc_matrix.shape)
    if silent == 'False': print("np.max(ncc_matrix)", np.max(ncc_matrix))
    if silent == 'False': print("np.min(ncc_matrix)", np.min(ncc_matrix))
    #y, x = np.unravel_index(np.argmax(ncc_matrix), ncc_matrix.shape)  # find the match
    index_max = np.argwhere(ncc_matrix==np.max(ncc_matrix))
    y, x = index_max.ravel()[0], index_max.ravel()[1]
    
    ncc_matrix = ncc_matrix / np.max(ncc_matrix) * 255.0
    #ncc_matrix = Image.fromarray(ncc_matrix)
    #if silent == 'False': ncc_matrix.show()
    
    #a = y+int((templ_row-1)/2)
    #b = x+int((templ_col-1)/2)
    #ref[a, b] = 0
    #ref = Image.fromarray(ref)
    #if silent == 'False': ref.show()
    
    y, x = y+int((templ_row-1)/2), x+int((templ_col-1)/2)
    
    return y, x


def conv_laplacian(image):
    kernel = np.array([
                        [-1,  0,  1],
                        [-1,  0,  1],
                        [-1,  0,  1]
                        ])
    convolved1 = signal.convolve2d(image, kernel, mode='full', boundary='symm', fillvalue=0)

    kernel = np.array([
                    [-1,  -1,  -1],
                    [0,    0,   0],
                    [1,    1,   1]
                    ])
    convolved2 = signal.convolve2d(image, kernel, mode='full', boundary='symm', fillvalue=0)
    convolved = np.sqrt(convolved1**2+convolved2**2)
    #convolved = ndimage.gaussian_filter(convolved, sigma=2, order=0) #### DA NON USARE, SERVONO FEATURES A GRANA FINE!!
    return convolved

@jit(nopython=True, cache=True)
def crop_nparray(patch_np, centerxy, width, height):
    x = centerxy[0]
    y = centerxy[1]
    cropped_patch = patch_np[y-height//2 : y+height//2, x-width//2 : x+width//2]
    return cropped_patch

#def SequentialCrossCorrelation_old(initial_kpt, img_folder, patch_width, patch_hight, silent):
#    template_img = Image.open(img_folder / initial_kpt[0])
#    template_img = template_img.convert('L')
#    template_img_np = np.array(template_img)
#    #if silent == "False": ref_img.show()
#
#    template_patch = crop_nparray(template_img_np, (initial_kpt[1], initial_kpt[2]), patch_width, patch_hight)
#    if silent == "False": template_patch = Image.fromarray(template_patch); template_patch.show(); template_patch = np.array(template_patch)
#
#    img_list = os.listdir(img_folder)
#    img_list.sort()
#
#    for im in img_list[0:]:
#        if im != initial_kpt[0]:
#            print("template_img", initial_kpt[0])
#            print("target_img", im)
#            target_img = Image.open(img_folder / im)
#            target_img = target_img.convert('L')
#            target_img_np = np.array(target_img)
#            searching_window = crop_nparray(target_img_np, (initial_kpt[1], initial_kpt[2]), 2*patch_width, 6*patch_hight)
#            if silent == "False": searching_window = Image.fromarray(searching_window); searching_window.show(); searching_window = np.array(searching_window)
#
#            searching_window = conv_laplacian(searching_window); #searching_window.astype(int)
#            template_patch = conv_laplacian(template_patch); #template_patch.astype(int)
#            searching_window = np.absolute(searching_window)
#            template_patch = np.absolute(template_patch)
#            print(np.max(searching_window))
#            print(type(np.max(searching_window)))
#            print(np.max(template_patch))
#            print(type(np.max(template_patch)))
#            searching_window = Image.fromarray(searching_window.astype(np.uint8))
#            searching_window.show()
#            template_patch = Image.fromarray(template_patch.astype(np.uint8))
#            template_patch.show()
#            searching_window = np.array(searching_window)
#            template_patch = np.array(template_patch)
#      
#            y, x = NCC(searching_window, template_patch, 'False')
#            
#            print(x,y)
#            searching_window = Image.fromarray(searching_window)
#            img_with_box = ImageDraw.Draw(searching_window)
#            img_with_box.rectangle([x-patch_width//2, y-patch_hight//2, x+patch_width//2, y+patch_hight//2], fill=None, outline="black", width=5)
#            searching_window.show()
#
#            quit()
#
#    return None


def SequentialCrossCorrelation(initial_kpt, target_image, img_folder, patch_width, patch_hight, silent):

    #print(initial_kpt[1])
    #print(initial_kpt[2])
    #quit()

    template_img = Image.open(img_folder / initial_kpt[0])
    template_img = template_img.convert('L')
    template_img_np = np.array(template_img)
    #if silent == "False": ref_img.show()

    template_patch = crop_nparray(template_img_np, (initial_kpt[1], initial_kpt[2]), patch_width, patch_hight)
    if silent == "False": template_patch = Image.fromarray(template_patch); template_patch.show(); template_patch = np.array(template_patch)

    img_list = os.listdir(img_folder)
    img_list.sort()

    if silent == "False": print("template_img", initial_kpt[0])
    if silent == "False": print("target_img", target_image)
    target_img = Image.open(img_folder / target_image)
    target_img = target_img.convert('L')
    target_img_np = np.array(target_img)

    searching_window_width = patch_width * SEARCHING_WINDOW_WIDTH_AMPLIFICATION_FACTOR              
    searching_window_height = patch_hight * SEARCHING_WINDOW_HEIGHT_AMPLIFICATION_FACTOR             
    target_img_width = target_img_np.shape[1]
    target_image_height = target_img_np.shape[0]

    searching_window = crop_nparray(target_img_np, (initial_kpt[1], initial_kpt[2]), searching_window_width, searching_window_height)
    if silent == "False": searching_window = Image.fromarray(searching_window); searching_window.show(); searching_window = np.array(searching_window)
    searching_window = conv_laplacian(searching_window); #searching_window.astype(int)
    template_patch = conv_laplacian(template_patch); #template_patch.astype(int)
    searching_window = np.absolute(searching_window)
    template_patch = np.absolute(template_patch)
    if silent == "False": print(np.max(searching_window))
    if silent == "False": print(type(np.max(searching_window)))
    if silent == "False": print(np.max(template_patch))
    if silent == "False": print(type(np.max(template_patch)))
    searching_window = Image.fromarray(searching_window.astype(np.uint8))
    if silent == "False": searching_window.show()
    template_patch = Image.fromarray(template_patch.astype(np.uint8))
    if silent == "False": template_patch.show()
    searching_window = np.array(searching_window)
    template_patch = np.array(template_patch)

    y, x = NCC(searching_window, template_patch, silent)
    
    if silent == "False": print(x,y)
    searching_window = Image.fromarray(searching_window)
    img_with_box = ImageDraw.Draw(searching_window)
    img_with_box.rectangle([x-patch_width//2, y-patch_hight//2, x+patch_width//2, y+patch_hight//2], fill=None, outline="black", width=5)
    if silent == "False": searching_window.show()

    X = initial_kpt[1] - searching_window_width  // 2 + x
    Y = initial_kpt[2] - searching_window_height // 2 + y
    
        
    return X, Y


def Tracking(tentative_kpts, img_folder, img_dict, patch_width, patch_hight, silent): # TODO si potrebbe ciclare su patch successive aggiorando la patch reference con quella appena trovata e così via
    
    track_dict = {}
    t = 0
    img_dict_reverse = {a:b for a, b in zip(img_dict.values(), img_dict.keys())}

    tt = 0
    for kp in tentative_kpts:
        tt += 1
        print("Current track: {}".format(tt))
        current_track = []
        current_image = kp[0]
        current_id = img_dict_reverse[current_image]
        #print(current_image, current_id)
        #candidate_images = [i % len(img_dict.keys()) for i in range(current_id-2, current_id+3)] # 2 imgs forward, 2 backward
        candidate_images = [i % len(img_dict.keys()) for i in range(current_id-1, current_id+2)] # 1 imgs forward, 1 backward
        candidate_images.pop(len(candidate_images)//2)
        print("Current id and current image: {} {}".format(current_id, current_image))
        print(candidate_images)
        print([img_dict[im_id] for im_id in candidate_images])
        
        for c in candidate_images:
            target_im = img_dict[c]
            x, y = SequentialCrossCorrelation(kp, target_im, img_folder, patch_width, patch_hight, silent)
            if np.absolute(x-kp[1])>=STATIC_KPTS_THRESHOLD and np.absolute(y-kp[2])>=STATIC_KPTS_THRESHOLD:
                current_track.append((target_im , x, y))
            else:
                print("Excluded because static tie point, errors in px: {}, {}".format(np.absolute(x-kp[1]), np.absolute(y-kp[2])))
                quit()
            #current_track.append((target_im , x, y))
        
        if current_track != []:
            current_track.append(kp)
            track_dict[t] = current_track
            t += 1
        current_track = []
        
            
    return track_dict


def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-pw", "--PatchWidth", help = "Input patch width")
    parser.add_argument("-ph", "--PatchHight", help = "Input patch hight")
    parser.add_argument("-i", "--Images", help = "Image folder")
    parser.add_argument("-k", "--KeypointsFolder", help = "Keypoint folder")
    parser.add_argument("-s", "--Silent", help = "Silent mode")
    parser.add_argument("-o", "--Outs", help = "Output folder")
    args = parser.parse_args()

    patch_width = int(args.PatchWidth)
    patch_hight = int(args.PatchHight)
    img_folder = Path(args.Images)
    kpts_folder = Path(args.KeypointsFolder)
    output_folder = Path(args.Outs)
    silent = args.Silent


    print("SequentialCrossCorrelation")
    img_list = os.listdir(img_folder)
    img_list.sort()   
    print("N of images:\t{}".format(len(img_list)))
    #initial_kpt = (img_list[0], 5708, 2148)
    #initial_kpt = (img_list[0], 1756, 2179)
    #initial_kpt = (img_list[0], 2542, 2378)
    #initial_kpt = (img_list[0], 2055, 1726)
    #initial_kpt = (img_list[0], 1498, 2192)

    print("Storing all tentative keypoints ...")
    tentative_kpts = []
    images_with_kpts = os.listdir(kpts_folder)
    for img_with_kpts in images_with_kpts:
        with open(kpts_folder / Path("{}".format(img_with_kpts))) as kpt_file:
            lines = kpt_file.readlines()
            for line in lines[1:]:
                line = line.strip()
                x, y, _ = line.split(" ", 2)
                tentative_kpts.append((img_with_kpts[:-4], int(x), int(y)))
    #tentative_kpts = tentative_kpts[0:1]
    print("N of tentative kpts: \t{}".format(len(tentative_kpts)))
    
    # Giving an ID to each image
    img_dict = {i:img_name for i, img_name in zip(range(len(img_list)), img_list)}

    #SequentialCrossCorrelation(initial_kpt, img_folder, patch_width, patch_hight, silent)
    track_dict = Tracking(tentative_kpts, img_folder, img_dict, patch_width, patch_hight, silent)
    print(track_dict)

    # Write keypoints and matches in the COLMAP format
    kpts_dict = {}
    matches_dict = {}

    # Filling keypoints
    for track in track_dict:
        track_dict[track].sort(key = lambda element : element[0])
        for cont, t in enumerate(track_dict[track]):
            print("t", t)
            img = t[0]
            x = t[1]
            y = t[2]

            if img not in kpts_dict.keys():
                kpts_dict[img] = [(x, y)]
            else:
                kpts_dict[img].append((x, y))

            track_dict[track][cont] = (img, len(kpts_dict[img])-1) # Assinging an ID to each kpt


    # Generating all the possible couples
    #print("img_list", img_list)
    for i in range(len(img_list)-1):
        for j in range(1, len(img_list)):
            matches_dict[(img_list[i], img_list[j])] = []

    # Filling matches
    for track in track_dict:
        track_dict[track].sort(key = lambda element : element[0])
        print("track", track_dict[track])
        for en, t1 in enumerate(track_dict[track][:-1]):
            img1 = t1[0]
            kp_id1 = t1[1]
            print("img1, kp_id1", img1, kp_id1)
            for t2 in track_dict[track][en+1:]:
                img2 = t2[0]
                kp_id2 = t2[1]
                print("img2, kp_id2", img2, kp_id2)
                matches_dict[(img1, img2)].append((kp_id1, kp_id2))

                

    
    #print(track_dict)
    print("kpts_dict", kpts_dict)
    #print(matches_dict)


    for im, kp_im in zip(kpts_dict.keys(), kpts_dict.values()):
        print('im', 'kp_im')
        print(im, kp_im)
        with open(r"{}/{}.txt".format(output_folder, im), 'w') as kpt_file:
            kpt_file.write('{} 128\n'.format(len(kp_im)))
            for k in kp_im:
                print("k", k)
                kpt_file.write("{:.6f} {:.6f} 0.000000 0.000000\n".format(k[0], k[1]))

    with open(r"{}/matches.txt".format(output_folder), 'w') as matches_file:
        for m in matches_dict.keys():
            if matches_dict[m] != []:
                matches_file.write("{} {}\n".format(m[0], m[1]))
                for match in matches_dict[m]:
                    matches_file.write("{} {}\n".format(match[0], match[1]))
                matches_file.write("\n")


# Driver function 
if __name__=="__main__": 
    main()
