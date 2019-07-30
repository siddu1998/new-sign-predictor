import os
from mpl_toolkits.mplot3d import axes3d
from collections import defaultdict
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
from tkinter import *
from PIL import ImageTk, Image,ImageDraw
import statistics





#font size
LARGE_FONT=("Verdana",9)



#Creating the Tkinter APP
class SignAnalyzer(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container=tk.Frame(self)

        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.frames={}
        for F in (StartPage,PageOne,PageTwo):
            frame = F(container,self)
            self.frames[F]=frame
            frame.grid(row=0,column=0,sticky="nsew")
        
        self.show_frame(StartPage)

    def show_frame(self,cont):
        frame=self.frames[cont]
        frame.tkraise()



#Front page
class StartPage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label=tk.Label(self,text="New Sign Extractor",font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        label1=tk.Label(self,text="This tool uses the 2 point method to calculate the position of the new signs identified in the interstates")
        label1.pack(pady=10,padx=10)
        
        
        #Button to populate histogram and the whole chart itself
        button2=ttk.Button(self,text="Start Tool!", 
        command=lambda: controller.show_frame(PageTwo))

        button2.pack()

class PageOne(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        button1=ttk.Button(self,text="Back Home", 
        command=lambda: controller.show_frame(StartPage))
        button1.pack()







class PageTwo(tk.Frame):

    def __init__(self,parent,controller):
        
        tk.Frame.__init__(self,parent)

        self.width_of_panel=600
        self.height_of_panel=600
        self.title_text = StringVar()
        self.bug_variable=0
        print("Please select the image directories") 
        self.title = Label(self, textvariable=self.title_text, bg='gray20', fg='white',activebackground='gray20')
        self.title.pack(side='top')
        self.img_path_for_front = self.get_directories()
        self.img_path_for_right  = self.get_directories()
        self.img_index_front_images=0
        self.img_index_right_images=0
        self.front_image_list=[]
        self.right_image_list=[]
        self.image_name_front=None
        self.image_name_right=None
        self.next_image_front=None
        self.front_image_list=self.get_image_list(self.img_path_for_front)
        self.right_image_list=self.get_image_list(self.img_path_for_right)

        self.farme_for_images=tk.Frame(self,relief='solid', bg='gray30')
        self.img_label_1 = tk.Label(self.farme_for_images)
        self.img_label_1.pack(side='left')
        self.img_label_2=tk.Label(self.farme_for_images)
        self.img_label_2.pack(side='left',padx=40)
        self.img_label_3=tk.Label(self.farme_for_images)
        self.img_label_3.pack(side='left')
        self.btn_prev = tk.Button(self.farme_for_images, text='Previous image', command= self.prev_img)
        self.btn_prev.pack(side='bottom')
        self.btn = tk.Button(self.farme_for_images, text='Next image', command= self.next_img)
        self.btn.pack(side='bottom')
        self.btn_for_removal_of_bounding_box=tk.Button(self.farme_for_images,text='Remove current bbox',command=self.remove_current_bounding_box)
        self.btn_for_removal_of_bounding_box.pack(side='bottom')

        self.img_label_1.bind("<Button-1>",self.clicked)
        self.img_label_1.bind("<ButtonRelease-1>",self.release)

        self.img_label_2.bind("<Button-2>",self.clicked_i2)
        self.img_label_2.bind("<ButtonRelease-2>",self.release_i2)
        
        self.farme_for_images.pack(side="top", padx="10", pady="10", fill='both', expand=1)
        
        #variable storing all data for the output
        self.all_data=[]
        self.current_instance=[]#[im1,im2,(),(),(),(),c1,c2]
        #each entry in all data would be like [  [image_name_1,image_name_2,(bbox1_x1,bbox1_y1),(bbox1_x2,bbox1_y2),(bbox2_x1,bbox2_y1),(bbox2_x2,bbox2_y2),centroid_1,centroid_2,predited_gps_x,predicted_gps_y]   ]
        # self.x11=None
        # self.y11=None
        # self.x12=None
        # self.y12=None

        # self.x21=None
        # self.y21=None
        # self.x22=None
        # self.y22=None



        print(self.img_path_for_front)
        print(self.img_path_for_right)
        print(len(self.front_image_list),self.img_path_for_front)
        print(len(self.right_image_list),self.img_path_for_right)


    def prev_img(self):
        self.img_index_front_images=self.img_index_front_images-1
        self.img_index_right_images=self.img_index_right_images-1    
        self.image_name_front=self.front_image_list[self.img_index_front_images]
        self.next_image_front=self.front_image_list[self.img_index_front_images+1]
        self.image_name_right=self.right_image_list[self.img_index_right_images]
        self.title_text.set("n-front{} n+1 front {} n-right {}".format(self.image_name_front,self.next_image_front,self.image_name_right))
        image=Image.open(self.image_name_front)
        image_resized=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        image_2=Image.open(self.next_image_front)
        image_resized_2=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        image_3=Image.open(self.image_name_right)
        image_resized_3=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.img_label_1.img = ImageTk.PhotoImage(image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        self.img_label_2.img = ImageTk.PhotoImage(image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)
        self.img_label_3.img = ImageTk.PhotoImage(image_resized_3)
        self.img_label_3.config(image=self.img_label_3.img)


        print("----------------PREV----------")
        print("[INFO] Images {} {} {} being shown".format(self.image_name_front,self.next_image_front,self.image_name_right))
        print("[INFO] Image index front camera from list : " , self.img_index_front_images)
        print("[INFO] Image index right camera from list : " , self.img_index_right_images)
        print("-------------------------------")
#TODO get previous frame 
#TODO How to store values into inventory
#TODO Autoplay
#TODO values
#Storage and autoplay

    def next_img(self):
        print("-----------NEXT---------------")
        print("[INFO] Image index front camera from list : ", self.img_index_front_images)
        print("[INFO] Image Index right camera from list :",self.img_index_front_images)
        self.image_name_front=self.front_image_list[self.img_index_front_images]
        self.next_image_front=self.front_image_list[self.img_index_front_images+1]
        self.image_name_right=self.right_image_list[self.img_index_right_images]
        self.title_text.set("n-front{} n+1 front {} n-right {}".format(self.image_name_front,self.next_image_front,self.image_name_right))
        image=Image.open(self.image_name_front)
        image_resized=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        image_2=Image.open(self.next_image_front)
        image_resized_2=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        image_3=Image.open(self.image_name_right)
        image_resized_3=image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.img_label_1.img = ImageTk.PhotoImage(image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        self.img_label_2.img = ImageTk.PhotoImage(image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)
        self.img_label_3.img = ImageTk.PhotoImage(image_resized_3)
        self.img_label_3.config(image=self.img_label_3.img)
        print("[INFO] Images {} {} {} being shown".format(self.image_name_front,self.next_image_front,self.image_name_right))
        print("-------------------------------")
        self.img_index_front_images= self.img_index_front_images+1
        self.img_index_right_images= self.img_index_right_images+1

    #first click on image 1
    def clicked(self,event):
        initial_click=(event.x,event.y)
        print("-------------CREATING NEW BOUNDING BOX INSTANCE---------------")
        print("[INFO] Top-Left Corner of slected image in resized image {} {}".format(initial_click[0],initial_click[1]))
        #appending image_name_from_panel_1
        print("[INFO] Appending image index {} {}".format(self.img_index_front_images,self.img_index_front_images+1))
        self.current_instance.append(self.img_index_front_images)
        self.current_instance.append(self.img_index_right_images+1)
        print("[INFO] Appending top left corner of the image to the current instance")
        self.current_instance.append(initial_click)
        
    #release event on image 2
    def release(self,event):
        release_point=(event.x,event.y)
        print("[INFO] Releasing mouse at {} {}".format(release_point[0],release_point[1]))
        print("[INFO] Appending release point into current instance")
        self.current_instance.append(release_point)

        print("[INFO] Bounding Boxes drawn on box-1 Now proceed to draw bouding boxes on box two")
        
    #double_click event for second image
    def clicked_i2(self,event):
        initial_click_i2=(event.x,event.y)
        print("[INFO] Top-Left Corner of slected image 2 in resized image {} {}".format(initial_click_i2[0],initial_click_i2[1]))
        #appending image_name_from_panel_1
        print("[INFO] Appending top left corner of the image 2 to the current instance")
        self.current_instance.append(initial_click_i2)
    
    #double_click_release
    def release_i2(self,event):
        release_point_i2=(event.x,event.y)
        print("[INFO] Releasing mouse at 2 {} {}".format(release_point_i2[0],release_point_i2[1]))
        print("[INFO] Appending release point into current instance")
        self.current_instance.append(release_point_i2)
        print("[INFO] Bounding Boxes drawn on box-2")
        print("[INFO] Appending the current instance {} into global inventory".format(self.current_instance))
        self.all_data.append(self.current_instance)
        self.current_instance=[]
        print("[INFO] Printing inventory till now {}".format(self.all_data))
        print("[INFO] All Data captured! Move to next image")
        print("---------------------------------------------------------------")

        

    def remove_current_bounding_box(self):
        pass
    
    def get_directories(self):
        return filedialog.askdirectory()
    
    def get_image_list(self,img_path):
        image_list=[]
        sub_folders = sorted(os.listdir(img_path))
        jpg_cnt = sum(1 for f in sub_folders if f.endswith(".jpg"))
        if jpg_cnt == 0:
            # frames are in the sub-directories
            file_list = []
            for sub_folder in sub_folders:
                temp_list = (os.listdir(os.path.join(input_image_dir, sub_folder)))
                temp_list = [os.path.join(sub_folder, f) for f in temp_list if f.endswith(".jpg")]
                file_list = file_list + temp_list
                
            file_list.sort()
            front_image_list = file_list
        else:
            # frames are in the folder
            image_list = sub_folders

        return image_list


                
app=SignAnalyzer()
app.mainloop()

