### TARGET TRIANGULATION
### 3DOM - FBK - TRENTO - ITALY
# Configuration file
# Please, change the input directories with yours.
# Note: Set 0.5 for the image_translation_vector_X and image_translation_vector_Y parameters, when you mark targets with OpenCV or other tools which have the reference system placed in the middle of the first pixel, while COLMAP has the reference system placed in the upper-left corner.
# GCPs LABEL MUST BE AN INTEGER!!!

COLMAP_EXE_PATH = r"C:\Users\User\Desktop\Luca\COLMAP\COLMAP_3_6_windows" # Path to the COLMAP executable
AlignCC_PATH = r"..\AlignCC_for_windows" # Path to the AlignCC_for_windows folder, this part is usefull if you want automatically compare your script using the Cloud Compare libraries
#database_path = r".\input\colmap_sparse\database.db"
image_folder = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\imgs" # Path to the image folder used for running the sparse COLMAP reconstruction
projection_folder = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\target_projections"
sparse_model_path = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\KeyNetAffNetHardNet\colmap_filtered0.2pix"
ground_truth_path = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\gcp_list.txt"

image_file_extension = ".jpg"
projection_delimiter = ","
image_reduction_factor = 1/4.01066666666              # 1500/6048 Ratio between the image resolution used in COLMAP and the image res targets were extracted
image_translation_vector_X = 0                        # X and Y value must be the same
image_translation_vector_Y = 0                        # X and Y value must be the same
INFO = False                                             # Get more info printed when script is running
DEBUG = False
DEBUG_level = 5                                         # 0:CHECKS
                                                        # 1:CONVERT TARGET PROJECTIONS IN COLMAP FORMAT
                                                        # 2:TARGETS MATCHING
                                                        # 3:INITIALIZE A NEW DATABASE
                                                        # 4:TARGET TRIANGULATION
                                                        # 5:FULL PIPELINE







