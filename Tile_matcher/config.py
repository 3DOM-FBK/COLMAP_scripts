# Input/Output folders
image_folder = r"C:\Users\User\Desktop\Luca\Projects\Aerial-images\aerial_trento\Trento_resized_JPG"
desc_folder = r"C:\Users\User\Desktop\Luca\Projects\Aerial-images\aerial_trento\lfnet\lfnet_descriptor"
colmap_desc_folder = r"C:\Users\User\Desktop\Luca\Projects\Aerial-images\aerial_trento\lfnet\colmap_desc"
matches_folder = r"C:\Users\User\Desktop\Luca\Projects\Aerial-images\aerial_trento\lfnet\colmap_matches"
tile_folder = r"C:\Users\User\Desktop\Luca\Projects\Aerial-images\aerial_trento\aerial_trento_tiles"

# Matching parameters
local_feature = "KeyNet" # "LFNet" or "KeyNet"
cross_check = True
check = 'without_Lowe_ratio_test'    # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
matching_distance = 'L2'
matching_strategy = 'intersection'
ratio_thresh = 0.85
pool_N = 1                                          # nuber of logical processors to be used
