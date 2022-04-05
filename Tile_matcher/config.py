# Input/Output folders
image_folder = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR_TIME\RoRD\imgs"
desc_folder = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR_TIME\RoRD\descs"
colmap_desc_folder = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR_TIME\RoRD\colmap_desc"
matches_folder = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR_TIME\RoRD\matches"
tile_folder = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR_TIME\matches_on_images\tiles"
custom_pairs = r"C:\Users\Luscias\Desktop\3DOM\ISPRS2022_EUROSDR\SceneViews.json"

# Matching parameters
multhreading = False # if False, pool_N must be 1
tiling = False
max_kpts_per_tile = 3000
matching_approach = "exhaustive" # "exhaustive" or "custom"
local_feature = "RoRD" # "LFNet", "KeyNet", "photomatch", "RootSIFT", "RoRD" or "D2Net"
cross_check = True
check = 'without_Lowe_ratio_test'    # 'without_Lowe_ratio_test' or 'Lowe_ratio_test'
matching_distance = 'L2'
matching_strategy = 'intersection'
ratio_thresh = 0.95
pool_N = 1                                          # nuber of logical processors to be used
debug = False

# Print settings
print("matcher.py configuration:")
print("\nINPUT/OUTPUT DIR:")
print("image_folder\t\t\t", image_folder)
print("desc_folder\t\t\t", desc_folder)
print("colmap_desc_folder\t\t", colmap_desc_folder)
print("matches_folder\t\t\t", matches_folder)
print("tile_folder\t\t\t", tile_folder)
print("custom_pairs\t\t\t", custom_pairs)

print("\nOptions:")
print("multhreading\t\t\t", multhreading)
print("tilining\t\t\t", tiling)
print("max_kpts_per_tile\t\t", max_kpts_per_tile)
print("matching_approach\t\t", matching_approach)
print("local_feature\t\t\t", local_feature)
print("cross_check\t\t\t", cross_check)
print("check\t\t\t\t", check)
print("matching_distance\t\t", matching_distance)
print("matching_strategy\t\t", matching_strategy)
print("ratio_thresh\t\t\t", ratio_thresh)
print("pool_N\t\t\t\t", pool_N)
print("debug\t\t\t\t", debug)

userI = input("\nDo you want to continue? y/n\n")
if userI != "y":
    quit()