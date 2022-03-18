import numpy as np
import os

def ConvertMarkersFormat(path):

    data_matrix_labels = np.loadtxt(path, dtype = str, delimiter = ',', usecols = (0,1))
    data_matrix_values = np.loadtxt(path, dtype = float, delimiter = ',', usecols = (2,3))
    print(data_matrix_labels)
    print(data_matrix_values)
    current_directory = os.getcwd()
    os.mkdir('{}/markers_coordinates'.format(current_directory))
    
    for i in range(0, data_matrix_labels.shape[0]):
        current_image = data_matrix_labels[i, 1]
        files = os.listdir('{}/markers_coordinates'.format(current_directory))
        if '{}.txt'.format(current_image) not in files: 
            new_file = open('{}/markers_coordinates/{}.txt'.format(current_directory, current_image),"w")
            new_file.close
            
    files = os.listdir('{}/markers_coordinates'.format(current_directory))
    for i in range(0, data_matrix_labels.shape[0]):
        current_target = data_matrix_labels[i, 0]
        current_image = data_matrix_labels[i, 1]
        current_image_output_file = '{}/markers_coordinates/{}.txt'.format(current_directory, current_image)
        file = open(current_image_output_file, 'a')
        file.write('{},{},{}\n'.format(current_target, data_matrix_values[i, 0], data_matrix_values[i, 1]))
        file.close()
        