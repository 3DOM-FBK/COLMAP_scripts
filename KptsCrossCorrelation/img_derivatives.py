import os
import numpy as np
from PIL import Image
from pathlib import Path
from scipy import signal

img_dir = Path(r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\KptsCrossCorrelation\test\imgs")


def conv_laplacian(image):
    kernel = np.array([
                        [-1,  0,  1],
                        [-1,  0,  1],
                        [-1,  0,  1]
                        ])
    convolved1 = signal.convolve2d(image, kernel, mode='same', boundary='symm', fillvalue=0)

    kernel = np.array([
                    [-1,  -1,  -1],
                    [0,    0,   0],
                    [1,    1,   1]
                    ])
    convolved2 = signal.convolve2d(image, kernel, mode='same', boundary='symm', fillvalue=0)
    convolved = np.sqrt(convolved1**2+convolved2**2)
    #convolved = ndimage.gaussian_filter(convolved, sigma=2, order=0)
    return convolved


### MAIN ###
img_list = os.listdir(img_dir)
img_list.sort()

for img_name in img_list:
    img = Image.open(img_dir / "{}".format(img_name))
    img = img.convert('L')
    img.show()
    img_np = np.array(img)
    convolved = conv_laplacian(img_np)
    min_value = np.min(convolved)
    convolved = convolved - min_value
    max_value = np.max(convolved)
    convolved = convolved * (255 / max_value)
    convolved = convolved.astype(np.uint8)
    print(np.max(convolved), np.min(convolved))
    
    convolved_pil = Image.fromarray(convolved)
    convolved_pil.show()

    convolved_pil.save(r"{}".format(img_name))
    