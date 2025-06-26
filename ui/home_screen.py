import tkinter as tk
from PIL import ImageTk, Image 
import csv
import sys, os

def get_root_path():
    if hasattr(sys, "_MEIPASS"):
        # When bundled as an .exe
        return sys._MEIPASS
    else:
        # When running as a .py file, use the working directory from which the script was launched
        return os.path.abspath(os.getcwd())

def get_csv_path(filename):
    return os.path.join(get_root_path(), filename)

def resource_path(relative_path):
    """ Get the absolute path to a resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



def load_home_screen(root, go_to_update, go_to_journal):
    label = tk.Label(root, text="Welcome to Game Tracker!", font=("Arial", 16))
    label.pack(pady=20)
    #read curPlay.csv to get the current game. It is automatically made to "N/A,N/A"
    csv_path = get_csv_path("curPlay.csv")
    play = "Currently, you are playing:\n"
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            play += line[0] + " with progress: " + line[1]
    play_label = tk.Label(root, text=play, font=("Arial", 16))

    image_path = resource_path("ui/media/games.png")
    image = Image.open(image_path)
    resized_image = image.resize((275, 225))
    photo_image = ImageTk.PhotoImage(resized_image)
    label2 = tk.Label(root, image=photo_image)
    label2.image = photo_image
    btn = tk.Button(root, text="Updates", command=go_to_update)
    btn2 = tk.Button(root, text="Collection", command=go_to_journal)
    play_label.pack()
    btn.pack()
    btn2.pack()
    label.pack(pady=20)
    label2.pack()