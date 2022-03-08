# Looking for 3D coordinates of the included targets

class projection:
    def __init__(self, x, y, camera, gcp_n, p2D_id, Xe, Ye, Ze, camera_id, triangulated):
        self.x = x
        self.y = y
        self.camera =camera
        self.gcp_n = gcp_n
        self.p2D_id = p2D_id
        self.Xe = Xe
        self.Ye = Ye
        self.Ze = Ze
        self.camera_id = camera_id
        self.triangulated = triangulated

class p3D:
    def __init__(self, point3D_id, x, y, z, r, g, b, error, prjs):
        self.point3D_id = point3D_id
        self.x = x
        self.y = y
        self.z = z
        self.r = r
        self.g = g
        self.b = b
        self.error = error
        self.prjs = prjs

class GCP:
    def __init__(self, id, number_projection, X, Y, Z):
        self.id = id
        self.number_projection = number_projection
        self.X = X
        self.Y = Y
        self.Z = Z

def main(txt_path, output_file_path, path):
    n = 0
    with open(path, 'r') as aaa:
        for aa in aaa:
            img, gcp, idd, x, y, cam_id = aa.split(",")
            n = n + 1
            
    proj_ob = [projection(x = None, y = None, camera = None, gcp_n = None, p2D_id = None, Xe = None, Ye = None, Ze = None, camera_id = None, triangulated = None) for i in range(n)]
    
    n = 0
    with open(path, 'r') as aaa:
        for aa in aaa:
            img, gcp, idd, x, y, cam_id = aa.split(",")
            proj_ob[n].x = x
            proj_ob[n].y = y
            proj_ob[n].camera = img
            proj_ob[n].gcp_n = gcp
            proj_ob[n].p2D_id = idd
            proj_ob[n].camera_id = cam_id
            n = n + 1
    
    lines= []
    
    # Open COLMAP file points3D.txt
    c = 0
    with open(txt_path,'r') as file :
        for line in file :
            lines.append(line)
            c += 1
    
    point_3D_object = [p3D(point3D_id = None, x = None, y = None, z = None, r = None, g = None, b = None, error = None, prjs = []) for i in range(c-3)]
    
    # Store 3D points in a dictionary
    for k in range (3, len(lines)-3) :
        point3D_id, x, y, z, r, g, b, error, projs_and_images = lines[k].split(' ', 8)
        point_3D_object[k-3].point3D_id = point3D_id
        point_3D_object[k-3].x = x
        point_3D_object[k-3].y = y
        point_3D_object[k-3].z = z
        point_3D_object[k-3].r = r
        point_3D_object[k-3].g = g
        point_3D_object[k-3].b = b
        point_3D_object[k-3].error = error
        p_i = projs_and_images.split(" ")
        numb_of_proj = len(p_i)
        for s in range(0, int(numb_of_proj/2)):
            point_3D_object[k-3].prjs.append((int(p_i[s*2]), int(p_i[s*2+1])))
    
    for j in range(0, len(point_3D_object)):
        for c in range(0, len(proj_ob)):
            if proj_ob[c].p2D_id != "None":         
                for e in point_3D_object[j].prjs:
                    if e[1] == int(proj_ob[c].p2D_id) and e[0] == int(proj_ob[c].camera_id):
                        proj_ob[c].Xe = point_3D_object[j].x
                        proj_ob[c].Ye = point_3D_object[j].y
                        proj_ob[c].Ze = point_3D_object[j].z
                        proj_ob[c].triangulated = point_3D_object[j].point3D_id
    
    ## Write output
    with open(output_file_path, 'w') as file:
        for c in range(0, len(proj_ob)):
            file.write('{},{},{},{},{}\n'.format(
                proj_ob[c].gcp_n,
                proj_ob[c].Xe,
                proj_ob[c].Ye,
                proj_ob[c].Ze,
                proj_ob[c].triangulated
                ))


    ## Write number of projection for each target
    
    with open(r"{}_with_projections.txt".format(output_file_path[:-4]), 'w') as file:
        gcp_obj = []
        gcp_obj.append(GCP(id = proj_ob[0].gcp_n, number_projection = 1, X = proj_ob[0].Xe, Y = proj_ob[0].Ye, Z = proj_ob[0].Ze))
        for c in range(1, len(proj_ob)): 
            if proj_ob[c].triangulated != None:
                length = len(gcp_obj)
                for t in range(0, length):
                    control = False
                    if gcp_obj[t].id == proj_ob[c].gcp_n:
                        gcp_obj[t].number_projection = gcp_obj[t].number_projection + 1
                        control = True
                        break
                    else:
                        control = False
                if control == False:
                    gcp_obj.append(GCP(id = proj_ob[c].gcp_n, number_projection = 1, X = proj_ob[c].Xe, Y = proj_ob[c].Ye, Z = proj_ob[c].Ze))

        file.write("TARGET_ID N_PROJECTIONS X Y Z\n")
        for d in gcp_obj:
            file.write("{} {} {} {} {}\n".format(d.id, d.number_projection, d.X, d.Y, d.Z))
    print('Done. Check in the output folder.')
            

    
    
    
            
    
