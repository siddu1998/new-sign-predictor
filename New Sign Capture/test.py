import tkinter as tk
from tkinter import filedialog
import os
from PIL import ImageTk,Image
import cv2
import pandas as pd



class UI:
    
    def __init__(width,height,coords_path_file,right_image_dir):

        self.image_dir_for_right_side_images=image_dir_for_right_side_images
        self.image_dir_for_front_side_images=image_dir_for_front_side_images

        sub_folders_images_right=sorted(os.listdir(image_dir_for_right_side_images))
        sub_folders_images_front=sorted(os.listdir(image_dir_for_front_side_images))

        jpg_count_right=sum(1 for f in sub_folders_images_right if f.endswith(".jpg"))
        jpg_count_front=sum(1 for f in sub_folders_images_front if f.endswith(".jpg"))

        if(jpg_count_front==jpg_count_right):
            self.input_image_names_front=sub_folders_images_front
            self.input_image_names_right=sub_folders_images_right
        

        self.width=width
        self.height=height

        self.current_index_of_front=0
        self.current_index_of_right=0

        self.coord_file=pd.read_csv(coords_path_file)
        self.sign_inventory_df=pd.read_csv(sign_inventory_df)

        # 3 image panels
        self.image_panel_image1=None
        self.image_panel_image2=None
        self.image_panel_image3=None

        #current set instance
        self.current_image_set=None

        self.next_lidar_frame_button = None
        self.prev_lidar_frame_button = None

        self.frame2imgpath_front={}
        self.frame2imgpath_right={}
        self.create_frame2imgpath()

        self.bboxes =defaultdict(list)
        self.bboxesOTHER={}
        self.current_bbox=[]

        self.sign_gps=defaultdict(dict)

        self.sign_id=1
        self.frame_rate=1
        self.image_index=0
        self.scale_x=1.0
        self.scale_y=1.0

        self.master=Tk()
        self.master.protocol("WM_DELETE_WINDOW",self.on_closing)

        self.title_text=StringVar()
        self.roi_val_image_1=IntVar()
        self.roi_val_image_2=IntVar()

        self.win=None
        self.phys_cond_var=StringVar()
        self.retro_cond_var=StringVar()
        self.ovr_type_var=StringVar()
        self.mutcd_code_var=StringVar()

        self.create_df_headers()
        self.start_ui()

        def create_df_headers(self):
            columns_list=['frame_id_1','frame_id_2','bbox1_x1','bbox1_y1','bbox1_x2','bbox1_y2','bbox2_x1','bbox2_y1','bbox2_x2','bbox2_y2']
            for column in columns_list:
                self.sign_inventory_df['column']=None
        
        def start_ui(self):
            self.roi_val_image_1.set(2)
            self.roi_val_image_2.set(2)
            self.create_ui()
            self.create_bindings()
            self.master.mainloop()
        
        def create_frame2imgpath(self):
            input_image_names_front=self.input_image_names_front
            input_image_names_right=self.input_image_names_right
            for (frame_id,frame_path) in enumerate(input_image_names_front):
                self.frame2imgpath_front[frame_id]=frame_path
            for(frame_id,frame_path) in enumerate(input_image_names_right):
                self.frame2imgpath_right[frame_id]=frame_path

        def get_next_image_for_roi_frame(self):
            if self.image_index<len(self.input_image_names_front):
                #front image 1
                img_path_front_image_1=os.path.join(self.image_dir_for_front_side_images,self.input_image_names_front[self.image_index+self.frame_rate])
                img_path_front_image_2=os.path.join(self.image_dir_for_front_side_images,self.input_image_names_front[self.image_index+self.frame_rate+1])
                img_path_right_image=os.path.join(self.image_dir_for_right_side_images,self.input_image_names_right[self.image_index+self.frame_rate])

                img1=cv2.imread(img_path_front_image_1)
                img2=cv2.imread(img_path_front_image_2)
                img3=cv2.imread(img_path_right_image)

                y_=img1.shape[0]
                x_=img1.shape[1]
                self.scale_x=float(self.width)/x_
                self.scale_y=float(self.height)/y_


                img1=cv2.resize(img1,(self.width,self.height))
                img2=cv2.resize(img2,(self.width,self.height))
                img3=cv2.resize(img3,(self.width,self.height))
                
                return [img1,img2,img3]



    def read_next_image(self):
        if self.image_index < len(self.input_image_names):
                #front image 1
                img_path_front_image_1=os.path.join(self.image_dir_for_front_side_images,self.input_image_names_front[self.image_index])
                img_path_front_image_2=os.path.join(self.image_dir_for_front_side_images,self.input_image_names_front[self.image_index+self.frame_rate])
                img_path_right_image=os.path.join(self.image_dir_for_right_side_images,self.input_image_names_right[self.image_index+self.frame_rate])

                print("[INFO]  front img_path: {}".format(img_path_front_image_1))
                print("[INFO] front img_path for image 5m ahead {}".format(img_path_front_image_2))
                print("[INFO]  right img_path: {}".format(img_path_right_image))
                
                img1=cv2.imread(img_path_front_image_1)
                img2=cv2.imread(img_path_front_image_2)
                img3=cv2.imread(img_path_right_image)

                self.org_size=img1.shape
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

                y_=img.shape[0]
                x_=img.shape[1]
                
                self.scale_x=float(self.width)/x_
                self.scale_y=float(self.height)/y_

                img1=cv2.resize(img1,(self.width,self.height))
                img2=cv2.resize(img2,(self.width,self.height))
                img3=cv2.resize(img3,(self.width,self.height))

                self.org_img=img1.copy()
                self.curr_img=img1.copy()

                self.org_img2=img2.copy()
                self.curr_img=img2.copy()

                self.title_text.select.set('Showing images {}:front {}:front {}:right'.format(self.input_image_names_front[self.image_index],self.input_image_names_front[self.image_index+self.frame_rate],self.input_image_names_right[self.image_index+self.frame_rate]))
                return [img1,img2,img3]
            else:
                print("looks like you are done")

    def create_ui(self):
        images=read_next_image()[0]
        img1=images[0]
        img2=images[1]
        img3=images[2]

        left_frame_front = Frame(self.master, borderwidth=2, relief='solid', bg='gray50')
        right_frame_front =Frame(self.master,borderwidth=2,relief='solid',bg='gray50')
        right_frame_right =Frame(self.master,borderwidth=2,relief='solid',bg='gray50')
        
        self.title = Label(left_frame_front, textvariable=self.title_text, bg='gray20', fg='white',activebackground='gray20')
        self.title.pack(side='top')

        self.image_panel_image1=Label(left_frame_front,image=img1)
        self.image_panel_image2=Label(right_frame_front,image=img2)
        self.image_panel_image3=Label(right_frame_right,image=img3)

        left_frame_front.pack(side='left')
        right_frame_front.pack(side='left')
        right_frame_right.packt(side='left')

        frame1=Frame(left_frame,relief='solid',bg='gray30')
        frame1.pack(side="top", padx="10", pady="10", fill='both', expand=1)

        clear_prev_bbox_button = Button(frame1, command=self.clear_prev_bbox, text='Clear Current BBox')
        clear_prev_bbox_button.pack(side='left', padx='5', pady='10')
        #self.next_lidar_frame_button =  Button(frame3,command=self.choose_next_function,text="Next Sign in Inventory", state='active')
        #self.next_lidar_frame_button.pack(side="left", padx="10", pady="10")
        #self.prev_lidar_frame_button = Button(frame3,command=self.choose_prev_function,text="Prev Sign in Inventory", state='active')
        #self.prev_lidar_frame_button.pack(side="left", padx="10", pady="10")
    
    def initialize_dd(self):
        self.retro_cond_var.set("None")
        self.phys_cond_var.set("None")
        self.mutcd_code_var.set("None")
        self.ovr_type_var.set("None")
    
    def create_bindings(self):
        # Left mouse button press
        self.image_panel_image1.bind('<ButtonPress-1>', self.clicked_image_1)
        # Mouse motion
        self.image_panel_image1.bind('<Motion>', self.motion_image_1)
        # Left mouse button release
        self.image_panel_image1.bind('<ButtonRelease-1>', self.release_image_1)
        # Left mouse button
        self.image_panel_image1.bind('<Button-3>', self.label_bbox_image_1)
        # Left mouse button for Macs
        self.image_panel_image1.bind('<Button-2>', self.label_bbox_image_1)
        # Left, Right arrow keys
        self.master.bind('<Left>', self.show_prev_sign)
        self.master.bind('<Right> ', self.show_next_sign)
    def update_ui(self):
        img = self.read_next_image()
        self.draw_bboxes()
        self.update_panel(self.curr_img)
