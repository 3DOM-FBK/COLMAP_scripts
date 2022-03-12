# Input/Output folders
image_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Tile_matcher\sample_project\imgs"
desc_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Tile_matcher\sample_project\desc"
colmap_desc_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Tile_matcher\sample_project\colmap_desc"
matches_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Tile_matcher\sample_project\matches"
tile_folder = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\Tile_matcher\sample_project\tiles"

# Matching parameters
local_feature = "photomatch" # "LFNet" or "KeyNet" or "photomatch"
cross_check = True
check = 'Lowe_ratio_test'    # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
matching_distance = 'L2'
matching_strategy = 'intersection'
ratio_thresh = 0.85
pool_N = 1                                          # nuber of logical processors to be used
