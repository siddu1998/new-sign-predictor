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
from constants import *
import time


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
        self.frame_rate=1
        print("Please select the image directories") 
        self.title = Label(self, textvariable=self.title_text, bg='gray20', fg='white',activebackground='gray20')
        self.title.pack(side='top')
        self.img_path_for_front = self.get_directories()
        print(self.img_path_for_front)
        self.img_path_for_right  = self.get_directories()
        print(self.img_path_for_right)
        self.img_index_front_images=0
        self.img_index_right_images=0
        self.front_image_list=[]
        self.right_image_list=[]
        self.image_name_front=None
        self.image_name_right=None
        self.next_image_front=None
        self.front_image_list=self.get_image_list(self.img_path_for_front)
        self.right_image_list=self.get_image_list(self.img_path_for_right)
        self.all_data=[]
        self.current_instance=[]
        #drop down list varibles
        self.phys_cond_var=StringVar()
        self.retro_cond_var=StringVar()
        self.ovr_type_var=StringVar()
        self.mutcd_code_var=StringVar()
        self.previous_index=0
        
        self.play_button_var=0
        #self.jump_distance=0


        #images frame
        self.farme_for_images=tk.Frame(self,relief='solid', bg='gray30')

        self.img_label_1 = tk.Label(self.farme_for_images)
        self.img_label_1.pack(side='left')
        
        self.img_label_2=tk.Label(self.farme_for_images)
        self.img_label_2.pack(side='left',padx=40)
        
        self.img_label_3=tk.Label(self.farme_for_images)
        self.img_label_3.pack(side='left')
        
        
        
        self.img_label_1.bind("<Button-1>",self.clicked)
        self.img_label_1.bind("<ButtonRelease-1>",self.release)
        self.img_label_2.bind("<Button-1>",self.clicked_i2)
        self.img_label_2.bind("<ButtonRelease-1>",self.release_i2)

        self.image=None
        self.image_2=None
        self.image_3=None
        self.image_resized=None
        self.image_resized_2=None
        self.image_resized_3=None


        self.image_resized_copy=None
        self.image_resized_2_copy=None
        self.image_resized_3_copy=None

        self.inital_click=(0,0)
        self.release_point=(0,0)
        self.initial_click_i2=(0,0)
        self.release_point_i2=(0,0)

        self.go_to=0

        self.farme_for_images.pack(side="top", padx="10", pady="10", fill='both', expand=0)
        

        self.farme_for_np=tk.Frame(self,relief='solid', bg='gray90')

        self.btn = tk.Button(self.farme_for_np, text='Next image',command=self.next_img)
        self.btn.pack(side='left', padx='5', pady='10')

    


        self.btn_play = tk.Button(self.farme_for_np, text='Play',command=self.play_button)
        self.btn_play.pack(side='left', padx='5', pady='10')
        # self.btn_stop = tk.Button(self.farme_for_np, text='Stop',command=self.stop_button)
        # self.btn_stop.pack(side='left', padx='5', pady='10')
        self.btn_prev = tk.Button(self.farme_for_np, text='Previous image', command=  self.prev_img)
        self.btn_prev.pack(side='left', padx='5', pady='10')
        
                        
        phys_cond_dd = OptionMenu(self.farme_for_np, self.phys_cond_var, *PHYSICAL_CONDITION,
                                    command=lambda *args: self.set_values('physical_condition'))
        phys_cond_dd.pack(side='left', padx='5', pady='10')

        mutcd_dd = OptionMenu(self.farme_for_np, self.mutcd_code_var, *MUTCD_CODES,
                                command=lambda *args: self.set_values('mutcd_code'))
        mutcd_dd.pack(side='left', padx='5', pady='10')

        ovr_dd = OptionMenu(self.farme_for_np, self.ovr_type_var,
                            *OVERHEAD_TYPE, command=lambda *args: self.set_values('overhead_type'))
        ovr_dd.pack(side='left', padx='5', pady='10')

        #entry
        self.go_to_number=Entry(self.farme_for_np)
        self.go_to_number.pack(side='left',padx='5',pady='5')

        self.jump_btn=tk.Button(self.farme_for_np,text='Jump to here',command=self.jump_image)
        self.jump_btn.pack(side='left',padx='5',pady='5')

        

        

        self.btn_for_removal_of_bounding_box=tk.Button(self.farme_for_np,text='Remove current bbox',command=self.clear_current_instance)
        self.btn_for_removal_of_bounding_box.pack(side='left', padx='5', pady='10')

    
        self.farme_for_np.pack(side="bottom",anchor='w', padx="10", pady="10", fill='both', expand=0)

        #image frame ends
    def play_button(self):
        
        if self.play_button_var==1:
            self.play_button_var=0
            print("updating play button stauts {}".format(self.play_button_var))


        elif self.play_button_var==0:
            self.play_button_var=1
            print("updating play button stauts {}".format(self.play_button_var))


    def set_values(self, type):
        label = None
        label_2 = None
        label_3=None
        if type == 'physical_condition':
            label = self.phys_cond_var.get()
            print("[USER] {} selected".format(label))
            self.current_instance.append(label)

        # elif type == 'retro_condition':
            # label = self.retro_cond_var.get()
        elif type == 'mutcd_code':
            label_2 = self.mutcd_code_var.get()
            print("[USER] {} selected".format(label_2))
            self.current_instance.append(label_2)

        elif type == 'overhead_type':
            label_3 = self.ovr_type_var.get()
            print("[USER] {} selected".format(label_3))
            self.current_instance.append(label_3)
        print("[INFO] Printing inventory till now {}".format(self.all_data))
        print("[INFO] All Data captured! Move to next image")
        print("---------------------------------------------------------------")

        
        
  
    def initialize_dd(self):        
        self.retro_cond_var.set("None")
        self.phys_cond_var.set("None")
        self.mutcd_code_var.set("None")
        self.ovr_type_var.set("None")
    



    def next_img(self):
        print("-----------NEXT---------------")
        print("[USER] YOU CLICKED NEXT")

        print("[INFO] Moving to : ", self.img_index_front_images)
        #print("[INFO] Starting to play the images automatically!")
        
        self.image_name_front=self.front_image_list[self.img_index_front_images]
        self.next_image_front=self.front_image_list[self.img_index_front_images+self.frame_rate]
        self.image_name_right=self.right_image_list[self.img_index_right_images]

        self.title_text.set("n-front{} n+1 front {} n-right {}".format(self.image_name_front,self.next_image_front,self.image_name_right))
        
       
        self.image=Image.open(self.img_path_for_front+'/'+self.image_name_front)
        self.image_resized=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.image_2=Image.open(self.img_path_for_front+'/'+self.next_image_front)
        self.image_resized_2=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.image_3=Image.open(self.img_path_for_front+'/'+self.image_name_right)
        self.image_resized_3=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.img_label_1.img = ImageTk.PhotoImage(self.image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        
        self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)
        
        self.img_label_3.img = ImageTk.PhotoImage(self.image_resized_3)
        self.img_label_3.config(image=self.img_label_3.img)

        self.draw_bounding_for_marked(self.img_index_front_images,self.img_index_front_images+self.frame_rate)

        print("[INFO] Dealing with indices {} {}".format(self.img_index_front_images,self.img_index_front_images+self.frame_rate))
        print("[INFO] Dealing with unique id: {}".format(self.sign_id_gen(self.img_index_front_images,self.img_index_front_images+self.frame_rate)))        
        print("[INFO] Images {} {} {} being shown".format(self.image_name_front,self.next_image_front,self.image_name_right))
        print("-------------------------------")

        #self.current_instance=[]
        self.initialize_dd()
        self.previous_index=self.img_index_front_images
        self.img_index_front_images=1+self.img_index_front_images
        self.img_index_right_images=1+self.img_index_right_images
        print("[Play button status] {}".format(self.play_button_var))
        if self.play_button_var==1:
            self.after(300,self.next_img)

    def jump_image(self):
        print("-----------NEXT---------------")
        self.go_to=self.go_to_number.get()
        print("[USER] YOU CHOOSE TO JUMP to {}".format(self.go_to))
        self.img_index_front_images=int(self.go_to)
        print("[INFO] Moving to : ", self.img_index_front_images)
        #print("[INFO] Starting to play the images automatically!")
        
        self.image_name_front=self.front_image_list[self.img_index_front_images]
        self.next_image_front=self.front_image_list[self.img_index_front_images+self.frame_rate]
        self.image_name_right=self.right_image_list[self.img_index_right_images]

        self.title_text.set("n-front{} n+1 front {} n-right {}".format(self.image_name_front,self.next_image_front,self.image_name_right))
        
       
        self.image=Image.open(self.img_path_for_front+'/'+self.image_name_front)
        self.image_resized=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.image_2=Image.open(self.img_path_for_front+'/'+self.next_image_front)
        self.image_resized_2=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.image_3=Image.open(self.img_path_for_front+'/'+self.image_name_right)
        self.image_resized_3=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        
        self.img_label_1.img = ImageTk.PhotoImage(self.image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        
        self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)
        
        self.img_label_3.img = ImageTk.PhotoImage(self.image_resized_3)
        self.img_label_3.config(image=self.img_label_3.img)

        self.draw_bounding_for_marked(self.img_index_front_images,self.img_index_front_images+self.frame_rate)

        print("[INFO] Dealing with indices {} {}".format(self.img_index_front_images,self.img_index_front_images+self.frame_rate))
        print("[INFO] Dealing with unique id: {}".format(self.sign_id_gen(self.img_index_front_images,self.img_index_front_images+self.frame_rate)))        
        print("[INFO] Images {} {} {} being shown".format(self.image_name_front,self.next_image_front,self.image_name_right))
        print("-------------------------------")

        #self.current_instance=[]
        self.initialize_dd()
        self.previous_index=self.img_index_front_images
        self.img_index_front_images=1+self.img_index_front_images
        self.img_index_right_images=1+self.img_index_right_images

    def prev_img(self):

        print("----------------PREV----------")
        print("[USER] YOU CLICKED PREVIOUS")


        self.previous_index=self.previous_index-1
        self.img_index_front_images=self.previous_index
        self.img_index_right_images=self.previous_index
        print("[INFO] Moving to:",self.previous_index)


        
        self.image_name_front=self.front_image_list[self.previous_index]
        self.next_image_front=self.front_image_list[self.previous_index+self.frame_rate]
        self.image_name_right=self.right_image_list[self.previous_index]



        
        self.title_text.set("n-front{} n+1 front {} n-right {}".format(self.image_name_front,self.next_image_front,self.image_name_right))
        
        print("[INFO] Dealing with indices {} {}".format(self.img_index_front_images,self.img_index_front_images+self.frame_rate))
        print("[INFO] Dealing with unique id: {}".format(self.sign_id_gen(self.img_index_front_images,self.img_index_front_images+self.frame_rate)))  
        print("[INFO] Images {} {} {} being shown".format(self.image_name_front,self.next_image_front,self.image_name_right))

        self.image=Image.open(self.img_path_for_front+'/'+self.image_name_front)
        self.image_resized=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.image_2=Image.open(self.img_path_for_front+'/'+self.next_image_front)
        self.image_resized_2=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.image_3=Image.open(self.img_path_for_front+'/'+self.image_name_right)
        self.image_resized_3=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)

        self.img_label_1.img = ImageTk.PhotoImage(self.image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)
        self.img_label_3.img = ImageTk.PhotoImage(self.image_resized_3)
        self.img_label_3.config(image=self.img_label_3.img)
        print("BOUNDING ID")
        self.draw_bounding_for_marked(self.previous_index,self.previous_index+self.frame_rate)
        self.img_index_front_images=self.previous_index+1
        self.img_index_right_images=self.previous_index+1



#TODO get previous frame 
#TODO How to store values into inventory
#TODO Autoplay
#TODO values
#Storage and autoplay


    def sign_id_gen(self,image_index_1,image_index_2):
        print("[INFO] Generating sign id usig Cantor Pairing function")
        return int(0.5*(image_index_1+image_index_2)*(image_index_1+image_index_2+1)+image_index_2)

    #first click on image 1
    def clicked(self,event):
        self.current_instance=[]
        self.initial_click=(event.x,event.y)
        print("-------------CREATING NEW BOUNDING BOX INSTANCE---------------")
        print("You Have found a new sign in the images indicies {} {}".format(self.previous_index,self.previous_index+1))
        print("Creating new sign id for this sign {}".format(self.sign_id_gen(self.previous_index,self.previous_index+1)))
        
        self.current_instance.append(self.sign_id_gen(self.previous_index,self.previous_index+1))

        print("[INFO] Top-Left Corner of slected image in resized image {} {}".format(self.initial_click[0],self.initial_click[1]))
        #appending image_name_from_panel_1
        print("[INFO] Appending image index {} {}".format(self.previous_index,self.previous_index+1))
        self.current_instance.append(self.previous_index)
        self.current_instance.append(self.previous_index+1)
        self.current_instance.append(self.image_name_front)
        self.current_instance.append(self.next_image_front)
        print("[INFO] Appending top left corner of the image to the current instance")
        self.current_instance.append(self.initial_click)
        
    #release event on image 2
    def release(self,event):
        self.release_point=(event.x,event.y)
        print("[INFO] Releasing mouse at {} {}".format(self.release_point[0],self.release_point[1]))
        print("[INFO] Appending release point into current instance")
        self.current_instance.append(self.release_point)
        
        self.image_resized_copy=self.image_resized

        draw=ImageDraw.Draw(self.image_resized_copy)
        
        draw.rectangle(((self.initial_click),(self.release_point)),outline='red')
        
        self.img_label_1.img = ImageTk.PhotoImage(self.image_resized_copy)
        
        self.img_label_1.config(image=self.img_label_1.img)
        
        print("[INFO] Bounding Boxes drawn on box-1 Now proceed to draw bouding boxes on box two")
        
    #double_click event for second image
    def clicked_i2(self,event):
        self.initial_click_i2=(event.x,event.y)
        print("[INFO] Top-Left Corner of slected image 2 in resized image {} {}".format(self.initial_click_i2[0],self.initial_click_i2[1]))
        #appending image_name_from_panel_1
        print("[INFO] Appending top left corner of the image 2 to the current instance")
        self.current_instance.append(self.initial_click_i2)
    
    #double_click_release
    def release_i2(self,event):
    
        self.release_point_i2=(event.x,event.y)
        print("[INFO] Releasing mouse at 2 {} {}".format(self.release_point_i2[0],self.release_point_i2[1]))
        print("[INFO] Appending release point into current instance")
        
        self.image_resized_2_copy=self.image_resized_2

        
        draw=ImageDraw.Draw(self.image_resized_2_copy)
        draw.rectangle(((self.initial_click_i2),(self.release_point_i2)),outline='red')
        
        self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2_copy)
        self.img_label_2.config(image=self.img_label_2.img)        
        self.current_instance.append(self.release_point_i2)
        print("[INFO] Bounding Boxes drawn on box-2")
        print("[INFO] Appending the current instance {} into global inventory".format(self.current_instance))
        self.all_data.append(self.current_instance)


        

    def clear_current_instance(self):
        print("[INFO] Removing all the bounding boxes in these two images")
        sign_id=self.sign_id_gen(self.previous_index,self.previous_index+1)

        self.image=Image.open(self.img_path_for_front+'/'+self.image_name_front)
        self.image_resized=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.image_2=Image.open(self.img_path_for_front+'/'+self.next_image_front)
        self.image_resized_2=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
        self.image_3=Image.open(self.img_path_for_front+'/'+self.image_name_right)
        self.image_resized_3=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)

        self.img_label_1.img = ImageTk.PhotoImage(self.image_resized)
        self.img_label_1.config(image=self.img_label_1.img)
        self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2)
        self.img_label_2.config(image=self.img_label_2.img)

        print(sign_id)
        for i in self.all_data:
            if i[0]==sign_id:
                print(i[0])
                self.all_data.remove(i)


        print(self.all_data)

    def draw_bounding_for_marked(self,id_1,id_2):
        print('In it')
        sign_id=self.sign_id_gen(id_1,id_2)
        print(sign_id)
        for i in self.all_data:
            if i[0]==sign_id:
                print(i[5])
                print(i[6])
                print(self.image_name_front)
                self.image=Image.open(self.img_path_for_front+'/'+self.image_name_front)
                self.image_resized=self.image.resize((self.width_of_panel,self.height_of_panel),Image.ANTIALIAS)
                draw_o=ImageDraw.Draw(self.image_resized)
                draw_o.rectangle((i[5],i[6]),outline='red')
                self.img_label_1.img = ImageTk.PhotoImage(self.image_resized)
                self.img_label_1.config(image=self.img_label_1.img)
                
                
                draw_p=ImageDraw.Draw(self.image_resized_2)
                draw_p.rectangle((i[7],i[8]),outline='red')
                
                self.img_label_2.img = ImageTk.PhotoImage(self.image_resized_2)
                self.img_label_2.config(image=self.img_label_2.img)        
            else:
                print('nope')


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

