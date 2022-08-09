# Usage:
# python detector.py -i ./tests/bottle/imgs -m ./tests/bottle/masks -o ./tests/bottle/kpts -b True -t 30 -a random_points -n 100 -s False 

import os
import argparse
import cv2 as cv
import numpy as np
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
from scipy import signal, ndimage


PIX_BUFFER = 70 # 70 used for the plastic bottle


def conv_laplacian(image):

    kernel = np.array([
                        [-1,  0,  1],
                        [-1,  0,  1],
                        [-1,  0,  1]
                        ])
    convolved1 = signal.convolve2d(image, kernel, mode='same', boundary='symm', fillvalue=0)

    kernel = np.array([
                    [-1,  -1,  -1],
                    [0,    0,   0],
                    [1,    1,   1]
                    ])

    convolved2 = signal.convolve2d(image, kernel, mode='same', boundary='symm', fillvalue=0)
    convolved = np.sqrt(convolved1**2+convolved2**2)
    convolved = ndimage.gaussian_filter(convolved, sigma=15, order=0)

    return convolved


def LocalFeatures(path_to_img, mask_threshold, silent, path_to_masks, use_ini_masks, approach, n_kpts):

    # Image prepocessing (derivatives and gaussian kernels)
    img_name = path_to_img.name
    img = Image.open(path_to_img).convert('L')
    img_np = np.array(img)
    convolved = conv_laplacian(img_np)
    
    if silent == "False":
        convolved = Image.fromarray(convolved)
        convolved.show()
        convolved = np.array(convolved)
    
    # Binarization (zero or one)
    convolved = (convolved - np.min(convolved)) 
    convolved = convolved* 255 / np.max(convolved)
    convolved = convolved.astype(np.uint8)
    convolved = Image.fromarray(convolved, 'L')
    convolved = convolved.point( lambda p: 255 if p > mask_threshold else 0 )
    convolved = convolved.convert("1")
    if silent == "False": convolved.show()

    if use_ini_masks == "True":
        initial_mask = Image.open(path_to_masks / "{}.mask.JPG".format(img_name[:-4]))
        initial_mask = initial_mask.convert('1')
        initial_mask = ImageChops.invert(initial_mask)
        if silent == "False": initial_mask.show()
        convolved = ImageChops.logical_or(convolved, initial_mask)
        if silent == "False": convolved.show()
    
    convolved = np.array(convolved)

    # Buffer the actual mask by PIX_BUFFER
    #dim1, dim2 = convolved.shape[0], convolved.shape[1]
    ###one_cells = []
    ###for idx, cell in np.ndenumerate(convolved):
    ###    if cell == 1:
    ###        one_cells.append((idx[1], idx[0]))
    #one_cells = np.argwhere(convolved==1)
    #convolved = Image.fromarray(convolved)
    #convolved = convolved.convert('RGB')
    #draw = ImageDraw.Draw(convolved)
    #for kpt in one_cells:
    #    ellipse_bounding_box = [kpt[1]-PIX_BUFFER, kpt[0]-PIX_BUFFER, kpt[1]+PIX_BUFFER, kpt[0]+PIX_BUFFER]
    #    draw.ellipse(ellipse_bounding_box, fill='white', outline='white', width=1)
    #if silent == "False": convolved.show()
    #convolved = convolved.convert('1')
    #convolved = np.array(convolved)

    # Keypoints extracted at random outside the mask
    if approach == "random_points":
        sel_index = np.random.choice(np.argwhere(convolved.ravel()==0).ravel(), size=n_kpts)
        random_y, random_x = np.unravel_index(sel_index, convolved.shape)
        ktps_list = [(x, y) for x, y in zip(random_x, random_y)]
    
    elif approach == "density":
        pass

    elif approach == "harris":
        img_name = path_to_img.name
        img = Image.open(path_to_img).convert('L')
        img_np = np.array(img)
        #cv.imshow('graycsale image',img_np)
        #cv.waitKey(0)
        #cv.destroyAllWindows()
        dst = cv.cornerHarris(img_np,2,3,0.04)
        dst = cv.dilate(dst,None)
        img_np[dst>0.0001*dst.max()]=0 # img_np[dst>0.01*dst.max()]=0
        img_np = Image.fromarray(img_np)
        #img_np.show()
        img_np = np.array(img_np)
        img_np[img_np!=0]=255
        img_np = Image.fromarray(img_np)
        img_np = img_np.convert('1')
        #img_np.show()
        convolved = Image.fromarray(convolved)
        #convolved.show()
        intersection = ImageChops.logical_or(convolved, img_np)
        #intersection.show()

        intersection = np.array(intersection)
        #print(len(np.argwhere(intersection.ravel()==0).ravel()))
        number_kpts = min(n_kpts, len(np.argwhere(intersection==0)))
        
        sel_index = np.random.choice(np.argwhere(intersection.ravel()==0).ravel(), size=number_kpts)
        random_y, random_x = np.unravel_index(sel_index, intersection.shape)
        ktps_list = [(x, y) for x, y in zip(random_x, random_y)]
        convolved = np.array(convolved)
        
    
    # Drawing keypoints as points
    #if silent == "False":
    #    convolved = Image.fromarray(convolved)
    #    convolved = convolved.convert('RGB')
    #    draw = ImageDraw.Draw(convolved)
    #    draw.point(ktps_list, fill='red')
    #    convolved.show()
    
    # Drawing keypoints as circles
    if silent == "False":
        convolved = Image.fromarray(convolved)
        convolved = convolved.convert('RGB')
        draw = ImageDraw.Draw(convolved)
        for kpt in ktps_list:
            ellipse_bounding_box = [kpt[0]-10, kpt[1]-10, kpt[0]+10, kpt[1]+10]
            draw.ellipse(ellipse_bounding_box, fill='red', outline='red', width=1)
        convolved.show()
    
    return ktps_list


###############################################################################
# Main function
def main():

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Images", help = "Input path to the image folder")
    parser.add_argument("-m", "--InitialMasks", help = "Input path to the image folder")
    parser.add_argument("-b", "--UseInitialMasks", help = "Bool if use initial masks")
    parser.add_argument("-t", "--MaskThreshold", help = "Input mask threshold")
    parser.add_argument("-a", "--Approach", help = "random_points")
    parser.add_argument("-n", "--NumberKpts", help = "random_points or ...", type=int)    
    parser.add_argument("-s", "--Silent", help = "Silent mode")
    parser.add_argument("-o", "--Output", help = "Output directory")
    args = parser.parse_args()
    

    im_folder = Path(args.Images)
    initial_mask_path = Path(args.InitialMasks)
    use_ini_masks = args.UseInitialMasks
    mask_threshold = int(args.MaskThreshold)
    approach = args.Approach
    n_kpts = args.NumberKpts
    silent = args.Silent
    out_dir = args.Output


    img_list = os.listdir(im_folder)
    kpts_dict = {}
    for img in img_list:
        path_to_img = im_folder / "{}".format(img)
        ktps_list = LocalFeatures(path_to_img, mask_threshold, silent, initial_mask_path, use_ini_masks, approach, n_kpts)
        kpts_dict[img] = ktps_list

    print("Total processed images: {}".format(len(kpts_dict.keys())))

    print("Saving outputs ...")
    for img in kpts_dict.keys():
        with open(out_dir / Path("{}.txt".format(img)), 'w') as out_file:
            out_file.write("{} 128\n".format(len(kpts_dict[img])))
            for kpt in kpts_dict[img]:
                out_file.write('{} {} 0.00 0.00\n'.format(kpt[0], kpt[1]))
    print("Finish")


###############################################################################
# Driver function 
if __name__=="__main__": 
    main()
