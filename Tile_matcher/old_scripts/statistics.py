# Import packages
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

# Input/Output
file_1 = r'res_quadratic.txt'
file_2 = r'res_quadratic_more_points.txt'
#threshold = 0.05

# Database initialization
#cont = 0
#matrix = np.empty((0,4))

# Read input file
matrix_1 = np.loadtxt(file_1, dtype = 'float', comments = '//', delimiter = ',', usecols = (0,1,2,4)) # max_rows = 1000
print(file_1)
print(matrix_1[:10,:])

#with open(input_file,'r') as file :
#    file = file.readlines()[1:100]
#    for line in file :
#        cont = cont + 1
#        #line = line[:-1]
#        X, Y, Z, colour, distance = line.split(',', 4)
#        X = float(X)
#        Y = float(Y)
#        Z = float(Z)
#        distance = float(distance)
#        if distance < threshold : matrix = np.vstack([matrix, [X, Y, Z, distance]])

## Plot 3D points
#fig = plt.figure()
#ax = plt.axes(projection='3d')
#print(matrix.shape)
#xline = matrix[:, 0]
#yline = matrix[:, 1]
#zline = matrix[:, 2]
#ax.scatter3D(xline, yline, zline, 'gray')
#plt.show()

# Histogram
all_distances_1 = matrix_1[:, 3]

print(np.amax(all_distances_1))
print(np.amin(all_distances_1))

bins = np.linspace(0, 0.05, 100)
plt.hist(all_distances_1, bins, alpha = 0.5, label = 'quadratic', color = 'b')  # density=False would make counts
plt.axvline(all_distances_1.mean(), color='b', linestyle='dashed', linewidth=1)
plt.ylabel('# points')
plt.xlabel('Error C2C')
plt.xlim([0, 0.05])
#plt.legend(loc='upper right')
plt.show()

print('Valore medio:', all_distances_1.mean())