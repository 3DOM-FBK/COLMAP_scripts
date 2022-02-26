from PIL import Image
import os

IMG_FOLDER = r"C:\Users\fbk3d\Desktop\aerialResized"
OUTPUT_FOLDER = r"C:\Users\fbk3d\Desktop\aerialJPG"

# Main starts here
print("IMAGE MANIPULATION")

img_list = os.listdir(IMG_FOLDER)
print("Number of images: ", len(img_list))

# Convert TIFF with alpha_channel to jpg
for img in img_list:
    img_file = f"{IMG_FOLDER}/{img}"
    out_file = f"{OUTPUT_FOLDER}/{img[:-4]}.jpg"

    pimg = Image.open(img_file)
    pimg = pimg.convert("RGB")
    pimg.save(out_file, "JPEG", quality=100)