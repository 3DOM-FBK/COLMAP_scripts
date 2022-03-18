# Input/Output folders
image_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\prova\all_imgs"
desc_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\outs"
colmap_desc_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\colmap_desc"
matches_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\matches"
tile_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Keypoints\RootSIFT_COLMAP\prova\tiles"

# Matching parameters
local_feature = "KeyNet" # "LFNet" or "KeyNet" or "photomatch"
cross_check = True
check = 'Lowe_ratio_test'    # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
matching_distance = 'L2'
matching_strategy = 'intersection'
ratio_thresh = 0.80
pool_N = 4                                          # nuber of logical processors to be used
