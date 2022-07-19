import numpy as np
from PIL import Image
from scipy import signal, ndimage

im_path = r"/home/luca/Scrivania/3DOM/bottiglia/imgs_original/DSC_0186.JPG"


def conv_laplacian(image):
    kernel = np.array([
                        [-1,  0,  1],
                        [-1,  0,  1],
                        [-1,  0,  1]
                        ])
    convolved1 = signal.convolve2d(image, kernel, mode='full', boundary='symm', fillvalue=0)

    kernel = np.array([
                    [-1,  -1,  -1],
                    [0,    0,   0],
                    [1,    1,   1]
                    ])
    convolved2 = signal.convolve2d(image, kernel, mode='full', boundary='symm', fillvalue=0)
    convolved = np.sqrt(convolved1**2+convolved2**2)
    convolved = ndimage.gaussian_filter(convolved, sigma=15, order=0)
    return convolved


img = Image.open(im_path).convert('L')
img_np = np.array(img)
convolved = Image.fromarray(conv_laplacian(img_np))
convolved.show()

convolved = np.array(convolved)
print(np.max(convolved))
