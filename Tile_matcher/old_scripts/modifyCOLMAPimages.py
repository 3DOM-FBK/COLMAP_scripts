# >cd C:/Users/Luscias/Desktop/3DOM
# >python modifyCOLMAPimages.py

import numpy as np

# I/O folders
txt_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo\colmap_for_dense\txt-outs\images.txt'
output_file_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo\colmap_for_dense\txt-outs\prova.txt'
print(txt_path)
print(output_file_path)

image_set = []
## Primo dataset
#for n in range(9001,9006):
#    image_set.append("IMG_{}.jpg".format(n)) 
## Secondo dataset
#for n in range(9065,9072):
#    image_set.append("IMG_{}.jpg".format(n)) 
## Terzo dataset
for n in range(8547,8556):
    image_set.append("LEO_{}_acr.jpg".format(n)) 
## Quarto dataset
for n in range(8593,8602):
    image_set.append("LEO_{}_acr.jpg".format(n)) 

print(image_set)

# Initialize variables
lines= []
k = 0
control = False

# Open COLMAP file points3D.txt
with open(txt_path,'r') as file :
    for line in file:
        k = k+1
        line = line[:-1]
        first_elem, waste = line.split(' ', 1)
        
        if first_elem == "#":
            lines.append(line)

        elif k%2 != 0:
            image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, name = line.split(" ", 9)
            print(name)
            if name in image_set:
                control = True
                lines.append(line)
            else :
                control = False
        else :
            if control == True :
                lines.append(line)
        #break

out_file = open(output_file_path, 'w')
for element in lines:
    out_file.write(element)
    out_file.write('\n')
out_file.close()
