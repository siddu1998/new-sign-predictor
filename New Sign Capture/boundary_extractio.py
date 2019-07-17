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
	def __init__(self,front_camera_images_path,right_camera_images_path,coords_file,camera_properties_file,width,height):
		self.width=width
		self.height=height
		self.front_camera_images=front_camera_images
		self.right_camera_images=right_camera_images

		#both the front and right camera have the same number of images taken along the path so we can call both the images using only one single name, no need of two separate variables 
		#make sure to place them