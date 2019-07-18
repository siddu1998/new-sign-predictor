from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import style
import pandas as pd 
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib
from matplotlib.figure import Figure
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk 
from PIL import ImageTk, Image
import os


class UI:
	def __init__(self,front_camera_images_path,right_camera_images_path,coords_file_path,width,height,storage_csv):
		self.width=width
		self.height=height
		self.front_camera_images_path=front_camera_images_path
		self.right_camera_images_path=right_camera_images_path

		#both the front and right camera have the same number of images taken along the path so we can call both the images using only one single name, no need of two separate variables 
		#make sure to place them in a single list of sequence
        
		#load and store front camera iamge names in list named : front_camera_input_names
		sub_folders = sorted(os.listdir(front_camera_images_path)
        jpg_cnt = sum(1 for f in sub_folders if f.endswith(".jpg"))
        if jpg_cnt == 0:
            # frames are in the sub-directories
            file_list_front_camera = []
            for sub_folder in sub_folders:
                temp_list = (os.listdir(os.path.join(front_camera_images_path, sub_folder)))
                temp_list = [os.path.join(sub_folder, f) for f in temp_list if f.endswith(".jpg")]
                file_list_front_camera = file_list_front_camera + temp_list
            file_list_front_camera.sort()
            self.front_camera_input_image_names = file_list_front_camera
        else:
            # frames are in the folder
            self.front_camera_input_image_names = sub_folders

		#load and store the right camera image names in list named : right_caemra_input_names
		sub_folders = sorted(os.listdir(right_camera_images_path)
        jpg_cnt = sum(1 for f in sub_folders if f.endswith(".jpg"))
        if jpg_cnt == 0:
            # frames are in the sub-directories
            file_list_right_camera = []
            for sub_folder in sub_folders:
                temp_list = (os.listdir(os.path.join(right_camera_images_path, sub_folder)))
                temp_list = [os.path.join(sub_folder, f) for f in temp_list if f.endswith(".jpg")]
                file_list_right_camera = file_list_right_camera + temp_list
            file_list_right_camera.sort()
            self.right_camera_input_image_names = file_list_right_camera
        else:
            # frames are in the folder
            self.right_camera_input_image_names = sub_folders
		
		self.image_index_front_camera=0
		self.image_index_right_camera=0

		self.coords_file=coords_file_path

		#reading coords and converting to dataframe
		self.coords_df=pd.read_csv(self.coords_file)

