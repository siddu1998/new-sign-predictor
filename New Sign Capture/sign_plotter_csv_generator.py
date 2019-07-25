import tkinter as tk
from tkinter import filedialog
import os
from PIL import ImageTk,Image
import cv2

# Create empty list for coordinate arrays to be appended to
coords = []

# Function to be called when mouse is clicked
def save_coords(event):
    click_loc = [event.x, event.y]
    print("you clicked on", click_loc)
    coords.append(click_loc)

def next_img():
    
    image_name=next(imgs)
    next_image=int(image_name[:-4])+1
    print(image_name)
    print(format(next_image,'05d')+'.jpg')
    
    
    img_label.img = ImageTk.PhotoImage(Image.open(image_name))
    img_label.config(image=img_label.img)



root = tk.Tk()

# Choose multiple images
img_dir = filedialog.askdirectory(parent=root, initialdir="D:/Temp/", title='Choose folder')
os.chdir(img_dir)
imgs = iter(os.listdir(img_dir))

img_label = tk.Label(root)
img_label.pack()
img_label.bind("<Button-1>",save_coords)

btn = tk.Button(root, text='Next image', command=next_img)
btn.pack()

next_img() # load first image

root.mainloop()

print(coords)
