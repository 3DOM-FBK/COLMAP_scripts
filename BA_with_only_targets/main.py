### GOPRO EVALUATION
print('\nGOPRO EVALUATION')
print('\main.py')

### Create a conda environment named opencv2
# In fase di installazione aprire anaconda prompt come amministratore
# >conda create --name opencv
# >conda activate opencv
# >conda install -c conda-forge opencv
# >conda install -c anaconda pandas
# >conda install -c conda-forge matplotlib
# >conda deactivate opencv

### Utilizzo
# Set images and options in config.py
# >conda activate opencv
# >cd C:\Users\Luscias\Desktop\3DOM
# >python main.py

# Importing libraries
print('\nImporting libraries ...')
import cv2
import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

# Importing other scripts
print('\nImporting other scripts ...')
import config
from lib import convert_markers_format
from lib import rearranging_markers_for_COLMAP
from lib import matching

# Main
if config.bool_sorting_PS_markers == True: convert_markers_format.ConvertMarkersFormat(config.PS_marker_path)
if config.bool_rearranging_markers_for_COLMAP == True: rearranging_markers_for_COLMAP.rearranging_markers_for_COLMAP(config.folder_markers_camera_path)
if config.bool_matching == True: matching.Matching(config.folder_markers_camera_path)

# END
print('\nEND')