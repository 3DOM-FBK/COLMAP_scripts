# Quaternioni
# https://www.meccanismocomplesso.org/i-quaternioni-di-hamilton-e-la-rotazione-in-3d-con-python/

# >cd C:/Users/Luscias/Desktop/3DOM
# >python readCOLMAPimages.py

import numpy as np
from pyquaternion import quaternion
from scipy.spatial.transform import Rotation as R
from scipy import linalg

# I/O folders
txt_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo_no_gcps\colmap\txt-outs\images.txt'
output_file_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo_no_gcps\colmap\txt-outs\image_coordinates.txt'
print(txt_path)
print(output_file_path)

# Initialize variables
lines= []
d = {}
k = 0
n_images = 0

# Open COLMAP file points3D.txt
with open(txt_path,'r') as file :
    for line in file:
        k = k+1
        line = line[:-1]
        first_elem, waste = line.split(' ', 1)
        if first_elem == "#":
            print(first_elem)
        #elif len(lines) == 10:
        #    quit()
        elif k%2 != 0:
            image_id, qw, qx, qy, qz, tx, ty, tz, camera_id, name = line.split(" ", 9)
            #q = R.from_quat([float(qw), float(qx), float(qy), float(qz)])
            #t = np.array([[float(tx)],[float(ty)],[float(tz)]])
            #camera_location = np.dot(-q.as_matrix().transpose(),t) #.transpose()
            
            q = np.array([float(qw), float(qx), float(qy), float(qz)])
            t = np.array([[float(tx)],[float(ty)],[float(tz)]])
            q_matrix = quaternion.Quaternion(q).transformation_matrix
            q_matrix = q_matrix[0:3,0:3]
            camera_location = np.dot(-q_matrix.transpose(),t)
            
            print('q', float(qw), float(qx), float(qy), float(qz), float(qw)**2+float(qx)**2+float(qy)**2+float(qz)**2)
            #print('q.as_matrix()\n', q.as_matrix())
            print('t', t)
            print('camera_location', camera_location)
            lines.append('{} {} {} {}'.format(name, camera_location[0,0], camera_location[1,0], camera_location[2,0]))
            print(line)
            n_images = n_images + 1
            #break

print(lines)
print ("Camera number = ", n_images)

out_file = open(output_file_path, 'w')
for element in lines:
    out_file.write(element)
    out_file.write('\n')
out_file.close()




quit()

print('prova')

q0 = 0.993452 
q1 = 0.0763888 
q2 = 0.0789067 
q3 = 0.0314928

translation = np.array([[3.77525],[-0.593781],[0.190783]])

r = R.from_quat([q1, q2, q2, q3])
print(r.as_matrix())
t = -np.dot(r.as_matrix().transpose(),translation)
print(t)
