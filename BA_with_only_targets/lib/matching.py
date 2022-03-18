import numpy as np
import os

def Matching(path_to_images):

    current_directory = os.getcwd()
    images = os.listdir('{}/{}'.format(current_directory, path_to_images))
    file_matches = open('{}/matches.txt'.format(current_directory), 'w')
    raw_matches = []
    
    for image1_count in range(0, len(images)-1):
    
        image1_kps = np.loadtxt('{}/{}/{}'.format(current_directory, path_to_images, images[image1_count]), dtype = float, delimiter = ',', usecols = (0,1,2))
        #print(image1_kps)
    
        for image2_count in range(image1_count+1, len(images)):
        
            image2_kps = np.loadtxt('{}/{}/{}'.format(current_directory, path_to_images, images[image2_count]), dtype = float, delimiter = ',', usecols = (0,1,2))
            #print(image2_kps)
            matches_matrix = np.array(['{}'.format(images[image1_count][:-4]), '{}'.format(images[image2_count][:-4])])
            print('Working on: ', images[image1_count], images[image2_count])
            
            for k in range(0, image1_kps.shape[0]):
            
                for j in range(0, image2_kps.shape[0]):
                
                    if image1_kps[k, 0] == image2_kps[j, 0]:
                        
                        other_match = np.array([k, j])
                        #print('matches_matrix\n', matches_matrix, matches_matrix.shape)
                        #print('other_match\n', other_match, other_match.shape)
                        matches_matrix = np.vstack((matches_matrix, other_match))
    
            raw_matches.append(matches_matrix)
            #print(raw_matches)
        
        for item in raw_matches:
        
            print('item: \n', item)
            print('type: \n', type(item))
            print('shape: \n', item.shape)
            
            for i in range(0, item.shape[0]):
            
                file_matches.write("%s %s\n" % (item[i, 0], item[i, 1]))
                
            file_matches.write('\n')
        
        raw_matches = []
        
    file_matches.close()       
        
        
        #raw_matches.append(matches_matrix)
    
        
    #print('RAW_MATCHES:\n', len(raw_matches))
    #print(raw_matches)
    
    #for item in raw_matches:
    #    file_matches.write("%s\n" % item)
        
    #file_matches.close()
        
    