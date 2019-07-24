import tkinter as tk
from tkinter import filedialog
import os

# Create empty list for coordinate arrays to be appended to
coords = []

# Function to be called when mouse is clicked
def save_coords(event):
    click_loc = [event.x, event.y]
    print("you clicked on", click_loc)
    coords.append(click_loc)

# Function to load the next image into the Label
def next_img():
    img_1,img_2=pairwise(imgs)
    img_1=Image.open(img_1)
    img_2=Image.open(img_2)
    img_front_label_first.img = tk.PhotoImage(img_)1
    img_front_label_first.config(image=img_front_label_first.img)

    



root = tk.Tk()

# Choose multiple images
img_dir = filedialog.askdirectory(parent=root, initialdir="C:/smaram7/Desktop", title='Choose folder')
os.chdir(img_dir)
imgs = iter(os.listdir(img_dir))

img_front_label_first = tk.Label(root)
img_front_label_second = tk.Label(root)

img_front_label_first.pack()
img_front_label_second.pack()





img_front_label_first.bind("<Button-1>",save_coords)
img_front_label_second.bind("<Button-1>",save_coords)



btn = tk.Button(root, text='Next pair', command=next_img)
btn.pack()

next_img() # load first image

root.mainloop()

print(coords)