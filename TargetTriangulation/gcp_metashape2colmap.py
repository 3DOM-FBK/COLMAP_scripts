import argparse
import numpy as np
import os

def ConvertGCPmetashape2colmap(metashape_gcp_folder, output_folder):

    target_metashape = r"{}".format(metashape_gcp_folder)

    data_matrix_labels = np.loadtxt(target_metashape, dtype = str, delimiter = ',', usecols = (0,1))
    data_matrix_values = np.loadtxt(target_metashape, dtype = float, delimiter = ',', usecols = (2,3))
    print(data_matrix_labels)
    print(data_matrix_values)
    
    for i in range(0, data_matrix_labels.shape[0]):
        current_image = data_matrix_labels[i, 1]
        files = os.listdir(output_folder)
        if '{}.txt'.format(current_image) not in files: 
            new_file = open('{}/{}.txt'.format(output_folder, current_image),"w")
            new_file.close
            
    files = os.listdir(output_folder)
    for i in range(0, data_matrix_labels.shape[0]):
        current_target = data_matrix_labels[i, 0]
        current_image = data_matrix_labels[i, 1]
        current_image_output_file = '{}/{}.txt'.format(output_folder, current_image)
        file = open(current_image_output_file, 'a')
        file.write('{},{},{}\n'.format(str(int(current_target)), data_matrix_values[i, 0], data_matrix_values[i, 1]))
        file.close()

def main():
    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = "Input a file containing a list of GCPs projections in the Metashape format.")
    parser.add_argument("-o", "--Output", help = "Output folder.")
    args = parser.parse_args()

    if args.Input:
        print("Input: % s" % args.Input)
    if args.Output:
        print("Output: % s" % args.Output)
    
    metashape_gcp_folder = args.Input
    output_folder = args.Output

    ConvertGCPmetashape2colmap(metashape_gcp_folder, output_folder)

# Driver function 
if __name__=="__main__": 
    main()