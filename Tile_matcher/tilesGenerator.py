import argparse
import os
import glob
import ntpath
import cv2
import shutil
import numpy as np
from PIL import Image


X_OVERLAP = 0
Y_OVERLAP = 0
TILE_WIDTH = 2500
TILE_HEIGHT = 2500

################################################################################
parser = argparse.ArgumentParser(description='tiles generation')
parser.add_argument('-p','--path', help='the path of the images to process', required=True)
parser.add_argument('-ox','--overlapX', type=int, help='the tiles overlap on the X direction', required=False)
parser.add_argument('-oy','--overlapY', type=int, help='the tiles overlap on the Y direction', required=False)
parser.add_argument('-tw','--tileWidth', type=int, help='the tiles width', required=False)
parser.add_argument('-th','--tileHeight', type=int, help='the tiles height', required=False)

#parser.add_argument('-rs', '--resize', help='resize to 640x480 rgb+depth images', action="store_true")
#parser.add_argument('-i', '--invert', help='invert png', action="store_true")
#parser.add_argument('-d', '--discard', help='discard bad image couples', action="store_true")
parser.add_argument('-rm', '--remove', help='remove original files at the end', action="store_true")
args = parser.parse_args()

IMGS_PATH = os.path.abspath(args.path)
if not IMGS_PATH[-1] == '/': IMGS_PATH = IMGS_PATH + '/'

if args.overlapX: X_OVERLAP = args.overlapX
if args.overlapY: Y_OVERLAP = args.overlapY
if args.tileWidth: TILE_WIDTH = args.tileWidth
if args.tileHeight: TILE_HEIGHT = args.tileHeight
if args.remove: REMOVE_ORIGINALS = True

################################################################################
def recreateDir(directory):
################################################################################
  if os.path.exists(directory):
      try:
        shutil.rmtree(directory)
      except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

  os.makedirs(directory)
  return directory


################################################################################
def createDir(directory):
################################################################################
  if not os.path.exists(directory):
      os.makedirs(directory)


################################################################################
def cropImg(imgArr, fName, postfix, left, top, right, down, folder):
################################################################################
    # think about a cartesian system with origin in topleft image corner
    # going positively down on the y axsis
    # going positively right on the x axsis
    #print("      cropping " + postfix + " image")
    crop_imgArr = imgArr[top:top+down, left:left+right]

    outFile = IMGS_PATH + folder + os.sep + fName + postfix + '.jpg'
    print("      ..saving file", outFile)

    if not crop_imgArr.size == 0:
        cv2.imwrite(outFile, crop_imgArr)


################################################################################
def getParam(str, prefix):
################################################################################
    value = str.split(prefix)[1]
    value = value.split('_')[0]

    return value




################################################################################
# MAIN STARTS HERE
print('\nParameters')
print('  overlap on X: '  +str(X_OVERLAP))
print('  overlap on Y: '  +str(Y_OVERLAP))
print('  tile size: ({}, {})'.format(TILE_WIDTH, TILE_HEIGHT))

#list available files
file_list = glob.glob(IMGS_PATH + "/*.jpg")

filesNames = []
for f in file_list:
    tmp_name = ntpath.basename(f)
    out_name = tmp_name.split('.')[0]
    filesNames.append(out_name)
print("\nfilesNames: " + str(filesNames))

outputPath = recreateDir(IMGS_PATH + "tiles")
print("\noutput folder: " + str(outputPath))

print('\nStart processing all files:')
for img_count, fName in enumerate(filesNames):
    print("  (" + str(img_count) + ") " + fName)

    imgArr = cv2.imread(IMGS_PATH + fName + ".jpg", cv2.IMREAD_UNCHANGED);

    dim = imgArr.shape
    img_w = dim[1]; img_h = dim[0]

    #rows = int(img_h / TILE_HEIGHT) #+ 1
    #cols = int(img_w / TILE_WIDTH) #+ 1
    print("    image size {}x{}".format(img_w, img_h))
    #print("    we have {} rows and {} cols".format(rows, cols))

    # modify the tilesize not to have smaller tiles
    rows = int(img_h / (TILE_HEIGHT-X_OVERLAP))
    cols = int(img_w / (TILE_WIDTH-Y_OVERLAP))
    print("    we have {} rows and {} cols".format(rows, cols))

    imgRestX = img_w - (TILE_WIDTH-X_OVERLAP)*cols - X_OVERLAP
    print("    imgRestX {}".format(imgRestX))
    incrementX = int(imgRestX / cols)
    print("    incrementX {}".format(incrementX))
    TILE_WIDTH += incrementX

    imgRestY = img_h - (TILE_HEIGHT-Y_OVERLAP)*rows - Y_OVERLAP
    print("    imgRestY {}".format(imgRestY))
    incrementY = int(imgRestY / rows)
    print("    incrementY {}".format(incrementY))
    TILE_HEIGHT += incrementY

    print("    tile size is {}x{}".format(TILE_WIDTH, TILE_HEIGHT))

    rows = int(img_h / (TILE_HEIGHT-X_OVERLAP))
    cols = int(img_w / (TILE_WIDTH-Y_OVERLAP))
    print("    we have {} rows and {} cols".format(rows, cols))

    #exit()

    top = 0; left = 0
    for r in range(rows): #for r in range(1000000):
        if (top >= img_h): continue

        for c in range(cols): #for c in range(1000000):

            # topLeft corner coordinates
            left = c*TILE_WIDTH - c*X_OVERLAP
            top = r*TILE_HEIGHT - r*Y_OVERLAP

            #if (left >= img_w-X_OVERLAP): continue
            #if (top >= img_h-Y_OVERLAP): continue

            right = TILE_WIDTH; down = TILE_HEIGHT # shift on the x and y

            postfix = '_r' + str(r) + '_c' + str(c)
            postfix = postfix + '_ox' + str(X_OVERLAP) + '_oy' + str(Y_OVERLAP)
            postfix = postfix + '_tw' + str(TILE_WIDTH) + '_th' + str(TILE_HEIGHT)
            print('    crop: ' + fName + postfix)
            print('      top left ({}, {})'.format(left, top))
            print('      right {}'.format(right))
            print('      down {}'.format(down))
            cropImg(imgArr, fName, postfix, left, top, right, down, "tiles")

        #break

    print("\n    image covereing size is {}x{}".format(
        left+TILE_WIDTH, top+TILE_HEIGHT))

exit()

# read all tiles and give the global coordinate of the tile center
print('\n\nRead all tiles and give the global coordinate of the tile center')
file_list = glob.glob(IMGS_PATH + "/tiles/*.jpg")

filesNames = []
for f in file_list:
    tmp_name = ntpath.basename(f)
    out_name = tmp_name.split('.')[0]
    filesNames.append(out_name)
print("\nfilesNames: " + str(filesNames))

print('\nGlobal coordinates of tiles center:')
for img_count, fName in enumerate(filesNames):
    print("  (" + str(img_count) + ") " + fName)

    r = int(getParam(fName, '_r'))
    c = int(getParam(fName, '_c'))
    ox = int(getParam(fName, '_ox'))
    oy = int(getParam(fName, '_oy'))
    tw = int(getParam(fName, '_tw'))
    th = int(getParam(fName, '_th'))

    # topLeft corner coordinates
    left = c*tw - c*ox
    top = r*th - r*oy

    # let's take for example the center of the tile
    tileArr = cv2.imread(IMGS_PATH  + 'tiles' + os.sep + fName + ".jpg", cv2.IMREAD_UNCHANGED);
    dim = tileArr.shape
    tile_w = dim[1]; tile_h = dim[0]
    tile_center = [tile_w/2, tile_h/2]
    global_coords = [tile_center[0] + left, tile_center[1] + top]
    print('    tile center: {} -> {}'.format(tile_center, global_coords))
