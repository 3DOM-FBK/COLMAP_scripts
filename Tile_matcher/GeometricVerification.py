# USAGE
# python GeometricVerification.py find_fundamental ./images ./kpts_folder ./matches.txt ./out_folder --error_threshold 3 --debug False
# python GeometricVerification.py evaluate_matches ./images ./kpts_folder ./matches.txt ./out_folder --error_threshold 3 --debug False --f_matrix ./f_matrix.txt

from PIL import Image, ImageDraw
from pathlib import Path
import numpy as np
import pydegensac
import argparse
import os



### MAIN STARTS HERE
if __name__ == "__main__":
    # I/O foders and options
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Digit find_fundamental or evaluate_matches")
    parser.add_argument("image_folder", help="Input path to a folder with only two images")
    parser.add_argument("kpts_folder", help="Input keypoint folder using the COLMAP format")
    parser.add_argument("matches", help="Input matches.txt using the COLMAP format")
    parser.add_argument("out_folder", help="Path to the output folder")
    parser.add_argument("-e","--error_threshold", help="Input matches.txt using the COLMAP format", default = 4, type=int)
    parser.add_argument("-d","--debug", help="True or False", default = False, type=bool)
    parser.add_argument("-f","--f_matrix", help="Path to the F_matrix.txt file")
    args = parser.parse_args()

    command = args.command
    image_folder = Path(r"{}".format(args.image_folder))
    kpts_folder = Path(r"{}".format(args.kpts_folder))
    matches_file = Path(r"{}".format(args.matches))
    out_folder = Path(r"{}".format(args.out_folder))
    error_threshold = args.error_threshold
    f_matrix_path = Path(r"{}".format(args.f_matrix))
    debug = args.debug

    # Find the Foundamental matrix from input matches
    if command == "find_fundamental":
        kpts_dict = {}
        matches_dict = {}

        imgs_list = os.listdir(image_folder)
    
        # Importing keypoints from file
        for img in imgs_list:
            with open("{}/{}.txt".format(kpts_folder, img),'r') as kpt_file:
                kpts_dict[img] = np.loadtxt(kpt_file, delimiter=' ', skiprows=1, usecols=(0,1))

        # Importing matches from file
        controller = True
        with open(matches_file, 'r') as match_file:
            lines = match_file.readlines()
            for line in lines:
                if line == '\n':
                    controller = False
                else:
                    line = line.strip()
                    elem1, elem2 = line.split(' ', 1)
                    if elem1 in imgs_list:
                        img1 = elem1
                        img2 = elem2
                        pair = '{} {}'.format(img1, img2)
                        matches_dict[pair] = np.empty((2,2), dtype=float)
                    else:
                        matches_dict[pair] = np.vstack((matches_dict[pair],     np. array([elem1, elem2], ndmin=2)))

        for m in matches_dict:
            matches_dict[m] = matches_dict[m][2:, :]

        # Geometric verification
        verified_kpts = {}
        verified_matches = {}
        for key in matches_dict:
            match1 = matches_dict[key][:, 0]
            match2 = matches_dict[key][:, 1]
            match1 = match1.astype(np.int)
            match2 = match2.astype(np.int)
            img1, img2 = key.split(" ", 1)
            feat1 = kpts_dict[img1]
            feat2 = kpts_dict[img2]

            kpt_left = feat1[match1, :]
            kpt_right = feat2[match2, :]

            F, inliers = pydegensac.findFundamentalMatrix(kpt_left,     kpt_right,  error_threshold, 0.99, 10000)

            if img1 not in verified_kpts.keys():
                verified_kpts[img1] =  kpt_left[inliers]
            if img2 not in verified_kpts.keys():
                verified_kpts[img2] =  kpt_right[inliers]
            verified_matches[key] = np.array([(m, m) for m in range (kpt_left    [inliers].shape[0])])
            print(verified_matches[key])
            print(kpt_left[inliers].shape, kpt_left[inliers].shape)

        for img in imgs_list:
            with open("{}/{}.txt".format(out_folder, img), "w")   as    colmap_desc_file:
                colmap_desc_file.write("{} {}\n".format(verified_kpts[img]. shape    [0], 128))
                for row in range(verified_kpts[img].shape[0]):
                    colmap_desc_file.write("{} {} 0.000000 0.000000\n". format   (verified_kpts[img][row, 0], verified_kpts[img] [row, 1]))
                colmap_desc_file.write("\n")    

        with open("{}/verified_matches.txt".format  (out_folder),    "w") as colmap_matches:
            for math_pair in verified_matches:
                colmap_matches.write("{}\n".format(math_pair))
                for row in range(verified_matches[math_pair].shape[0]):
                    colmap_matches.write("{} {}\n".format(verified_matches      [math_pair][row, 0], verified_matches[math_pair][row,   1]))
                colmap_matches.write("\n")

        with open("{}/F_matrix.txt".format(out_folder),    "w") as F_file:
            F_file.write("{} {} {} {} {} {} {} {} {}".format(F[0,0], F[0,1], F[0,2], F[1,0], F[1,1], F[1,2], F[2,0], F[2,1], F[2,2]))
        
        if debug == True:
            print('F', F)
            x1, y1 = 292, 191
            m = np.array([[x1], [y1], [1]])
            line_params = F @ m
            a, b, c = line_params[0,0], line_params[1,0], line_params[2,0]
            img2_pil = Image.open(r"{}/{}".format(image_folder, imgs_list[1]))
            line_extrema = [(0, -c/b),(-c/a, 0)]
            print(line_extrema)
            print((img2_pil.width, img2_pil.height))
            draw = ImageDraw.Draw(img2_pil)
            draw.line(line_extrema, fill=255)
            img2_pil.show()


    elif command == "evaluate_matches":
        print("Importing F:")
        with open(r"{}".format(f_matrix_path), 'r') as f_matrix_file:
            line = f_matrix_file.readlines()
            f1, f2, f3, f4, f5, f6, f7, f8, f9 = line[0].split(" ", 8)
            F = np.array([
                            [float(f1), float(f2), float(f3)],
                            [float(f4), float(f5), float(f6)],
                            [float(f7), float(f8), float(f9)]
                                                                ])
            print(F)
        
        kpts_dict = {}
        matches_dict = {}
        imgs_list = os.listdir(image_folder)
    
        # Importing keypoints from file
        for img in imgs_list:
            with open("{}/{}.txt".format(kpts_folder, img),'r') as kpt_file:
                kpts_dict[img] = np.loadtxt(kpt_file, delimiter=' ', skiprows=1, usecols=(0,1))

        # Importing matches from file
        controller = True
        with open(matches_file, 'r') as match_file:
            lines = match_file.readlines()
            for line in lines:
                if line == '\n':
                    controller = False
                else:
                    line = line.strip()
                    elem1, elem2 = line.split(' ', 1)
                    if elem1 in imgs_list:
                        img1 = elem1
                        img2 = elem2
                        pair = '{} {}'.format(img1, img2)
                        matches_dict[pair] = np.empty((2,2), dtype=float)
                    else:
                        matches_dict[pair] = np.vstack((matches_dict[pair],     np. array([elem1, elem2], ndmin=2)))

        for m in matches_dict:
            matches_dict[m] = matches_dict[m][2:, :]

        # Evaluation
        verified_kpts_img1 = []
        verified_kpts_img2 = []
        verified_matches = []
        cont = 0
        for key in matches_dict:
            match1 = matches_dict[key][:, 0]
            match2 = matches_dict[key][:, 1]
            match1 = match1.astype(np.int)
            match2 = match2.astype(np.int)
            img1, img2 = key.split(" ", 1)
            feat1 = kpts_dict[img1]
            feat2 = kpts_dict[img2]

            kpt_left = feat1[match1, :]
            kpt_right = feat2[match2, :]
        
        for k in range(kpt_left.shape[0]):
            x1 = kpt_left[k, 0]
            y1 = kpt_left[k, 1]

            x2 = kpt_right[k, 0]
            y2 = kpt_right[k, 1]

            m = np.array([[x1], [y1], [1]])
            line_params = F @ m
            a, b, c = line_params[0,0], line_params[1,0], line_params[2,0]
            #img2_pil = Image.open(r"{}/{}".format(image_folder, imgs_list[1]))
            #line_extrema = [(0, -c/b),(-c/a, 0)]
            #draw = ImageDraw.Draw(img2_pil)
            #draw.line(line_extrema, fill=255)
            #draw.ellipse(((x2-3, y2-3), (x2+3, y2+3)), fill='red', #outline='blue')
            #img2_pil.show()

            distance_point_line = np.absolute(a*x2 + b*y2 + c) / np.sqrt(a**2 + b**2)

            print(distance_point_line)

            if distance_point_line < error_threshold:
                verified_kpts_img1.append((x1, y1))
                verified_kpts_img2.append((x2, y2))
                verified_matches.append("{} {}".format(cont, cont))
                cont += 1

        with open("{}/{}.txt".format(out_folder, img1), "w")   as   colmap_desc_file:
            colmap_desc_file.write("{} {}\n".format(len(verified_kpts_img1), 128))
            for point in verified_kpts_img1:
                colmap_desc_file.write("{} {} 0.000000 0.000000\n".format   (point[0], point[1]))
            colmap_desc_file.write("\n")  

        with open("{}/{}.txt".format(out_folder, img2), "w")   as   colmap_desc_file:
            colmap_desc_file.write("{} {}\n".format(len(verified_kpts_img2), 128))
            for point in verified_kpts_img2:
                colmap_desc_file.write("{} {} 0.000000 0.000000\n".format   (point[0], point[1]))
            colmap_desc_file.write("\n") 

        with open("{}/verified_matches.txt".format  (out_folder),    "w") as colmap_matches:
            colmap_matches.write("{} {}\n".format(img1, img2))
            for element in verified_matches:
                colmap_matches.write("{}\n".format(element))
            colmap_matches.write("\n")

    else:
        print("Error! Change command")
        quit()




#error_threshold = 10.0#
#colmap_desc =  #r'C:\Users\Luscias\Desktop\NowAndThen\demilked_SanFrancisco\GroundTr#th\k pts'
#matches =  #r'C:\Users\Luscias\Desktop\NowAndThen\demilked_SanFrancisco\GroundTr#th\m atches.txt'#
#verified_kpts_folder = #r"C:\Users\Luscias\Desktop\NowAndThen\demilked_SanFrancisco\GroundTr#th\v    er_kpts"
#verified_matches_folder =  #r"C:\Users\Luscias\Desktop\NowAndThen\demilked_SanFrancisco\GroundTr#th\v er_matches"#
## MAIN STARTS HERE
#kpts_dict = {}
#matches_dict = {}#
#imgs_list = os.listdir(colmap_desc)
#for c, item in enumerate(imgs_list):
#    imgs_list[c] = item[:-4]#
## Importing keypoints from file
#for img in imgs_list:
#    with open("{}/{}.txt".format(colmap_desc, img),'r') as kpt_file:
#        kpts_dict[img] = np.loadtxt(kpt_file, delimiter=' ',#skiprows=1,    usecols=(0,1))
#        #print(kpts_dict)#
## Importing matches from file
#controller = True
#with open(matches, 'r') as match_file:
#    lines = match_file.readlines()
#    for line in lines:
#        if line == '\n':
#            controller = False
#        else:
#            line = line.strip()
#            elem1, elem2 = line.split(' ', 1)
#            if elem1 in imgs_list:
#                img1 = elem1
#                img2 = elem2
#                pair = '{} {}'.format(img1, img2)
#                matches_dict[pair] = np.empty((2,2), dtype=float)
#            else:
#                matches_dict[pair] = np.vstack((matches_dict[pair],#np. array([elem1, elem2], ndmin=2)))#
#for m in matches_dict:
#    matches_dict[m] = matches_dict[m][2:, :]#
## Geometric verification
#verified_kpts = {}
#verified_matches = {}
#for key in matches_dict:
#    match1 = matches_dict[key][:, 0]
#    match2 = matches_dict[key][:, 1]
#    match1 = match1.astype(np.int)
#    match2 = match2.astype(np.int)
#    img1, img2 = key.split(" ", 1)
#    feat1 = kpts_dict[img1]
#    feat2 = kpts_dict[img2]#
#    print('match1', match1)
#    print('match2', match2)
#    print('feat1', feat1)
#    print('feat2', feat2)#
#    #print(match2[:5])
#    #print(feat2[:5, :])#
#    kpt_left = feat1[match1, :]
#    kpt_right = feat2[match2, :]
#    #print(kpt_right[:5, :])#
#    #H, inliers = pydegensac.findHomography(kpt_left, kpt_right,   #error_threshold, 0.99, 10000)
#    F, inliers = pydegensac.findFundamentalMatrix(kpt_left,#kpt_right,  error_threshold, 0.99, 10000)#
#    if img1 not in verified_kpts.keys():
#        verified_kpts[img1] =  kpt_left[inliers]
#    if img2 not in verified_kpts.keys():
#        verified_kpts[img2] =  kpt_right[inliers]
#    verified_matches[key] = np.array([(m, m) for m in rang#(kpt_left    [inliers].shape[0])])
#    print(verified_matches[key])
#    print(kpt_left[inliers].shape, kpt_left[inliers].shape)#
#for img in imgs_list:
#    with open("{}/{}.txt".format(verified_kpts_folder, img), "w")#as    colmap_desc_file:
#        colmap_desc_file.write("{} {}\n".format(verified_kpts[img]#shape    [0], 128))
#        for row in range(verified_kpts[img].shape[0]):
#            colmap_desc_file.write("{} {} 0.000000 0.000000\n"#format   (verified_kpts[img][row, 0], verified_kpts[img#[row, 1]))
#        colmap_desc_file.write("\n")    #
#with open("{}/verified_matches.txt".forma#(verified_matches_folder),    "w") as colmap_matches:
#    for math_pair in verified_matches:
#        colmap_matches.write("{}\n".format(math_pair))
#        for row in range(verified_matches[math_pair].shape[0]):
#            colmap_matches.write("{} {}\n".format(verified_matches #[math_pair][row, 0], verified_matches[math_pair][row,#1]))
#        colmap_matches.write("\n")#
#print('F', F)
#x1, y1 = 292, 191
#m = np.array([
#                [x1],
#                [y1],
#                [1]
#                    ])
#line_params = F @ m
#a, b, c = line_params[0,0], line_params[1,0], line_params[2,0]#
#img2_pil = Image.open  #(r"C:\Users\Luscias\Desktop\NowAndThen\demilked_SanFrancisco\imgs\Sa#Fran  cisco2.png")#
#line_extrema = [
#            (0, -c/b),
#            #(img2_pil.width, (-c-a*img2_pil.width)/b),
#            (-c/a, 0),
#            #((-c-b*img2_pil.height)/a, img2_pil.height)
#                ]#
#print(line_extrema)#
##line_extrema = [element for element in line_extrema if element[0]>0#or     element[1]>0]#
#print(line_extrema)
#print((img2_pil.width, img2_pil.height))#
#draw = ImageDraw.Draw(img2_pil)
#draw.line(line_extrema, fill=255)
#img2_pil.show()
