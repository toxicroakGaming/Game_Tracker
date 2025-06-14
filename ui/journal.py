import tkinter as tk
import csv

def load_journal_screen(root, go_to_home, go_to_add):
    games = ""
    label = tk.Label(root, text = "collection", font = ("Arial", 16))
    with open('games.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_file)
        for line in csv_reader:
            print(line)
            games += "Game: " +line[0] + ", Progress: " + line[1] + "\n"

    game_label = tk.Label(root, text = games, font = ("Arial", 16))

    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    add_btn = tk.Button(root, text="Add New Game", command=go_to_add)
    
    label.pack(pady=20)
    add_btn.pack(pady=20)
    back_btn.pack(pady=20)
    game_label.pack(pady=20)

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

def add_to_list(name, progress):
    data = [name, progress]
    with open('games.csv', 'a', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
