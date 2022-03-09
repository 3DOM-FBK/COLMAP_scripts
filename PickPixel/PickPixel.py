# 3DOM PICK PIXEL
#
# Example :
# >cd C:\Users\Luscias\Desktop\3domPickPixel
# >conda activate opencv
# Attenzione inserire il percorso utilizzando "/" e non "\"
# >python PickPixel.py -i _DCS7832.JPG
#
# code inspired by  https://www.geeksforgeeks.org/displaying-the-coordinates-of-the-points-clicked-on-the-image-using-python-opencv/ 

# Libraries
import cv2 
import sys
import argparse
import numpy as np
import os.path

print("NOTE: The targets will be marked on an image with a size which is the double of the original size.")


def pickPix(img_path, output_path):

    cv2.namedWindow('image',cv2.WINDOW_NORMAL)

    # reading the image 
    img = cv2.imread(img_path, 1)    
  
    # displaying the image 
    cv2.imshow('image', img) 
    
    # picked pixels
    pickedPix = {}
    
    def LeftClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: 
            print(x, ' ', y) 
            inp_user = input("Insert GCP ID:  ")
            pickedPix[inp_user]=np.array([x,y])
            cv2.circle(img,(x,y),0,(0,0,255),2)
            cv2.imshow('image', img)
  
    # setting mouse hadler for the image 
    # and calling the click_event() function 
    cv2.setMouseCallback('image', LeftClick) 
    
    # wait for a key to be pressed to exit 
    cv2.waitKey(0) 
  
    # close the window 
    cv2.destroyAllWindows()
    
    print('Picked GCP:  ')
    print(pickedPix)
    print('Saving file ...')
    #np.save(output_path,pickedPix)
    txt_file = open('{}.txt'.format(output_path),"w")
    keys = pickedPix.keys()
    cont = 0
    for k in keys :
        cont = cont + 1
        txt_file.write('{}'.format(k))
        txt_file.write(' {} {} {} '.format(pickedPix[k][0],pickedPix[k][1], cont))
        txt_file.write('\n')
    txt_file.close()
    print('Done')
    
    
    return pickedPix



def EllipseCenter(img_path, output_path):

    #pickedPix = {}

    # collect ellipse edge points
    def LeftClick(event,x,y,flags,param):
        if event == cv2.EVENT_LBUTTONDOWN: 
            print(x, ' ', y) 
            ellipse_pts.append(np.array([x,y]))
            print(ellipse_pts)
            cv2.circle(img,(x,y),0,(0,0,255),2)
            cv2.imshow('image', img)

    
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    img = cv2.imread(img_path, 1) 
    print("img shape" + str(img.shape))
    #img = img # if you do not want to double the image size
    img = cv2.pyrUp(img) ############################# da parametrizzare
    print("img shape" + str(img.shape))
    cv2.imshow('image', img)
    ellipse_pts = []
    cv2.setMouseCallback('image', LeftClick)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # convert list to numpy array
    matrix_points = np.array([[ellipse_pts[0][0],ellipse_pts[0][1]],])
    for i in range (1, len(ellipse_pts)):
        matrix_points = np.concatenate((matrix_points, np.array([[ellipse_pts[i][0], ellipse_pts[i][1]],])),axis=0)

    # Find center of the ellipse
    ellipse = cv2.fitEllipse(matrix_points)
    centerE = ellipse[0]
    print('center')
    print(centerE)
    print('center type')
    print(type(centerE))
    img = cv2.ellipse(img, ellipse, (255,0,0), 1)
    img = cv2.circle(img,(round(centerE[0]), round(centerE[1])),0,(0,0,255),2)
    cv2.namedWindow('image',cv2.WINDOW_NORMAL)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return centerE


def PickEllipse(img_path, output_path):
    pickedPix = {}
    control = 'continue'
    while control == 'continue':
        centerE = EllipseCenter(img_path, output_path)
        inp_user = input("Insert GCP ID:  ")
        #pickedPix[inp_user]=np.array([round(centerE[0]), round(centerE[1])]) # int coordinates
        pickedPix[inp_user]=np.array([(centerE[0]/2), (centerE[1]/2)]) # float coordinates da parametrizzare
        userIO = input('Do you want to pick unother point? y/n')
        if userIO == 'y': control = 'continue'
        elif userIO == 'n': control = 'stop'
        else: quit()

    print('Picked GCP:  ')
    print(pickedPix)
    print('Saving file ...')
    #np.save(output_path,pickedPix)
    txt_file = open('{}.txt'.format(output_path),"w")
    keys = pickedPix.keys()
    cont = 0
    for k in keys :
        cont = cont + 1
        txt_file.write('{}'.format(k))
        #txt_file.write(' {} {} {} '.format(pickedPix[k][0],pickedPix[k][1], cont))
        #txt_file.write(',{},{},{}'.format(img_path, pickedPix[k][0], pickedPix[k][1]))
        txt_file.write(',{},{}'.format(pickedPix[k][0], pickedPix[k][1]))
        txt_file.write('\n')
    txt_file.close()
    print('Done')

    return pickedPix



# Main function
def main():

    print("-- 3DOM PickPixel --\n")

    # I/O management
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--Input", help = "Input image path")
    #parser.add_argument("-o", "--Output", help = "Output Folder")
    args = parser.parse_args()

    #if args.Output:
    #    print("Diplaying Output as: % s" % args.Output)
    if args.Input:
        print("Diplaying Input as: % s" % args.Input)
    
    img_path = args.Input
    #output_path = args.Output
    output_path = img_path
    
    # Verify if image path exists
    if os.path.isfile(img_path):
        print("Image path is correct.")
    else:
        print("File doesn't exist or it is not written correctly.")
    
    userIO = input('Would you like to continue?  y/n\n')
    if userIO == 'n' : quit()
    userIO = input('''
Would you like to pick single points? Type 'single'.
Would you like to pick ellipse center? Type 'ellipse'.\n''')

    if userIO == 'single' or userIO == 's':
        pickPix(img_path, output_path)

    elif userIO == 'ellipse' or userIO == 'e' :
        PickEllipse(img_path, output_path)

    else : quit()

    
    #pickPix(img_path,output_path)
  

# driver function 
if __name__=="__main__": 
    main()
