import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import sys, os
from PIL import Image, ImageTk
import shutil

background_data = {"label": None, "img": None}


def ensure_csv_exists(name):
    csv_path = get_csv_path(name)
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'progress'])
        return True
    return False


def get_root_path():
    if hasattr(sys, "_MEIPASS"):
        # When bundled as an .exe
        return sys._MEIPASS
    else:
        # When running as a .py file, use the working directory from which the script was launched
        return os.path.abspath(os.getcwd())

def get_csv_path(filename):
    return os.path.join(get_root_path(), filename)


def get_bg_image():
    csv_path = get_csv_path("curBG.csv")
    if(ensure_csv_exists("curBG.csv")):
        data = [get_resource_path(r"ui\media\bg\default_bg.png")]
        with open(csv_path, 'w', newline = '') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(data)
    with open(csv_path, 'r', newline = '') as new_file:
        csv_reader = csv.reader(new_file)
        return next(csv_reader)[0]


def set_background(root, image_path, holder):
    current_bg_path = image_path
    print(current_bg_path)
    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return None, None

    try:
        img = Image.open(image_path)
        img = img.resize((max(root.winfo_width(), 1000), max(root.winfo_height(), 800)))

        # Create and store PhotoImage in holder to keep reference
        holder["img"] = ImageTk.PhotoImage(img)

        # Check if label exists and is not destroyed
        if holder.get("label") and holder["label"].winfo_exists():
            holder["label"].config(image=holder["img"])
        else:
            holder["label"] = tk.Label(root, image=holder["img"])
            holder["label"].place(x=0, y=0, relwidth=1, relheight=1)

        holder["label"].lower()

        print(f"[INFO] Background loaded from: {image_path}")
        return holder["label"], holder["img"]

    except Exception as e:
        print(f"[ERROR] Failed to load image: {e}")
        return None, None

#for loading images and such
def get_resource_path(relative_path):
    """Returns the absolute path to a resource file (image, csv, etc.)"""
    if hasattr(sys, '_MEIPASS'):
        # If bundled into an EXE, use the temp folder PyInstaller extracts to
        base_path = sys._MEIPASS
    else:
        # If running locally, use the directory of the current script
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def load_custom_background(root, holder, backgrounds_folder):
    filepath = filedialog.askopenfilename(
        title="Select Background Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if filepath:
        # Optional: Copy the file into backgrounds folder
        dest_path = os.path.join(backgrounds_folder, os.path.basename(filepath))
        shutil.copy(filepath, dest_path)

        # Then set background using copied file path
        change_bg(root, dest_path, holder, [dest_path])
    #confirm with the user that they want to Change the game currently being played
def change_bg(root, dest_path, holder, data):
    global background_label, current_bg_path
    result = messagebox.askyesno("Confirm New Background", "Would you like to change your background to the selected image?")
    if result:
        csv_path = get_csv_path("curBG.csv")
        with open(csv_path, 'w', newline = '') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(data)
            print(data)
        background_label, current_bg_path = set_background(root, dest_path, holder)
        return background_label, current_bg_path
    else:
        print("User canceled deletion.")
    return None, None

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    current_bg_path = get_bg_image()
    background_label, bg_image = set_background(root, current_bg_path, background_data)