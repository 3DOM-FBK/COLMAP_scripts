import os

input_folder = r"G:\3DOM\13_Imgs_aeree\aerial_trento\Trento_resized_JPG"


# Main starts here
file_list = os.listdir(input_folder)
print(file_list)

for file in file_list:
    os.rename("{}/{}".format(input_folder, file), "{}/{}".format(input_folder, file[:-4]))