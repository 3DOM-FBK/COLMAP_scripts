from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

### INPUTS
txt_output = Path(r"G:\3DOM\13_Imgs_aeree\dortmund\lfnet\OPENCV_BA4pix_withPP") # Folder containing the COLMAP output in the txt format


### MAIN starts here
path_points3D_file = txt_output / "points3D.txt"

# Load all COLMAP 3D points

with open(path_points3D_file, "r") as points3D_file:
    lines = points3D_file.readlines()[3:]
    N_points = len(lines)
    points3D_matrix = np.empty((N_points, 9))
    
    for enum,line in enumerate(lines):
        line = line.strip()
        POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK = line.split(" ", 8)
        Track_elements = TRACK.split(" ")
        Track = len(Track_elements)/2
        points3D_matrix[enum][:] = POINT3D_ID, X, Y, Z, R, G, B, ERROR, Track
        
print(points3D_matrix)
print("mean track lenght:\t\t", np.mean(points3D_matrix[:,8]))
print("standard deviation MTL:\t", np.std(points3D_matrix[:,8]))


# Plot Histogram
data = points3D_matrix[:,8]
bins = np.linspace(0, 20, 20)
print(bins)
plt.hist(data, bins, alpha = 0.5, label = 'LF-Net\nMTL = 2.93\nstd=1.81', color = 'b')  # density=False would make counts
plt.axvline(data.mean(), color='b', linestyle='dashed', linewidth=1)
plt.ylabel('Absolute frequency')
plt.xlabel('Track Lenght')
plt.xlim([0, 20])
plt.legend(loc='upper right')
plt.show()