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
from PIL import ImageTk, Image
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
        
        self.farme_for_images.pack(side="top", padx="10", pady="10", fill='both', expand=1)
        
        
        self.all_data=[]

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
        image_resized=image.resize((200,200),Image.ANTIALIAS)
        image_2=Image.open(self.next_image_front)
        image_resized_2=image.resize((200,200),Image.ANTIALIAS)
        image_3=Image.open(self.image_name_right)
        image_resized_3=image.resize((200,200),Image.ANTIALIAS)
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
        image_resized=image.resize((200,200),Image.ANTIALIAS)
        image_2=Image.open(self.next_image_front)
        image_resized_2=image.resize((200,200),Image.ANTIALIAS)
        image_3=Image.open(self.image_name_right)
        image_resized_3=image.resize((200,200),Image.ANTIALIAS)
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
    #release event on image 2
    def release(self,event):
    #double_click event for second image
    def double_clicked(self,event):
    #double_click_release
    def release_after_double_click(self,event):
        


        

    def remove_current_bounding_box(self):
        self.all_data=self.all_data[:-1]
        print("[INFO] removing last element {}".format(len(self.all_data)))
    
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

