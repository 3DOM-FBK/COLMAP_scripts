import os

INPUT_FILE = r"G:\3DOM\13_Imgs_aeree\aerial_trento\31889_Trento_GCPs_Image_Coordinates.txt"
OUTPUT_FOLDER = r"C:\Users\Luscias\Desktop\3DOM\Github_3DOM\COLMAP_scripts\utils\out"
IMG_CONT1 = 0
IMG_CONT2 = 0

# Main starts here
print("CONVERT TXT GCP TO TRIANGULATION FORMAT")

with open(INPUT_FILE, "r") as all_gcp_file:
    all_gcp_file = all_gcp_file.readlines()[1:]
    for line in all_gcp_file:
        if line == "\n":
            IMG_CONT1 += 1
        else:
            header, rest = line.split(" ", 1)
            print(header)
            if header == "Image":
                current_img = rest.strip()
                current_img = current_img[2:]
                print("current_img", current_img)
                gcp_file = open("{}/{}.jpg.txt".format(OUTPUT_FOLDER, current_img), "w")
                gcp_file.close()
                IMG_CONT2 += 1
            elif header == "GCP_ID":
                gcp_file = open("{}/{}.jpg.txt".format(OUTPUT_FOLDER, current_img), "w")
                rest = rest.strip()
                all_items_split = rest.split(" ")
                print(all_items_split)
                for item in all_items_split:
                    if item != '' and item != ':':
                        gcp_file.write("{} ".format(item))
                gcp_file.write("\n")
                gcp_file.close()
            else:
                gcp_file = open("{}/{}.jpg.txt".format(OUTPUT_FOLDER, current_img), "a")
                rest = rest.strip()
                all_items_split = rest.split(" ")
                print(all_items_split)
                for item in all_items_split:
                    if item != '' and item != ':':
                        gcp_file.write("{} ".format(item))
                gcp_file.write("\n")
                gcp_file.close()

print("Final checks:")
print("IMG_CONT1: ", IMG_CONT1)
print("IMG_CONT2: ", IMG_CONT2)