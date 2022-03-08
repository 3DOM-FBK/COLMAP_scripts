0. REMEMBER TO CANCEL THE FOLDER "__pycache__" IF IT EXISTS
1. Put in the input folder (or create it in the same folder of the config.py and run_include_targets.py files):
	a. a folder with the images processed in COLMAP (each image file called IMG_NAME.jpg)
	b. the COLMAP database (DATABASE_NAME.db)
	c. a folder with the target projections (a txt file for each image called IMG_NAME.jpg.txt)
	   with the format "gcp_label X Y n", where n is the counter of the projections:
		gcp21 4980 2195 1
		gcp16 1848 1866 2
		gcp17 561 564 3

2. Create the output folder in the same directory of the input one, and remember to keep it empty before each run of the mail script run_include_targets.py
3. Check if you have installed all the python library in the scripts
4. Now in the console run >python run_include_targets.py
5. Run COLMAP
6. Create a new project
7. Import the keypoints selecting the folder ./output/desc
8. Import the matches selecting the file ./output/matches.txt
9. Run the reconstruction button in COLMAP
10. Save the results in txt format
11. In the python console type the path to the points3D.txt file
12. In the ouput folder you will find the 3D coordinates of the targets