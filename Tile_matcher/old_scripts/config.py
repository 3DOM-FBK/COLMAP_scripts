### UTILIZZO
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM\Python_scripts\CNN_Python
# >python 3domPipeline.py

import os

### INPUT IMAGES
image_set = []
image_set = os.listdir(r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\sample_project\imgs") # Specifica le immagini

### INPUT FOLDERS
desc_path_folder = r'C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\sample_project\desc'
image_path_folder = r'C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\sample_project\imgs'
gcp_path_folder = r'C:\Users\Luscias\Desktop\buttare\prova\empty'

### OUTPUT FOLDERS
converted_desc_path_folder = r'C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\sample_project\colmap_desc'
raw_matches_folder = r'C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\sample_project\matches'

### OTHER OPTIONS
res_factor = 1/1 #1500/6048 # Rapporto tra la larghezza dell'immagine usata in COLMAP e la larghezza dell'immagine su cui sono stati individuati i GCP
gcp_bool = False
descriptor = 'KeyNet' # 'D2Net' 'LFNet', 'ASLFeat', 'R2D2', 'KeyNet', 'SIFTopenCV', 'SuperPoint' or 'ORBopenCV' or 'PhotoMatch3DOM'
matching = 'BruteForce'
matching_distance = 'L2' # 'L2' or 'NORM_HAMMING'
matching_strategy = 'intersection' # 'intersection' or 'union' or 'unidirectional'
ratio_thresh_LRT = 0.80
print_debug = False
check = 'Lowe_ratio_test' # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
nmatches = 100000
crossCheck_bool = True
n_kp_input_SIFT = 8000 # Only with 'descriptor flag' = 'SIFTopenCV'
n_kp_input_ORB = 8000 # Only with 'descriptor flag' = 'ORBopenCV'



def main():
    print('image_set:  {}'.format(image_set))
  

# driver function 
if __name__=="__main__": 
    main()