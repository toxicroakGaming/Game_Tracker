import tkinter as tk
from PIL import ImageTk, Image 
import csv
import sys, os
from utils.util import *
from utils.achieve import get_streak

def get_root_path():
    if hasattr(sys, "_MEIPASS"):
        # When bundled as an .exe
        return sys._MEIPASS
    else:
        # When running as a .py file, use the working directory from which the script was launched
        return os.path.abspath(os.getcwd())


def load_home_screen(root, go_to_update, go_to_journal, go_to_image, go_to_spin, go_to_achieve):
    load_games()
    
    label = tk.Label(root, text="Welcome to Game Tracker!", font=("Arial", 16))
    label.pack(pady=20)
    get_streak(root)
    #read curPlay.csv to get the current game. It is automatically made to "N/A,N/A"
    csv_path = get_csv_path("curPlay.csv")
    play = "Currently, you are playing:\n"
    print(csv_path)
    print("above me is the csv path")
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            play += line[0] + " with progress: " + line[1]
            #load the image
            src = line[2]
            img = Image.open(resolve_image_path(src))
            img = img.resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            play_label = tk.Label(root, image=img_tk, text=play,compound="bottom")
            play_label.image = img_tk
            play_label.pack()
    image_path = get_resource_path("ui/media/games.png")
    image = Image.open(image_path)
    resized_image = image.resize((275, 225))
    photo_image = ImageTk.PhotoImage(resized_image)
    label2 = tk.Label(root, image=photo_image)
    label2.image = photo_image
    btn = tk.Button(root, text="Updates", command=go_to_update)
    col_btn = tk.Button(root, text="Collection", command=go_to_journal)
    ch_btn = tk.Button(root, text="Wheel of Choices", command=go_to_spin)
    bg_btn = tk.Button(root, text="Change Background", command=go_to_image)
    ach_btn = tk.Button(root, text="Achievements", command=go_to_achieve)
    csv_path = get_csv_path("streak.csv")
    streak_label = tk.Label(root, text="!", font=("Arial", 16))
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        cur = next(reader)
        streak_label = tk.Label(text="Current Daily Streak: " + cur[1] + "\n" +
            "Max streak: " + cur[2], font=("Arial", 16))
    play_label.pack()
    btn.pack()
    col_btn.pack()
    ach_btn.pack()
    ch_btn.pack(pady=20)
    bg_btn.pack()
    label.pack(pady=20)
    streak_label.pack(pady=20)
    label2.pack()