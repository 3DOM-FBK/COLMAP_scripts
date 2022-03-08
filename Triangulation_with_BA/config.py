# 3DOM - COLMAP target triangulation
# COLMAP_GCPs_v3
#
# Configuration file
#
# >cd C:\Users\Luscias\Desktop\3DOM\Python_scripts\COLMAP_GCPs\COLMAP_GCPs_v3
# >python run_include_targets.py

# Path to images folder
images_folder = r".\input\ventimiglia_imgs_nad"

# Path to the COLMAP database
database_path = r".\input\temp.db"

# Path to target projections (in image coordinates)
target_projections_folder = r".\input\ventimiglia_target_projections_nad"

# Reduction factor - type the ratio between the image resolution used in COLMAP and
# the resolution in which targets have been marked.
reduction_factor = 1500/6048    # for Ventimiglia e Muro dataset reduction_factor = 1500/6048

# Min number of matches for pair of images, otherwise matches of the pair which has not enough correspondences will not be reported in the matches.txt file
min_num_matches = 15

# Translation vector between image coordinate system
translation_vector = 0.5

# If you want print more info for an easier debug
debug = False

