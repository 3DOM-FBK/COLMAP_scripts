import os
import shutil

file_list = open(r"E:\Luca\imgs_selected.txt", 'r')
img_folder = r"E:\Luca\Nadir Primary"
output_folder = r"E:\Luca\imgs_selection"
img_list = os.listdir(img_folder)
print(img_list)

for file in file_list:
    file, trash = file.split(",", 1)
    print(file)
    shutil.copyfile(r'{}/{}'.format(img_folder, file), r'{}/{}'.format(output_folder, file))
    



file_list.close()