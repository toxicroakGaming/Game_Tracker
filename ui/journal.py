import tkinter as tk
import csv
import os, sys
from tkinter import *
from utils.util import *

#The main work of the "collections" screen
def load_journal_screen(root, go_to_home, go_to_add, go_to_journal):
    #get the scrollabale for the game options
    frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(frame)
    #collections label
    label = tk.Label(root, text = "Collection", font = ("Arial", 16))
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
                            print("changing curPlay line to (selection)")
                            print(line)
                            cur_game.set(line[0])
                            cur_prog.set(line[1])
                            print(cur_game.get() + " " + cur_prog.get())
                    index = index + 1
    listbox.bind('<<ListboxSelect>>', on_select)

    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    add_btn = tk.Button(root, text="Add New Game", command=go_to_add)
    change_btn = tk.Button(root, text="Change Game Currently Being Played to Selected", command=lambda:on_change(cur_game.get(), cur_prog.get()))
    remove_btn = tk.Button(root, text="Remove Game selected", command=lambda: (on_remove(cur_game.get()), go_to_journal()))
    label.pack(pady=20)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    frame.pack(padx=10, pady=10)
    add_btn.pack(pady=20)
    remove_btn.pack(pady=20)
    change_btn.pack(pady=20)
    back_btn.pack(pady=20)

#remove game from list
def remove_game(title_to_remove):
    if(title_to_remove != "N/A"):
        print("remove?")
        print(title_to_remove)
        games = read_games("games.csv", 1)
        print(games)
        cur_play = read_games("curPlay.csv", 0)
        updated_games = [g for g in games if g[0] != title_to_remove]
        for g in games:
            print(g[0] + " Game " + title_to_remove)
        new = [["N/A", "N/A"]]
        path = get_csv_path("curPlay.csv")
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in csv_reader:
                print("i[0] " + i[0] + " real? " + title_to_remove)
                if(i[0] == title_to_remove and i[0] != "N/A"):
                    write_games(new, "curPlay.csv", 0)
        if len(updated_games) == len(games):
            print("no game found")
        else:
            write_games(updated_games, "games.csv", 1)
            print("Removed " + title_to_remove)
    else:
        print("cant remove nothing") 


def read_games(game, header):
    ret = []
    print(game)
    g = get_csv_path(game)
    with open(g, 'r') as f:
        csv_reader = csv.reader(f)
        for i in range(0, header):
            next(csv_reader)
        for i in csv_reader:
            ret.append(i)  # Skip header
    print("returning")
    return ret

def write_games(games, CSV_FILE, head):
    g = get_csv_path(CSV_FILE)
    with open(g, "w", newline="") as f:
        writer = csv.writer(f)
        if(head):
            writer.writerow(["title", "platform"])  # write header back
        for i in games:
            print("I is " + i[0] + " " + i[1])
            writer.writerow(i)


#change the game in curPlay.csv to the selected game
def change_play_game(name, progress):
    print("this is being called " + name)
    data = [name, progress]
    csv_path = get_csv_path("curPlay.csv")
    with open(csv_path, 'w', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
    print(data)

def load_add_screen(root, go_to_home):
    label = tk.Label(root, text="Add a game", font=("Arial", 16))
    label2 = tk.Label(root, text="Select Progress", font=("Arial", 16))
    label3 = tk.Label(root, text="Type Game Name", font=("Arial", 16))
    entry = tk.Entry(root, text = "Type Game Name", font = ("Arial", 16))
    #v = StringVar(root, "1")

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
    add_btn = tk.Button(root, text="Add", command=lambda: (on_add(entry.get(), progress_var.get()), go_to_home()))
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

#confirm with the user that they want to remove the game
def on_remove(game):
    result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete " + game + " from the list?")
    if result:
        remove_game(game)
    else:
        print("User canceled deletion.")

#confirm with the user that they want to add the game
def on_add(game, prog):
    result = messagebox.askyesno("Confirm Add", "Are you sure you want to add " + game + " with " + prog + " to the list?")
    if result:
        add_to_list(game, prog)
    else:
        print("User canceled deletion.")

#confirm with the user that they want to Change the game currently being played
def on_change(game, prog):
    result = messagebox.askyesno("Confirm New Game Playing", "Are you sure you want to change your game currently being played to " 
                    + game + " with " + prog)
    if result:
        change_play_game(game, prog)
    else:
        print("User canceled deletion.")