#!/usr/bin/env python
# coding: utf-8

# ## Solution Template for 2 point Distance Calculations
# #### Dr. Yi-Chang (James) Tsai 
# 
# The below code template would stand valid for calculating distances of signs taken from two consecutive images. The input parameters for the whole code template would be, the camera parameters, the image cordinates of the sign in the image, the UTM and GPS cordinates of the camera. 
# 
# You are required to calculate the global position of the sign, from the above parameters. Please feel free to add your own suggestions and changes for better performance and more accurate predictions.

# In[95]:


import math
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.spatial import distance
from pyproj import Proj, transform, Geod
from math import atan2, cos, sin


# In[96]:


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


# In[97]:


def draw_boxes_and_points(image,sign_cordinates):
    """
    #TODO (optional) : develop a function which takes the sign_cordinates and the image frame and draws the 
    bounding boxes around the sign. This function is visulaization purposes, feel free to skip the funciton if 
    time is a constraint. We suggest you to finish this function to make sure, you have an idea of the loaction
    you are calculating the distance.
    :param image: the image frame in which you would like to draw the bounding boxes
    :param sign_cordinates: A list containing the sign details extracted from the json (converted to csv) file.
    :return: the frame with the points (four corners marked) and a list of the points itself
    """
    #tl
    cv2.circle(image,(sign_cordinates[0],sign_cordinates[1]),3,(255,255,255),-1)
    #tr
    cv2.circle(image,(sign_cordinates[0]+sign_cordinates[2],sign_cordinates[1]),3,(0,0,0),-1)
    #br
    cv2.circle(image,(sign_cordinates[0]+sign_cordinates[2],sign_cordinates[1]+sign_cordinates[3]),3,(0,0,255),-1)
    #bl
    cv2.circle(image,(sign_cordinates[0],sign_cordinates[1]+sign_cordinates[3]),3,(255,0,0),-1)
    cv2.imwrite("frame_with_bounding_boxes_plotted.jpg",image)
    points=[(sign_cordinates[0],sign_cordinates[1]),
            (sign_cordinates[0]+sign_cordinates[2],sign_cordinates[1]),
            (sign_cordinates[0]+sign_cordinates[2],sign_cordinates[1]+sign_cordinates[3]),
            (sign_cordinates[0],sign_cordinates[1]+sign_cordinates[3])]
    return image,points


# In[98]:


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


# In[99]:


def parsing_annotations(highway_sign_annotations,image_file_name):
    """
    TODO: From the sign annotactions please extract and return the values per image, this includes top_x, top_y, 
    width and height of the image along with the class of the sign present in the image. TIP: you can use pandas to 
    read the csv file. Develop a function to get the concerned data from the csv file. 
    :param highway_sign_annotaions: Get the annotaion file of the sign (.csv)
    :param image_file_name: name of the image whose data we need to get from the csv file
    :return: A list containing the data concerned with the input image taken from the input annotaions
    """
    highway_signs = pd.read_csv(highway_sign_annotations)
    for index,row in highway_signs.iterrows():
        if row['frame_name']== image_file_name:
            sign_top_left_x=row['top_x']
            sign_top_left_y=row['top_y']
            sign_width=row['width']
            sign_height=row['height']
            class_of_sign=['class']

    return [sign_top_left_x,sign_top_left_y,sign_width,sign_height,class_of_sign]


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


# In[100]:


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


# In[101]:



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
    


# In[106]:



def parsing_camrea_annotations(image,camera_annotations):
    """
    #TODO: Develop a function which reads the camera annocatios (.csv) and returns the data corresponding to the
    image. 
    :param image: The name of the image you are searching data for
    :param camera_annotations: the name of the file where the data of the corresponding image is present
    :return: A list of the format [camera_cordinates_x,camera_cordinates_y,camera_cordinates_lat,camera_cordinates_lon]
    
    """
    camera_annotations=pd.read_csv(camera_annotations)
    
    for index,row in camera_annotations.iterrows():
        if row["image_name"]==image:
            camera_cordinates_x=row['x']
            camera_cordinates_y=row['y']
            camera_cordinates_lat=row['lat']
            camera_cordinates_lon=row['lon']
            print(camera_cordinates_x,camera_cordinates_y,camera_cordinates_lat,camera_cordinates_lon)
    return [camera_cordinates_x,camera_cordinates_y,camera_cordinates_lat,camera_cordinates_lon]


# In[120]:


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


# In[121]:


def calculation_of_distances(image_file_name_before_distance,image_file_name_after_distance,sign_annotations,camera_annotations,f=1203.032354):
    """
    TODO: Develop a function to return the final cordinates UTM of the image based on the above functions developed
    :param image_file_name_before_distance: Name of the image file taken before distance d
    :param image_file_name_after_distance: Name of the image file taken after covering distance d
    :param sign_annotations: name of the sign annotaions file
    :param camera_annotation: name of the camera annotaions file
    :param f: focal length in pixels default value set to smartphone lenght
    :return the final positions
    """
    print(image_file_name_before_distance,image_file_name_after_distance)
    img_before_distance = cv2.imread(image_file_name_before_distance)
    img_after_distance  = cv2.imread(image_file_name_after_distance)
    #clear distortions
    #img_before_distance = clear_distortions(img_before_distance)
    #img_after_distance  = clear_distortions(img_after_distance)
    #calculate image center and dimensions
    image_height,image_width,_=img_before_distance.shape
    image_center = (int(image_width/2),int(image_height/2))
    #parse annotations for details
    sign_before_distance = parsing_annotations(sign_annotations,image_file_name_before_distance)
    sign_after_distance  = parsing_annotations(sign_annotations,image_file_name_after_distance)
    #if we are dealing with the same image proceed as else inform and kill 
    if sign_after_distance[4]==sign_before_distance[4]:
        #Find center of sign
        center_before_distance = find_center_of_sign(sign_before_distance)
        center_after_distance  = find_center_of_sign(sign_after_distance)
        #distance between center and sign
        x1=distance_two_points_along_x(center_before_distance,image_center)
        x2=distance_two_points_along_x(center_after_distance,image_center)
        #getting camera_cordinates_to_calculate distance between images
        camera_cordinates_image_2=parsing_camrea_annotations(image_file_name_after_distance,camera_annotations)
        camera_cordinates_image_1=parsing_camrea_annotations(image_file_name_before_distance,camera_annotations)
        #getting distances from camera
        distance_tuple=trignometric_calculations(x1,x2,f,camera_cordinates_image_1,camera_cordinates_image_2)
        #understanding spatial location
        #right_or_left = finding_relative_location_of_image(center_after_distance,image_width)
        #adding and subtracting images 
        final_positions = camera_to_sign(camera_cordinates_image_1,camera_cordinates_image_2,distance_tuple)
        #error_analysis(final_positions)
        return final_positions
    else:
        print('Sorry, We could not find the same sign on both the images')
        return (0,0)


# In[122]:


#Test Case
calculation_of_distances('0002876.jpg','0002877.jpg','i75_sign_annotations.csv','i75_camera_cordinates.csv',f=2400)


# In[ ]:





# In[ ]:




