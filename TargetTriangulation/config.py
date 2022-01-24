### TARGET TRIANGULATION
### 3DOM - FBK - TRENTO - ITALY
# Configuration file
# Please, change the input directories with yours.
# Note: Set 0.5 for the image_translation_vector_X and image_translation_vector_Y parameters, when you mark targets with OpenCV or other tools which have the reference system placed in the middle of the first pixel, while COLMAP has the reference system placed in the upper-left corner.

COLMAP_EXE_PATH = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\COLMAP_3_6_windows"
AlignCC_PATH = r"..\AlignCC_for_windows"
#database_path = r".\input\colmap_sparse\database.db"
image_folder = r".\input_test\imgs"
projection_folder = r".\input_test\img_projections"
sparse_model_path = r".\input_test\colmap_sparse"
ground_truth_path = r".\input_test\Ground_Truth.txt"

image_file_extension = ".jpg"
projection_delimiter = " "
image_reduction_factor = 1500/6048                      # 1500/6048 Ratio between the image resolution used in COLMAP and the image res targets were extracted
image_translation_vector_X = 0.5                        # X and Y value must be the same
image_translation_vector_Y = 0.5                        # X and Y value must be the same
INFO = True                                             # Get more info printed when script is running
DEBUG = True
DEBUG_level = 5                                         # 0:CHECKS
                                                        # 1:CONVERT TARGET PROJECTIONS IN COLMAP FORMAT
                                                        # 2:TARGETS MATCHING
                                                        # 3:INITIALIZE A NEW DATABASE
                                                        # 4:TARGET TRIANGULATION
                                                        # 5:FULL PIPELINE







