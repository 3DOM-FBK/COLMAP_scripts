import os
import argparse
import sqlite3
import shutil
import gzip
import numpy as np


# Defining the projection object that will contain all the info about each target to be included in COLMAP matches
class projection:
    def __init__(self, x, y, camera, gcp_n, p2D_id, camera_id):
        self.x = x
        self.y = y
        self.camera =camera
        self.gcp_n = gcp_n
        self.p2D_id = p2D_id
        self.camera_id =camera_id


def pair_id_to_image_ids(pair_id):
    image_id2 = pair_id % 2147483647
    image_id1 = (pair_id - image_id2) / 2147483647
    return image_id1, image_id2


# Main function
def main(
            path_to_GCPs,                   # path to the projections to be included in COLMAP
            database_path,                  # path to the COLMAP database
            new_descriptors_path,           # path to folder that will contain the image coordinates of each keypoint included targets projections
            new_matches_path,               # path to the new matches file containing both the tie points from the COLMAP database and the new targets
            path_to_GCPs_projections_sum,   # path to the file wich store the keypoint ID assigned to each target projection
            min_num_matches,                # min numeber of matches to decide if a pair of images can be included in the new matches file
            reduction_factor,                # the ratio between the image resolution used in COLMAP and the resolution in which targets have been marked
            translation_vector,
            debug
            ):

    # Storing all the target projections in a dictionary
    images_with_GCPs = os.listdir(path_to_GCPs)
    GCPs = {}
    n = 0
    for item in images_with_GCPs:
        GCPs[item] = {}
        with open(os.path.join(path_to_GCPs, item), 'r') as lines:
            for line in lines:
                gcp, x, y, bin = line.split(" ", 3)
                GCPs[item][gcp] = [str(float(x)*reduction_factor+translation_vector), str(float(y)*reduction_factor+translation_vector)]
                n = n + 1
        if debug == True:
            print(
                    "GCPs[item]\n",
                    GCPs[item]
                    )

    # Storing all the target from the dictionary in a list of projection objects
    proj_ob = [projection(x = None, y = None, camera = None, gcp_n = None, p2D_id = None, camera_id = None) for i in range(n)]
    n = 0
    for item in GCPs:
        for gcp in GCPs[item]:         
            proj_ob[n].x = GCPs[item][gcp][0]
            proj_ob[n].y = GCPs[item][gcp][1]
            proj_ob[n].camera = item
            proj_ob[n].gcp_n = gcp
            proj_ob[n].camera_id = None
            n = n + 1

    # Retrieval of the camera ID and the name of the images from the COLMAP database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    
    os.makedirs(new_descriptors_path)
    
    cameras = {}
    cursor.execute("SELECT camera_id, params FROM cameras;")
    for row in cursor:
        camera_id = row[0]
        params = np.fromstring(row[1], dtype=np.double)
        cameras[camera_id] = params

    images = {}
    cursor.execute("SELECT image_id, camera_id, name FROM images;")
    for row in cursor:
        image_id = row[0]
        camera_id = row[1]
        image_name = row[2]
        images[image_id] = (len(images), image_name)
     
        for i in range(0, len(proj_ob)):
            if proj_ob[i].camera == image_name + ".txt":
                proj_ob[i].camera_id = image_id

    # Retreival of keypoint coordinates from COLMAP database and writing them in the 'desc' folder
    count_projection_imgs = {}
    for image_id, (image_idx, image_name) in images.items():
        cursor.execute("SELECT data FROM keypoints WHERE image_id=?;", 
                    (image_id,))
        row = next(cursor)
        if row[0] is None:
            keypoints = np.zeros((0, 6), dtype=np.float32)
            descriptors = np.zeros((0, 128), dtype=np.uint8)
        else:
            keypoints = np.fromstring(row[0], dtype=np.float32).reshape(-1, 6)
            cursor.execute("SELECT data FROM descriptors WHERE image_id=?;",
                        (image_id,))
            row = next(cursor)
            descriptors = np.fromstring(row[0], dtype=np.uint8).reshape(-1, 128)
        
        print("Writing keypoints image_id {} image_idx {} image_name {}".format(image_id, image_idx, image_name))
        
        count_projection_imgs[image_name] = keypoints.shape[0]
        
        for item in images_with_GCPs:
            if item == image_name + ".txt":
                gcp_count = len(GCPs[item])
                break
            else:
                if debug == True:
                    print(
                            "item",
                            item,
                            "image_name",
                            image_name + ".txt"
                            )
                gcp_count = 0
        
        with open(os.path.join(new_descriptors_path, str(image_name) + '.txt'), 'w') as file:
            file.write("{} 128\n".format(keypoints.shape[0] + gcp_count))
            for k in range(0, keypoints.shape[0]):
                file.write("{} {} 0.000000 0.000000\n".format(keypoints[k][0], keypoints[k][1]))
            for item in images_with_GCPs:
                if item == image_name + ".txt":
                    for key in GCPs[item]:
                        file.write("{} {} 0.000000 0.000000\n".format(GCPs[item][key][0], GCPs[item][key][1]))
            
    # Retreival of matches from COLMAP database and writing them in the matches.txt file
    cursor.execute("SELECT pair_id, data FROM two_view_geometries "
                   "WHERE rows>=?;", (min_num_matches,))
        
    for row in cursor:
        pair_id = row[0]
        inlier_matches = np.fromstring(row[1],
                                       dtype=np.uint32).reshape(-1, 2)
        image_id1, image_id2 = pair_id_to_image_ids(pair_id)
        image_idx1 = images[image_id1][0]
        image_idx2 = images[image_id2][0]
        
        print("Writing matches couple image_id1 {} image_id2 {}".format(image_id1, image_id2))
        
        with open(new_matches_path, 'a') as file:

            file.write("{} {}\n".format(images[image_idx1+1][1], images[image_idx2+1][1]))
            for i in range(0, inlier_matches.shape[0]):
                file.write("{} {}\n".format(inlier_matches[i][0], inlier_matches[i][1]))
            
            l_c = 0
            j_c = 0
            
            if images[image_idx1+1][1] + '.txt' in images_with_GCPs and images[image_idx2+1][1] + '.txt' in images_with_GCPs:
                for l in GCPs[images[image_idx1+1][1] + '.txt']:
                    j_c = 0
                    for j in GCPs[images[image_idx2+1][1] + '.txt']:

                        if l == j:
                            file.write("{} {}\n".format(int(count_projection_imgs[images[image_idx1+1][1]]) + l_c, int(count_projection_imgs[images[image_idx2+1][1]]) + j_c))
                                            
                            for n in range(0, len(proj_ob)):
                                if proj_ob[n].camera == images[image_idx1+1][1] + '.txt' and proj_ob[n].gcp_n == l:
                                    proj_ob[n].p2D_id = int(count_projection_imgs[images[image_idx1+1][1]]) + l_c
    
                            for n in range(0, len(proj_ob)):
                                if proj_ob[n].camera == images[image_idx2+1][1] + '.txt' and proj_ob[n].gcp_n == j:
                                    proj_ob[n].p2D_id = int(count_projection_imgs[images[image_idx2+1][1]]) + j_c
                        
                        j_c = j_c + 1
                    l_c = l_c + 1
                                        
            file.write("\n")

    for kk in range(0, len(proj_ob)):
        with open(path_to_GCPs_projections_sum, "a") as gcp_out:
            gcp_out.write(
                str(proj_ob[kk].camera) + "," +
                str(proj_ob[kk].gcp_n) + "," +
                str(proj_ob[kk].p2D_id) + "," +
                str(proj_ob[kk].x) + "," +
                str(proj_ob[kk].y) + "," +
                str(proj_ob[kk].camera_id)
                + "\n")

if __name__ == "__main__":
    main()
