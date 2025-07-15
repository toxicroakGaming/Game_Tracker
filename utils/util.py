import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import sys, os
from PIL import Image, ImageTk
import shutil
import re

#this file contains utility functions taht can be used in other files

#for loading images and such, we want to get the relative path
def get_resource_path(relative_path):
    """Returns the absolute path to a resource file (image, csv, etc.)"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#for keeping references and not getting garbage collected
#the defaults for if there is no game
default_game = [
    "N/A",
    "N/A",
    r"ui\media\games\no_image.jpg",
    r"ui\desc\def_desc.txt",
    r"ui\desc\def_desc.txt"
]
background_data = {"label": None, "img": None}
games_holder = {"games": None, "sort": None}


#we want to create the CSV's needed if they dont exist
def ensure_csv_exists(filename):
    csv_path = get_csv_path(filename)  # You get the full path, e.g., ...\GameTracker\curBG.csv
    folder = os.path.dirname(csv_path)  # Extract the folder path

    if not os.path.exists(folder):
        os.makedirs(folder)  # Create folder(s) if they don't exist

    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as f:
            # Possibly write headers or initial data here if needed
            pass
        return True  # Indicates file was created
    return False  # File already existed

#for getting relative paths
def get_root_path():
    if hasattr(sys, "_MEIPASS"):
        # When bundled as an .exe
        return sys._MEIPASS
    else:
        # When running as a .py file, use the working directory from which the script was launched
        return os.path.abspath(os.getcwd())

def get_csv_path(filename):
    return os.path.join(get_user_data_dir(), filename)

#get the image thats the background image
def get_bg_image():
    csv_path = get_csv_path("curBG.csv")
    if ensure_csv_exists("curBG.csv"):
        data = [r"ui\media\bg\default_bg.png"]
        with open(csv_path, 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(data)

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            relative_path = next(reader)[0]
        except StopIteration:
            # File is empty, write default and return it
            default_path = get_resource_path(r"ui\media\bg\default_bg.png")
            with open(csv_path, 'w', newline='') as new_file:
                csv_writer = csv.writer(new_file)
                csv_writer.writerow([default_path])
            relative_path = default_path
    return relative_path

def set_background(root, image_path, holder):

    if not os.path.exists(image_path):
        print(f"[ERROR] Image not found: {image_path}")
        return None, None

    try:
        img = Image.open(image_path)
        img = img.resize(
            (
                max(root.winfo_width(), 1000),
                max(root.winfo_height(), 800)
            )
        )

        # Store PhotoImage so it doesn't get garbage-collected
        holder["img"] = ImageTk.PhotoImage(img)

        # If label exists, reuse it
        if holder.get("label") and holder["label"].winfo_exists():
            holder["label"].config(image=holder["img"])
        else:
            holder["label"] = tk.Label(root, image=holder["img"])
            holder["label"].place(x=0, y=0, relwidth=1, relheight=1)

        # Ensure it stays behind other widgets
        holder["label"].lower()

        print(f"[INFO] Background loaded from: {image_path}")

        return holder["label"], holder["img"]

    except Exception as e:
        print(f"[ERROR] Failed to load image: {e}")
        return None, None

def load_custom_background(root, holder, backgrounds_folder):
    filepath = filedialog.askopenfilename(
        title="Select Background Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if filepath:
        # Make sure the backgrounds folder exists
        if not os.path.exists(backgrounds_folder):
            os.makedirs(backgrounds_folder)

        # Choose destination filename: you can customize this (e.g., always save as "custom_bg.jpg")
        dest_filename = os.path.basename(filepath)
        dest_path = os.path.join(backgrounds_folder, dest_filename)

        # Copy the selected image into your app's persistent folder
        shutil.copy(filepath, dest_path)

        # For storing in csv, use the absolute path (you could also store relative if you prefer)
        # Here we'll store the absolute path
        relative_path = dest_path

        # Then set background using copied file path
        change_bg(root, dest_path, holder)
    #confirm with the user that they want to Change the game currently being played
def change_bg(root, filepath, holder):
    global background_label, current_bg_path

    if not filepath:
        print("[WARN] No file selected.")
        return None, None

    result = messagebox.askyesno("Confirm New Background", "Would you like to change your background to the selected image?")
    if result:
        # Prepare destination folder inside app data
        app_data_dir = os.path.join(os.getenv('APPDATA'), 'GameTracker', 'bg_images')
        os.makedirs(app_data_dir, exist_ok=True)

        filename = os.path.basename(filepath)
        dest_path = os.path.join(app_data_dir, filename)

        # Copy the selected file to app data folder
        shutil.copy(filepath, dest_path)

        # Save the absolute path to CSV for persistence
        csv_path = get_csv_path("curBG.csv")
        with open(csv_path, "w", newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([dest_path])

        # Update the background immediately
        background_label, current_bg_path = set_background(root, dest_path, holder)
        return background_label, current_bg_path

    else:
        print("User canceled background change.")
        return None, None

def clear_screen(root):
    for widget in root.winfo_children():
        widget.destroy()
    current_bg_path = get_bg_image()
    background_label, bg_image = set_background(root, current_bg_path, background_data)



def edit_text_file(root, file_path, go_to_journal, on_back=True):
    # Clear any previous widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Frame to hold the editor
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Title
    tk.Label(frame, text=f"Editing: {os.path.basename(file_path)}", font=("Arial", 16)).pack(pady=5)

    # Text widget
    text_widget = tk.Text(frame, wrap="word", width=80, height=25)
    text_widget.pack(fill="both", expand=True)

    # Load the file
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            text_widget.insert("1.0", content)

    # Save button
    def save_changes():
        new_content = text_widget.get("1.0", tk.END).rstrip()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        messagebox.showinfo("Saved", "Changes saved successfully!")
        go_to_journal()

    save_button = tk.Button(frame, text="Save", command=lambda:(save_changes()))
    save_button.pack(side="left", padx=10, pady=10)

    # Back button
    if on_back:
        back_button = tk.Button(frame, text="Back", command=lambda : go_to_journal())
        back_button.pack(side="right", padx=10, pady=10)

def create_description(game_title):
    # Clean up the title
    safe_title = "".join(c for c in game_title if c.isalnum() or c in (" ", "_", "-")).rstrip()
    filename = f"{safe_title}.txt"

    # Instead of using 'ui/desc', we use user data dir
    desc_dir = os.path.join(get_user_data_dir(), "desc")

    # ✅ Make sure the directory exists
    if not os.path.exists(desc_dir):
        os.makedirs(desc_dir)

    # Full path to the file
    desc_path = os.path.join(desc_dir, filename)

    # ✅ If it doesn't exist, create it
    if not os.path.exists(desc_path):
        with open(desc_path, "w", encoding="utf-8") as f:
            f.write("No description yet.")
        print(f"[INFO] Created description file: {desc_path}")
    else:
        print(f"[INFO] Description file already exists: {desc_path}")

def delete_description(game_title):
    safe_title = "".join(c for c in game_title if c.isalnum() or c in (" ", "_", "-")).rstrip()
    filename = f"{safe_title}.txt"
    
    desc_path = os.path.join("ui", "desc", filename)

    if os.path.exists(desc_path):
        os.remove(desc_path)
        print(f"[INFO] Deleted description file: {desc_path}")
    else:
        print(f"[WARNING] Description file not found: {desc_path}")

def browse_image(image_path, image_label):
    filepath = filedialog.askopenfilename(
        title="Select Game Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")]
    )
    if filepath:
        image_path.set(filepath)
        image_label.config(text=os.path.basename(filepath))
    else:
        print("N/A?")
        image_path.set(default_game[2])
        image_label.config(text="No image selected")

def get_user_data_dir():
    if sys.platform == "win32":
        # On Windows, use %APPDATA%
        return os.path.join(os.getenv('APPDATA'), 'GameTracker')
    else:
        # On macOS or Linux, use ~/.game_tracker
        return os.path.expanduser('~/.game_tracker')

def resolve_image_path(path):
    if os.path.isabs(path):
        return path
    return get_resource_path(path)

def get_persistent_bg_image():
    csv_path = get_csv_path("curBG.csv")
    # Make sure the csv exists
    if ensure_csv_exists("curBG.csv"):
        # Default to bundled default image
        default_resource = get_resource_path("ui/media/bg/default_bg.png")
        return default_resource
    # Read the saved image path
    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        saved_path = next(reader)[0]
        # If saved path exists, use it
        if os.path.exists(saved_path):
            return saved_path
        # Else fallback to bundled default
        return get_resource_path("ui/media/bg/default_bg.png")

def sanitize_filename(name):
    # Remove or replace characters not allowed in filenames
    name = name.strip()
    return re.sub(r'[\\/*?:"<>|\'\,`]', '', name)