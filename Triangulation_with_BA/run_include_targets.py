# 3DOM - COLMAP target triangulation
# COLMAP_GCPs_v3
#
# This is the main script.


import os
import argparse
import sqlite3
import shutil
import gzip
import numpy as np

from config import images_folder
from config import database_path
from config import target_projections_folder
from config import reduction_factor
from config import min_num_matches
from config import translation_vector
from config import debug

from lib import include_matches
from lib import export_p3D


def main():
    print("\n**********************************")
    print("3DOM - COLMAP TARGET TRIANGULATION")
    print("**********************************\n")
    print("Path to images folder:\t\t\t\t\t", images_folder)
    print("Path to the COLMAP database:\t\t\t\t", database_path)
    print("Path to target projections (in image coordinates):\t", target_projections_folder)
    print("reduction_factor:\t\t\t\t\t", reduction_factor)
    print("min_num_matches:\t\t\t\t\t", min_num_matches, "\n")
    
    
    # Check if input file are correct and/or exist
    try:
        if database_path[-3:] != ".db":
            print("Error: Put in the configuration file the path to a COLMAP database.")
            quit()
        file = open(database_path, 'r')
        file.close()
    except:
        print("Error: Database do not exist.")
        quit()

    if os.path.isdir(images_folder) == False:
        print("Error: images folder do not exist")
        quit()
    
    if os.path.isdir(target_projections_folder) == False:
        print("Error: the target_projections_folder do not exist")
        quit()
        
    # Check if the file extension and the file name of target projections are correct
    images_list = os.listdir(images_folder)
    gcps_projection_list = os.listdir(target_projections_folder)
     
    for gcps_item in gcps_projection_list:
        boolean = False
        n = 0
        while boolean == False and n<len(images_list):
            if images_list[n] == gcps_item[:-4]:
                boolean = True
                break
            else :
                n += 1
        if boolean == False:
            print("Error: target projection must be IMAGE_NAME.jpg.txt instead of {} {}".format(images_list[n-1], gcps_item))
            quit()
        
    # User choose if to follow the full pipeline or only the last part (reading only 3D coordinates of the targets)
    ris = input("\nIf you want extract only the 3D coordinates of GCPs type '3Dcoordinates'. \nIf you want run the entire pipeline type 'pipeline'. Otherwise 'quit'.\nWaiting for user input:\t")
    
    if ris == "quit":
        quit()
    
    elif ris == "pipeline":    # Running the entire pipeline
        
        # Check if the output folder exists or if it is empty
        if os.path.isdir(r".\output") == False:
            os.mkdir(r".\output")
            print("\nOutput folder created.")
        
        output_folder = r".\output"
        
        if not os.listdir(r".\output"):
            print('The output directory is empty.')
        else:
            print("Remeber to empty the output folder before continuing.")
            quit()
        
        # Including targets in the matches from the COLMAP database
        print("Output files:")
        print(r"{}\desc".format(output_folder))
        print(r"{}\matches.txt".format(output_folder))
        print(r"{}\gcps_projections_id.txt".format(output_folder))
        include_matches.main(
                                target_projections_folder,
                                database_path,
                                r"{}\desc".format(output_folder),
                                r"{}\matches.txt".format(output_folder),
                                r"{}\gcps_projections_id.txt".format(output_folder),
                                min_num_matches,
                                reduction_factor,
                                translation_vector,
                                debug
                                )
                                
        ris = input("\nRun COLMAP using the just rewritten keypoints ('desc' folder) and matches. When you will be ready, type 'continue' else press unother button to quit. \nWaiting for user input: ")
        
        # Finding the 3D coordinates triangulated by COLMAP from the points3D.txt file
        if ris == "continue":
            points3D_path = input("Type the path to the points3D.txt file: ")
            export_p3D.main(
                            r"{}".format(points3D_path), r"{}\target_3D_coordinates_not_scaled.txt".format(output_folder), r"{}\gcps_projections_id.txt".format(output_folder)
                            )
        
        else:
            quit()
    
    elif ris == "3Dcoordinates":
        # Finding the 3D coordinates triangulated by COLMAP from the points3D.txt file
        output_folder = r".\output"
        points3D_path = input("Type the path to the points3D.txt file: ")
        export_p3D.main(r"{}".format(points3D_path), r"{}\target_3D_coordinates_not_scaled.txt".format(output_folder), r"{}\gcps_projections_id.txt".format(output_folder))

    else:
        print("\nError: Type 'pipeline' or '3Dcoordinates' or 'quit'")
        quit()
    
    
if __name__ == "__main__":
    main()