# >cd C:/Users/Luscias/Desktop/3DOM
# >python readCOLMAPp3D.py

pt3D = '731185'


# I/O folders
txt_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo\colmap\txt-outs\points3D.txt'
output_file_path = r'C:\Users\Luscias\Desktop\ventimiglia_completo\colmap\txt-outs\GCP_LFNet_8000f.txt'
print(txt_path)
print(output_file_path)

# Initialize variables
lines= []
d = {}

# Open COLMAP file points3D.txt
with open(txt_path,'r') as file :
    for line in file :
        lines.append(line)

# Store 3D points in a dictionary
for k in range (3,len(lines)) :
    point3D_id, x, y, z, r, g, b, error, image_id, point2d_idx, blob = lines[k].split(' ', 10)
    d[point3D_id] = {
                'point3D_id' : point3D_id,
                'x' : x,
                'y' : y,
                'z' : z,
                'r' : r,
                'g' : g,
                'b' : b,
                'error' : error,
                'image_id' : image_id,
                'point2d_idx' : point2d_idx,
                'blob' : blob
                }

## Write output
out_file = open(output_file_path, 'w')
out_file.write('{},{},{},{}\n'.format(7,d['228864']['x'],d['228864']['y'],d['228864']['z']))
out_file.write('{},{},{},{}\n'.format(8,d['214162']['x'],d['214162']['y'],d['214162']['z']))
out_file.write('{},{},{},{}\n'.format(9,d['165233']['x'],d['165233']['y'],d['165233']['z']))
out_file.write('{},{},{},{}\n'.format(10,d['73822']['x'],d['73822']['y'],d['73822']['z']))
out_file.write('{},{},{},{}\n'.format(14,d['35610']['x'],d['35610']['y'],d['35610']['z']))
out_file.write('{},{},{},{}\n'.format(15,d['34259']['x'],d['34259']['y'],d['34259']['z']))
out_file.write('{},{},{},{}\n'.format(16,d['292705']['x'],d['292705']['y'],d['292705']['z']))
out_file.write('{},{},{},{}\n'.format(17,d['10078']['x'],d['10078']['y'],d['10078']['z']))
out_file.write('{},{},{},{}\n'.format(18,d['228865']['x'],d['228865']['y'],d['228865']['z']))
out_file.write('{},{},{},{}\n'.format(11,d['191274']['x'],d['191274']['y'],d['191274']['z']))
out_file.write('{},{},{},{}\n'.format(12,d['207461']['x'],d['207461']['y'],d['207461']['z']))
out_file.write('{},{},{},{}\n'.format(13,d['179345']['x'],d['179345']['y'],d['179345']['z']))
out_file.write('{},{},{},{}\n'.format(19,d['329744']['x'],d['329744']['y'],d['329744']['z']))
out_file.write('{},{},{},{}\n'.format(20,d['382476']['x'],d['382476']['y'],d['382476']['z']))
out_file.write('{},{},{},{}\n'.format(21,d['362662']['x'],d['362662']['y'],d['362662']['z']))
out_file.write('{},{},{},{}\n'.format(22,d['350219']['x'],d['350219']['y'],d['350219']['z']))
out_file.write('{},{},{},{}\n'.format(23,d['315312']['x'],d['315312']['y'],d['315312']['z']))
out_file.write('{},{},{},{}\n'.format(24,d['391027']['x'],d['391027']['y'],d['391027']['z']))
out_file.write('{},{},{},{}\n'.format(2,d['510399']['x'],d['510399']['y'],d['510399']['z']))
out_file.write('{},{},{},{}\n'.format(3,d['518533']['x'],d['518533']['y'],d['518533']['z']))
out_file.write('{},{},{},{}\n'.format(4,d['741236']['x'],d['741236']['y'],d['741236']['z']))
out_file.write('{},{},{},{}\n'.format(5,d['540301']['x'],d['540301']['y'],d['540301']['z']))
out_file.write('{},{},{},{}\n'.format(6,d['731185']['x'],d['731185']['y'],d['731185']['z']))
out_file.close()
print(d[pt3D])


## Write output CIPRO
#out_file = open(output_file_path, 'w')
#out_file.write('{},{},{},{}\n'.format(5,d['47239']['x'],d['47239']['y'],d['47239']['z']))
#out_file.write('{},{},{},{}\n'.format(7,d['49461']['x'],d['49461']['y'],d['49461']['z']))
#out_file.write('{},{},{},{}\n'.format(11,d['38346']['x'],d['38346']['y'],d['38346']['z']))
#out_file.write('{},{},{},{}\n'.format(21,d['52278']['x'],d['52278']['y'],d['52278']['z']))
#out_file.write('{},{},{},{}\n'.format(24,d['41780']['x'],d['41780']['y'],d['41780']['z']))
#out_file.write('{},{},{},{}\n'.format(26,d['53682']['x'],d['53682']['y'],d['53682']['z']))
#out_file.write('{},{},{},{}\n'.format(31,d['26450']['x'],d['26450']['y'],d['26450']['z']))
#out_file.write('{},{},{},{}\n'.format(33,d['16430']['x'],d['16430']['y'],d['16430']['z']))
#out_file.write('{},{},{},{}\n'.format(35,d['25230']['x'],d['25230']['y'],d['25230']['z']))
#out_file.write('{},{},{},{}\n'.format(37,d['2433']['x'],d['2433']['y'],d['2433']['z']))
#out_file.write('{},{},{},{}\n'.format(41,d['6681']['x'],d['6681']['y'],d['6681']['z']))
#out_file.write('{},{},{},{}\n'.format(43,d['8112']['x'],d['8112']['y'],d['8112']['z']))
#out_file.close()
#print(d[pt3D])


## Write output DATASET MURO
#out_file = open(output_file_path, 'w')
#out_file.write('{},{},{},{}\n'.format(23,d['32778']['x'],d['32778']['y'],d['32778']['z']))
#out_file.write('{},{},{},{}\n'.format(24,d['32777']['x'],d['32777']['y'],d['32777']['z']))
#out_file.write('{},{},{},{}\n'.format(25,d['34680']['x'],d['34680']['y'],d['34680']['z']))
#out_file.write('{},{},{},{}\n'.format(26,d['34679']['x'],d['34679']['y'],d['34679']['z']))
#out_file.write('{},{},{},{}\n'.format(27,d['26465']['x'],d['26465']['y'],d['26465']['z']))
#out_file.write('{},{},{},{}\n'.format(28,d['26464']['x'],d['26464']['y'],d['26464']['z']))
#out_file.write('{},{},{},{}\n'.format(29,d['23770']['x'],d['23770']['y'],d['23770']['z']))
#out_file.write('{},{},{},{}\n'.format(30,d['23769']['x'],d['23769']['y'],d['23769']['z']))
#out_file.write('{},{},{},{}\n'.format(31,d['20062']['x'],d['20062']['y'],d['20062']['z']))
#out_file.write('{},{},{},{}\n'.format(32,d['20061']['x'],d['20061']['y'],d['20061']['z']))
#out_file.write('{},{},{},{}\n'.format(33,d['16871']['x'],d['16871']['y'],d['16871']['z']))
#out_file.write('{},{},{},{}\n'.format(34,d['16870']['x'],d['16870']['y'],d['16870']['z']))
#out_file.write('{},{},{},{}\n'.format(37,d['12824']['x'],d['12824']['y'],d['12824']['z']))
#out_file.write('{},{},{},{}\n'.format(38,d['12823']['x'],d['12823']['y'],d['12823']['z']))
#out_file.write('{},{},{},{}\n'.format(39,d['9306']['x'],d['9306']['y'],d['9306']['z']))
#out_file.write('{},{},{},{}\n'.format(40,d['9305']['x'],d['9305']['y'],d['9305']['z']))
#out_file.write('{},{},{},{}\n'.format(41,d['1991']['x'],d['1991']['y'],d['1991']['z']))
#out_file.write('{},{},{},{}\n'.format(42,d['1461']['x'],d['1461']['y'],d['1461']['z']))
#out_file.write('{},{},{},{}\n'.format(43,d['5076']['x'],d['5076']['y'],d['5076']['z']))
#out_file.write('{},{},{},{}\n'.format(44,d['1745']['x'],d['1745']['y'],d['1745']['z']))
#out_file.write('{},{},{},{}\n'.format(47,d['8923']['x'],d['8923']['y'],d['8923']['z']))
#out_file.write('{},{},{},{}\n'.format(48,d['8997']['x'],d['8997']['y'],d['8997']['z']))
#out_file.close()
#print(d[pt3D])

# Write output NETTUNO
#out_file = open(output_file_path, 'w')
#out_file.write('{},{},{},{}\n'.format(19,d['7325']['x'],d['7325']['y'],d['7325']['z']))
#out_file.write('{},{},{},{}\n'.format(47,d['7326']['x'],d['7326']['y'],d['7326']['z']))
#out_file.write('{},{},{},{}\n'.format(27,d['1860']['x'],d['1860']['y'],d['1860']['z']))
#out_file.write('{},{},{},{}\n'.format(38,d['395']['x'],d['395']['y'],d['395']['z']))
#out_file.write('{},{},{},{}\n'.format(32,d['3556']['x'],d['3556']['y'],d['3556']['z']))
#out_file.write('{},{},{},{}\n'.format(41,d['4463']['x'],d['4463']['y'],d['4463']['z']))
#out_file.close()
#print(d[pt3D])

# Write output VENTIMIGLIA
#out_file = open(output_file_path, 'w')
#out_file.write('{},{},{},{}\n'.format(7,d['9569']['x'],d['9569']['y'],d['9569']['z']))
#out_file.write('{},{},{},{}\n'.format(8,d['5466']['x'],d['5466']['y'],d['5466']['z']))
#out_file.write('{},{},{},{}\n'.format(9,d['505']['x'],d['505']['y'],d['505']['z']))
#out_file.write('{},{},{},{}\n'.format(10,d['3280']['x'],d['3280']['y'],d['3280']['z']))
#out_file.write('{},{},{},{}\n'.format(14,d['7677']['x'],d['7677']['y'],d['7677']['z']))
#out_file.write('{},{},{},{}\n'.format(15,d['4521']['x'],d['4521']['y'],d['4521']['z']))
#out_file.write('{},{},{},{}\n'.format(16,d['16348']['x'],d['16348']['y'],d['16348']['z']))
#out_file.write('{},{},{},{}\n'.format(17,d['5467']['x'],d['5467']['y'],d['5467']['z']))
#out_file.write('{},{},{},{}\n'.format(18,d['9570']['x'],d['9570']['y'],d['9570']['z']))
#out_file.close()
#print(d[pt3D])