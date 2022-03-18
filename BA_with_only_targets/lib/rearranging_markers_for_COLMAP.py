import numpy as np
import os

def rearranging_markers_for_COLMAP(path):

    current_directory = os.getcwd()
    os.mkdir('{}/markers_coordinates_COLMAP_format'.format(current_directory))
    print('current_directory: ', current_directory)
    images = os.listdir('{}/{}'.format(current_directory, path))
    print('images: ', images)
    
    for image in images:
    
        image_path = '{}/{}/{}'.format(current_directory, path, image)
        print('image_path: ', image_path)
        file = np.loadtxt(image_path, dtype = float, delimiter = ',', usecols = (1,2))
        print(file)
        
        new_file = open('{}/{}/{}.txt'.format(current_directory, 'markers_coordinates_COLMAP_format', image[:-4]),'w')
        
        new_file.write('{} 128\n'.format(file.shape[0]))
        for k in range(0, file.shape[0]):
            new_file.write('{} {} {} {}\n'.format(file[k,0], file[k,1], '0.000000', '0.000000'))
            
        new_file.close()
        
    