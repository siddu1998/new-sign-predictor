import tkinter as tk
from tkinter import filedialog
import os
from PIL import ImageTk,Image
import cv2
import pandas as pd
# Create empty list for coordinate arrays to be appended to
coords_in_image_1 = []
coords_in_image_2 = []

scale_x=1.0
scale_y=1.0

width=800
height =800

df = pd.DataFrame(columns=['image_before','image_after','x1','y1','x2','y2'])

# Function to be called when mouse is clicked twice
def save_coords_in_image_2(event):
    click_loc = [event.x, event.y]
    empty_loc = [0,0]
    
    if click_loc:
        coords_in_image_2.append(click_loc)
        print("you clicked in image 2", click_loc)
    else:
        coords_in_image_2.append(empty_loc)
        print("you clicked nothing in image2",empty_loc)

# Function to be called when mouse is clicked
def save_coords(event):
    empty_loc=[0,0]
    click_loc = [event.x, event.y]
    if click_loc:
        coords_in_image_1.append(click_loc)
        print("you clicked in image 1", click_loc)
    else:
        coords_in_image_1.append(empty_loc)
        print("you clicked nothing in image2", empty_loc)




def next_img():
    
    image_name=next(imgs)
    next_image=int(image_name[:-4])+1

    print(type(image_name))
    next_image=format(next_image,'06d')+'.jpg'

    image=Image.open(image_name)
    image_resized=image.resize((800,800),Image.ANTIALIAS)
        
    img_label.img = ImageTk.PhotoImage(image_resized)
    img_label.config(image=img_label.img)
    
    image=Image.open(next_image)
    image_resized=image.resize((800,800),Image.ANTIALIAS)

    img2_label.img=ImageTk.PhotoImage(image_resized)
    img2_label.config(image=img2_label.img)


root = tk.Tk()

# Choose multiple images
img_dir = filedialog.askdirectory(parent=root, initialdir="D:/Temp/", title='Choose folder')
os.chdir(img_dir)
imgs = iter(os.listdir(img_dir))

img_label = tk.Label(root)
img_label.pack(side='left')
img_label.bind("<Button-1>",save_coords)


img2_label=tk.Label(root)
img2_label.pack(side='right')
img2_label.bind("<Double-Button-1>",save_coords_in_image_2)

btn = tk.Button(root, text='Next image', command=next_img)
btn.pack()



next_img() # load first image

root.mainloop()

print(coords_in_image_1)
print(coords_in_image_2)
