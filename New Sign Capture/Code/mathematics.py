import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import distance
from pyproj import Proj, transform, Geod
from math import atan2, cos, sin



def get_distance_between_two_consecutive_images(cordinate_1,cordinate_2):
    """
    #TODO : Develop a function which allows the user to find the distance between two consecutive images, 
    The UTM cordinate system plots points assuming the world is a flat sheet of paper, hence the distance between
    two points is the euclidean distance between them.
    :param cordinate_1: The first point on the UTM system
    :param cordinate_2: The second point on the UTM system
    :return: distance between the two points in meters
    
    """
    return distance.euclidean(cordinate_1,cordinate_2)



def clear_distortions(img_before_distance):
    """
    #TODO: Every image taken from a camera is subjected to distortions, the distortions subjected can be removed 
    by knowing the intrinstic parameteres of the camera. Develop a function to remove the distortions using opencv.
    :param: Image to clear distortions
    :return: Undistorted image
    """
    
    #TODO please change the matrix values accordingly as per your camera calibration file (provided .yaml)
    #mtx=[[1203.032354,0,720.0],[0,1284.609285,540.0],[0,0,1]]
    #dist=[ 0,0,0,0 ]

    #distortion_matrix_big camera
    mtx=[[2468.6668434782608,0,1228.876620888020],[0,2468.6668434782608,1012.976060035710],[0,0,1]] 
    dist=[ 0.00125859 , 0 ,  -0.00010658,0 ]
    
    #converting into numpy
    mtx = np.array(mtx)
    dist=np.array(dist)
    
    #image dimensions
    image_height,image_width,_=img_before_distance.shape

    #pumping distortion matrix
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(image_width,image_height),1,(image_width,image_height))

    #undistort image_before_distance
    img_before_distance = cv2.undistort(img_before_distance, mtx, dist, None, newcameramtx)
    x,y,w,h = roi
    undistorted_image = img_before_distance[y:y+h, x:x+w]

    #undistort image_after_distance

    return undistorted_image



def find_center_of_sign(sign_details_list):
    """
    TODO: From the list you get from the above function as the input calculate the center of the sign
    :param: data in the format [sign_top_left_x,sign_top_left_y,sign_width,sign_height,class_of_sign].
    :return: the mid-point of the sign 
    """
    sign_top_left_x=sign_details_list[0]
    sign_top_left_y=sign_details_list[1]
    sign_width=sign_details_list[2]
    sign_height=sign_details_list[3]

    location_sign=(int((sign_top_left_x+sign_top_left_x+sign_width)/2),int((sign_top_left_y+sign_top_left_y+sign_height)/2))
    return location_sign




def distance_two_points_along_x(A,B):
    """
    #TODO: return the distance along x-axis [A:(x1,y1),B:(x2,y2)] return x1-x2
    """
    return A[0]-B[0]
def distance_two_points_along_y(A,B):
    """
    #TODO: return the distance along y-axis [A:(x1,y1),B(x2,y2)] return y1-y2
    """
    return A[1]-B[1]





def trignometric_calculations(x1,x2,f,camera_cordinates_1,camera_cordinates_2):
    """
    #TODO: Using the 2 point method return how inclined and how ahead the sign is
    :param x1: cordinate of the sign in image 1 w.r.t to the image center
    :param x2: cordinate of the sign in image 2 w.r.t. to the image center
    "param camera_cordinates _1/2": Cordinates of the camera (UTM)
    Note: If you are taking the images from the GTSV you can use 5m as the distance between two 
    consecutive images, this saves calculation else use the get_distance_between_two_consecutive_images()
    :return: (w,l) --> (how wide, how ahead) the sign is. 
    """
    dst= get_distance_between_two_consecutive_images(camera_cordinates_1,camera_cordinates_2)   
    print('The images are taken at a distance of {} m '.format(dst)) 
    if(x2-x1)!=0:
        l =  dst * x1/(x2-x1) 
        w = l * (x2)/f 
    elif (x2-x1)==0:
        l=dst * x1
        w=l*(x2)/f
    #w--> how right or how left the sign is (x-axis)
    #l--> how ahead the sign is (y-axis)
    print('how inclined:', w) #add to the x-cordinate
    print('how ahead:', l) #add to the y-cordinate
    return (w,l)
    






def camera_to_sign(camera_cordinates_image_1,camera_cordiantes_image_2,distancs_tuple):
    """
    #TODO: develop a function which takes in the UTM of the camera and distances and return the final position 
    of the sign
    :param camera_cordinates: The UTM cordinates of the camrea
    :param distances_tuple: (w,l)
    :return: Return the final global UTM cordinates of the sign
    :reference: https://colab.research.google.com/drive/1FuMxjRer1jlFXTjgRy9gecxYe0RrsWfW
    """
    proj_wgs = Proj(init='EPSG:4326')  # WGS84 coordinate system http://spatialreference.org/ref/epsg/wgs-84/
    proj_ga = Proj(init='EPSG:26916') # UTM zone 16N, which contains Atlanta http://www.spatialreference.org/ref/epsg/26916/
    lat1=camera_cordinates_image_1[2]
    lat2=camera_cordiantes_image_2[2]
    lon1=camera_cordinates_image_1[3]
    lon2=camera_cordiantes_image_2[3]
    # Convert GPS coordinates of the cameras to XY coordinates using the UTM 16N coordinate system
    camera1_x, camera1_y = transform(proj_wgs, proj_ga, lon1, lat1)
    camera2_x, camera2_y = transform(proj_wgs, proj_ga, lon2, lat2)
    print(camera1_x,camera1_y)
    print(camera2_x,camera2_y)

    # Find the direction of movement of the camera, get angle to deal with which direction to add
    angle = atan2(camera2_y - camera1_y, camera2_x - camera1_x)
    print(angle)

    # Calculate world coordinates of the point in the UTM 16N coordinate system
    # First apply rotation and then add the position of the camera
    sign_world_coords = np.empty(2)
    sign_world_coords[0] = distancs_tuple[1] * cos(angle) + distancs_tuple[0] * sin(angle) + camera1_x
    sign_world_coords[1] = distancs_tuple[1] * sin(angle) - distancs_tuple[0] * cos(angle) + camera1_y
    print("UTM sign", sign_world_coords)

    # Convert the world coordinates of the point to GPS coordinates
    sign_lon, sign_lat = proj_ga(sign_world_coords[0], sign_world_coords[1], inverse=True)

    return sign_lat, sign_lon

    #return (camera_cordinates[0]+distancs_tuple[1],camera_cordinates[1]-distancs_tuple[0])




def get_gps(image_file_name_before_distance,image_file_name_after_distance,sign_center_1,sign_center_2,frame_gps):
    print(image_file_name_before_distance,image_file_name_after_distance)
    img_before_distance = cv2.imread(image_file_name_before_distance)
    img_after_distance  = cv2.imread(image_file_name_after_distance)
    #clear distortions
    img_before_distance = clear_distortions(img_before_distance)
    img_after_distance  = clear_distortions(img_after_distance)
    #calculate image center and dimensions
    image_height=2448
    image_width =2048

    #image_height,image_width,_=img_before_distance.shape
    image_center = (int(image_width/2),int(image_height/2))
    #if we are dealing with the same image proceed as else inform and kill 
    #Find center of sign
    #center_before_distance = find_center_of_sign(tr_bbox1,tr_bbox2)
    #center_after_distance  = find_center_of_sign(sign_after_distance)
    #distance between center and sign
    
    x1=sign_center_1[0]-image_center[0]
    x2=sign_center_2[0]-image_center[1]

    distance_tuple=trignometric_calculations(x1,x2,f,camera_cordinates_image_1,camera_cordinates_image_2)
    #understanding spatial location
    #right_or_left = finding_relative_location_of_image(center_after_distance,image_width)
    #adding and subtracting images 
    final_positions = camera_to_sign(camera_cordinates_image_1,camera_cordinates_image_2,distance_tuple)
    #error_analysis(final_positions)
    return final_positions


