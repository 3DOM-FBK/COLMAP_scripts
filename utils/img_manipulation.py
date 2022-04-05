from PIL import Image
import os

MANIPULATION_PROCESS = 'resize'
IMG_FOLDER = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\square_v0.3.1\images"
OUTPUT_FOLDER = r"C:\Users\User\Desktop\Luca\Projects\BenchmarkMilano\Piazza\imgs_resized"
SAVING_FORMAT = 'JPEG'
# Saving options
SAVING = 'JPEG'
QUALITY = 100
Image.MAX_IMAGE_PIXELS = 1000000000
FORMAT_EXTENTION = '.jpg'
# Resize images
NEW_SIZE = (1500, 1000)
RESAMPLE_MODE = Image.LANCZOS # "Image.BICUBIC" or "Image.LANCZOS"




#############################################################################
# MAIN STRATS HERE

print("IMAGE MANIPULATION")
# Load all images in a list
img_list = os.listdir(IMG_FOLDER)
print("Number of images:\t\t", len(img_list))

# PROCESSES
def ResizeImages(pimg, new_size, resample):
    print(f'new_size\t\t\t{new_size}')
    print(f'RESAMPLE_MODE\t\t\t{resample}')
    resized_img = pimg.resize(new_size, resample=resample)
    return resized_img

# Launch the process
print(f'MANIPULATION_PROCESS:\t\t{MANIPULATION_PROCESS}')
if MANIPULATION_PROCESS == 'resize':
    
    for img in img_list:
        img_file = f"{IMG_FOLDER}/{img}"
        pimg = Image.open(img_file)
        pimg = pimg.convert("RGB")
        output_img = ResizeImages(pimg, new_size=NEW_SIZE, resample=RESAMPLE_MODE)
        out_file = f"{OUTPUT_FOLDER}/{img[:-4]}{FORMAT_EXTENTION}"
        output_img.save(out_file, SAVING_FORMAT, quality=QUALITY)

else:
    print('ERROR!\nEnter a valid MANIPULATION_PROCESS ...')
    quit()








quit()
# Convert TIFF with alpha_channel to jpg
for img in img_list:
    img_file = f"{IMG_FOLDER}/{img}"
    out_file = f"{OUTPUT_FOLDER}/{img[:-4]}.jpg"

    pimg = Image.open(img_file)
    pimg = pimg.convert("RGB")
    pimg.save(out_file, "JPEG", quality=100)