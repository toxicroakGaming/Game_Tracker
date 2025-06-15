import tkinter as tk
import csv
import os, sys

#get the relative path to the CSV. This assumes it exists (we create games.csv in main.py)
def get_csv_path(filename):
    """Returns the correct writable path for CSV in both dev and PyInstaller"""
    if getattr(sys, 'frozen', False):  # Running in a PyInstaller bundle
        base_path = os.path.dirname(sys.executable)
    else:  # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

#The main work of the "collections" screen
def load_journal_screen(root, go_to_home, go_to_add):
    #get the scrollabale for the game options
    frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(frame)
    #collections label
    label = tk.Label(root, text = "collection", font = ("Arial", 16))
    #get the games from the CSV. Make a list with every game and the status
    game_list = []
    #Read the CSV file
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            print(line)
            game_list.append(line)
        if(game_list == []):
            print(True)
            game_list.append(["N/A","N/A"])
    #scrollbox
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, height=10)
    for game in game_list:
        print(game[0] + " " + game[1])
        listbox.insert(tk.END, game[0] + " Progress: " + game[1])

    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=listbox.yview)
    cur_game = tk.StringVar()
    cur_prog = tk.StringVar()
    cur_prog.set("N/A")
    cur_game.set("N/A")
    #when a game is selected to possibly change
    def on_select(event):
        selected_index = listbox.curselection()
        index = 0
        if selected_index:
            print(selected_index[0])
            csv_path = get_csv_path("games.csv")
            with open(csv_path, 'r') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)
                for line in csv_reader:
                    print(line)
                    if(index == selected_index[0]):
                        csv_path = get_csv_path("curPlay.csv")
                        with open(csv_path, 'w', newline = '') as new_file:
                            csv_writer = csv.writer(new_file)
                            csv_writer.writerow(line)
                            print("changing line to")
                            print(line)
                    index = index + 1
    listbox.bind('<<ListboxSelect>>', on_select)

    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    add_btn = tk.Button(root, text="Add New Game", command=go_to_add)
    change_btn = tk.Button(root, text="Change Game Currently Being Played to Selected", command=change_play_game(cur_game, cur_prog))
    
    label.pack(pady=20)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    frame.pack(padx=10, pady=10)
    add_btn.pack(pady=20)
    change_btn.pack(pady=20)
    back_btn.pack(pady=20)

#change the game in curPlay.csv to the selected game
def change_play_game(name, progress):
    data = [name, progress]
    csv_path = get_csv_path("curPlay.csv")
    with open(csv_path, 'w', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
    print(data)

# Importing Tkinter module
from tkinter import *
def load_add_screen(root, go_to_home):
    label = tk.Label(root, text="Add a game", font=("Arial", 16))
    label2 = tk.Label(root, text="Select Progress", font=("Arial", 16))
    label3 = tk.Label(root, text="Type Game Name", font=("Arial", 16))
    entry = tk.Entry(root, text = "Type Game Name", font = ("Arial", 16))
    v = StringVar(root, "1")

    # Dictionary to create multiple buttons
    values = {"Not Started" : "1",
            "In Progress" : "2",
            "Completed" : "3",
            "100%" : "4"}

    # Loop is used to create multiple Radiobuttons
    # rather than creating each button separately
    choice = tk.StringVar()
    label.pack(pady=20)
    label2.pack(pady=20)
    progress_var = StringVar(root)
    progress_var.set("Not Started")
    values = ["Not Started", "In Progress", "Completed", "100%"]
    for text in values:
        Radiobutton(root, text = text, variable = progress_var, value = text, indicator = 0, 
        background = "light blue").pack(fill=X, ipady=5)
    back_btn = tk.Button(root, text="Back", command=go_to_home)
    add_btn = tk.Button(root, text="Add", command=lambda: add_to_list(entry.get(), progress_var.get()))
    label3.pack(pady=20)
    entry.pack()
    back_btn.pack(pady=20)
    add_btn.pack(pady = 20)

#Update the CSV with the new game, which is the name and the progress
def add_to_list(name, progress):
    data = [name, progress]
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'a', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
