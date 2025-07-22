import tkinter as tk
from ui.update_screen import load_update_screen
from ui.home_screen import load_home_screen
from ui.spinner import load_spin_screen
from ui.options_screen import load_image_screen
from ui.journal import load_journal_screen, load_add_screen
from PIL import Image, ImageTk
import csv
import sys, os
from utils.state import *
from utils.util import *
from utils.achieve import *
global app_frame
def show_achieve_screen():
    clear_screen(root)
    load_achieve_screen(root, show_home_screen)

def show_spin_screen():
    clear_screen(root)
    load_spin_screen(root, show_home_screen)

def show_home_screen():
    clear_screen(root)
    load_home_screen(root, show_update_screen, show_journal_screen, show_image_screen, show_spin_screen, show_achieve_screen)

def show_update_screen():
    clear_screen(root)
    load_update_screen(root, show_home_screen)

def show_journal_screen():
    clear_screen(root)
    load_journal_screen(root, show_home_screen, show_add_screen, show_journal_screen)

def show_add_screen():
    clear_screen(root)
    load_add_screen(root, show_journal_screen)

def show_remove_screen():
    clear_screen(root)
    load_remove_screen(root, show_journal_screen)   

def show_image_screen():
    clear_screen(root)
    load_image_screen(root, show_home_screen, show_image_screen)


#load the default (home) screen
root = tk.Tk()
root.title("Game Tracker")
root.geometry("1000x800")
img_path = get_resource_path(current_bg_path)
# Load path saved previously
bg_path = get_persistent_bg_image()
# Show it
background_label, current_bg_path = set_background(root, bg_path, background_data)
print("[DEBUG] background_data id:", id(background_data))
ensure_csv_exists("games.csv")
if (ensure_csv_exists("curPlay.csv")):
    data = default_game
    csv_path = get_csv_path("curPlay.csv")
    with open(csv_path, 'w', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
#for importing from pre 1.1.1, function is in util.py
ensure_csv_exists("achieve.csv")
check_update()
#load from the csv file into our instance
load_achieve()
# Start at home screen
show_home_screen()
app_frame = tk.Frame(root)
app_frame.pack()
root.mainloop()