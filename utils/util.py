import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import sys, os
from PIL import Image, ImageTk
import shutil
import re
from utils.Date import current_time
from utils.achieve import check_achieve_write
import utils.state

#this file contains utility functions taht can be used in other files
app_frame = None
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
# ["title", "platform", "image", "desc", "added", "start", "last", "completed"]
# added is when it was added, start is when it was started, last is when it was last played
# completed is when it was completed
#i["title"], i["status"], i["image"], i["desc"], i["added"], i["start"],
                                            #i["last"], i["completed"])
default_game = {"title":"N/A",
    "status":"N/A",
    "image": r"ui\media\games\no_image.jpg",
    "desc":r"ui\desc\def_desc.txt",
    "added":current_time(),
    "last":"N/A",
    "completed":"N/A",
    "start":"NA"
    }

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
        check_achieve_write(app_frame)
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


def check_update():
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'r') as f:
        head = csv.DictReader(f)
        headers = head.fieldnames
        #if we make any updates in the future, we might need to change this
        missing = headers == None or [col for col in ["added"] if col not in headers]
        if missing:
            print("Missing columns:", missing)
        #some columns were added later on, so if they are not here, we need to make them.
        if(missing):
            header = [["title", "platform", "image", "desc", "added", "start", "last", "completed"]]
            with open(csv_path, 'r', newline = '') as w:
                reader = csv.reader(w)
                #get the games
                games = header
                for i in reader:
                    #added
                    i.append(current_time())
                    #started, we know that if it doesnt have progress "not started", then you started it before
                    #since we dont know when, all the parameters will be set to today
                    if(i[1] != "Not Started"):
                        i.append(current_time())
                        i.append(current_time())
                        i.append(current_time())
                        if(i[1] == "100%" or i[1] == "Completed"):
                            i.append(current_time())
                        else:
                            i.append("N/A")
                    else:
                        i.append("N/A")
                        #last
                        i.append("N/A")
                        
                        #completed
                        i.append("N/A")
                    games.append(i)
                with open(csv_path, 'w', newline = '') as new_file:
                    writer = csv.writer(new_file)
                    ind = 0
                    for j in games:
                        print("this is j")
                        print(j)
                        writer.writerow(j)
    csv_path = get_csv_path("achieve.csv")
    total_ach = 17
    with open(csv_path, 'r') as a:
        temp = []
        reader = csv.reader(a)
        for i in reader:
            temp.append(i)
        if(len(temp) != total_ach):
            while(len(temp) < total_ach):
                temp.append([0])
        with open(csv_path, 'w', newline = '') as new_file:
            writer = csv.writer(new_file)
            for i in temp:
                writer.writerow(i)
    print("exist?")
    if(ensure_csv_exists("favorites.csv")):
        games_csv = get_csv_path("games.csv")
        fav_csv = get_csv_path("favorites.csv")
        with open(games_csv, 'r') as f:
            with open(fav_csv, 'w', newline = '') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                for i in f:
                    writer.writerow(["False"])
    #create the streak csv. The bulk of this code will be in achieve.csv
    #streak will show both on the home screen and in achievments
    if(ensure_csv_exists("streak.csv")):
        streak_csv = get_csv_path("streak.csv")
        with open(streak_csv, 'w', newline = '') as f:
            writer = csv.writer(f)
            #day, current, longest
            writer.writerow([current_time(), 0, 0]) 

#load from the csv into local memory
def load_games():
    utils.state.game_store = []
    games_csv = get_csv_path("games.csv")
    fav_csv = get_csv_path("favorites.csv")
    tag_conn_csv = get_csv_path("tag_connect.csv")
    with open(games_csv, 'r') as game:
        with open(fav_csv, 'r') as fav:
                with open(tag_conn_csv, 'r') as tag_conn:
                    tag_reader = csv.reader(tag_conn)
                    game_reader = csv.reader(game)
                    fav_reader = csv.reader(fav)
                    next(game_reader)
                    #title,platform,image,desc,added,start,last,completed
                    for i in game_reader:
                        favo = next(fav_reader)
                        tags = next(tag_reader)
                        #print(tags)
                        #print(tags[0])
                        utils.state.game_store.append({"title":i[0], "status":i[1], "image":i[2], "desc":i[3], "added":i[4], "start":i[5],
                                                        "last":i[6], "completed":i[7], "favorite":favo, "tags": tags})
    print("loaded")



#save to CSVs
def save_games():
    games_csv = get_csv_path("games.csv")
    fav_csv = get_csv_path("favorites.csv")
    tag_conn_csv = get_csv_path("tag_connect.csv")
    with open(games_csv, 'w', newline = '') as game:
        game_writer = csv.writer(game)
        #title,platform,image,desc,added,start,last,completed
        for i in utils.state.game_store:
            game_writer.writerow([i["title"], i["status"], i["image"], i["desc"], i["added"], i["start"],
                                            i["last"], i["completed"]])
    with open(fav_csv, 'w', newline = '') as fav:
        fav_writer = csv.writer(fav)
        for i in utils.state.game_store:
            fav_writer.writerow(i["favorite"])
    with open(tag_conn_csv, 'w', newline = '') as tag_conn:
        tag_writer = csv.writer(tag_conn)
        for i in utils.state.game_store:
            tag_writer.writerow(i["tags"])

#getting cached images (so that we dont have to create new photoImages every time)
def get_cached_image(path, thumb_size):
    if path in utils.state.image_cache:
        return utils.state.image_cache[path]

    if os.path.exists(path):
        img = Image.open(path)
    else:
        img = Image.new("RGB", thumb_size, color="gray")

    img.thumbnail(thumb_size)
    photo = ImageTk.PhotoImage(img)
    utils.state.image_cache[path] = photo
    return photo