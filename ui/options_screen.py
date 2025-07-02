import tkinter as tk
from PIL import ImageTk, Image 
import csv
import sys, os
from utils.util import *
from utils.state import *

#size of the images on the backgrounds page
thumb_size = (150, 100)
#where are the backgrounds stored?
bg_folder = get_resource_path(r'ui\media\bg')
#keep alive
image_buttons = []


def load_image_screen(root, show_home_screen, show_image_screen):
    global image_buttons
    image_buttons = []  # Clear old references to prevent memory leak

    # Get all image files in the folder
    image_files = [f for f in os.listdir(bg_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    row = 0
    col = 0
    max_cols = 4  # Number of images per row
    top_label = tk.Label(root, text = "Change Background", font = ("Arial", 16))
    top_label.place(x = 450, y = 50)
    #load the images for the options screen
    for img_file in image_files:
        #get paths
        full_path = os.path.join(bg_folder, img_file)
        try:
            #load and resize
            img = Image.open(full_path)
            img.thumbnail(thumb_size)
            tk_img = ImageTk.PhotoImage(img)
            image_buttons.append(tk_img)  # Store reference

            # Create a button with the image
            btn = tk.Button(root, image=tk_img, command=lambda path=full_path: on_background_click(root, path))
            btn.grid(row=row, column=col, padx=10, pady=125)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        except Exception as e:
            print(f"[ERROR] Could not load {img_file}: {e}")
    #other stuff on the screen
    back_btn = tk.Button(root, text="Back to home", command=lambda:show_home_screen())
    load_btn = tk.Button(root, text="Load Custom Images", command=lambda:load_custom_background(root, background_data, bg_folder))
    back_btn.place(x = 450, y = 600)
    load_btn.place(x = 450, y = 500)

#what happens when we click a background image? we want to request to change the background to that image!
def on_background_click(root, path):
    print("click")
    data = [path]
    background_label, bg_image = change_bg(root, path, background_data, data)