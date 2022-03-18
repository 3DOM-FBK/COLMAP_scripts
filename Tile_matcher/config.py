# Input/Output folders
image_folder = r"C:\Users\Luscias\Desktop\prova1000\imgs"
desc_folder = r"C:\Users\Luscias\Desktop\prova1000\desc"
colmap_desc_folder = r"C:\Users\Luscias\Desktop\prova1000\colmap_desc"
matches_folder = r"C:\Users\Luscias\Desktop\prova1000\matches"
tile_folder = r"C:\Users\Luscias\Desktop\prova1000\tiles"
custom_pairs = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR\SceneViews.json"

# Matching parameters
tiling = True
matching_approach = "exhaustive" # "exhaustive" or "custom"
local_feature = "RootSIFT" # "LFNet" or "KeyNet" or "photomatch" or "RootSIFT"
cross_check = True
check = 'Lowe_ratio_test'    # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
matching_distance = 'L2'
matching_strategy = 'intersection'
ratio_thresh = 0.85
pool_N = 2                                          # nuber of logical processors to be used
debug = True
