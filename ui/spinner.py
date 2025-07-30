from utils.util import *
import tkinter as tk
import csv
import os, sys
from tkinter import *
import time
import random
from utils.achieve import *
import utils.state

image_refs = []
def load_spin_screen(root, go_to_home):
    title_label = tk.Label(root, text = "Choose a new game!", font = ("Arial", 16))
    text_label = tk.Label(root, text = "Click the button below to start spinning!", font = ("Arial", 16))
    game_label = tk.Label(root, font = ("Arial", 16))
    new_btn = tk.Button(root, text="Choose new game", command=lambda:(choose_game(game_label)))
    back_btn = tk.Button(root, text="Back", command=go_to_home)
    title_label.pack(pady=20)
    text_label.pack(pady=20)
    game_label.pack(pady=20)
    new_btn.pack(pady=20)
    back_btn.pack(pady=20)

def choose_game(game_label, ind = 200):
    global app_frame, image_refs
    choice = ""
    cur_play_path = get_csv_path("games.csv")
    with open(cur_play_path, 'r', newline='') as f:
        reader = list(csv.reader(f))
        reader = reader[1:]  # Skip header

    if not reader:
        game_label.config(text="No games available.")
        return

    # Pick a random game each time
    g = random.choice(reader)
    choice = g[0]
    img = get_resource_path(g[2])
    thumb_size = (220, 220)
    new_img = Image.new("RGB", thumb_size, color="gray")
    new_img.thumbnail(thumb_size)
    new_img = Image.open(img)
    new_img.thumbnail(thumb_size)
    photo = ImageTk.PhotoImage(new_img)
    image_refs.append(photo)
    game_label.config(text=f"{choice}", image = photo, compound=tk.TOP)

    # Update the label

    if ind > 0:
        game_label.after(10, lambda: choose_game(game_label, ind - 1))
    #elif g[1] == "Completed":
        #game_label.after(10, lambda: choose_game(game_label, ind))
    else:
        print(f"[INFO] Final choice: {choice}")
        check_achieve_spin(app_frame)
        result = messagebox.askyesno("Change Game", "Would you like to change the game currently being played to " + choice + "?")
        if(result):
            utils.state.cur_no_game = 0
            change_to_play(choice)
        else:
            check_achieve_pick(app_frame)
            print("user cancelled. game didnt change")

def change_to_play(game):
    csv_path = get_csv_path("games.csv")
    #read in games. if game has progress in_progress, we want to save it but have progress as 
    #"Some progress, not completed"
    #if the game has the same name as the parameter game, we want to write it to curPlay.csv (save for later)
    cur_games = []
    change = []
    with open(csv_path, 'r', newline = '') as new_file:
        csv_reader = csv.reader(new_file)
        for i in csv_reader:
            #title,platform,image,desc
            if(i[0] == game):
                #for cur_play
                change = [i[0], "In Progress", i[2]]
                cur_games.append([i[0], "In Progress", i[2], i[3], i[4], i[5], i[6], i[7]])
            elif(i[1] == "In Progress"):
                print(i)
                print(i[1] + "   prog")
                print(i[2])
                print(i[3])
                cur_games.append([i[0], "Some progress, not completed", i[2], i[3], i[4], i[5], current_time(), i[7]])
            else:
                cur_games.append(i)
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'w', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        for i in cur_games:
            csv_writer.writerow(i)
    csv_path = get_csv_path("curPlay.csv")
    with open(csv_path, 'w', newline = '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(change)