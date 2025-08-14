import utils.state
import utils.util
import tkinter as tk
import csv
import os, sys
from tkinter import messagebox, Radiobutton
#from tkinter import *
#this file will handle thing related to tags
def load_tags():
    games = utils.util.get_csv_path("games.csv")
    with open(games, 'r') as g:
        reader = csv.reader(g)
        #if tag_connect does not exist...
        if(utils.util.ensure_csv_exists("tag_connect.csv")):
            tc = utils.util.get_csv_path("tag_connect.csv")
            with open(tc, 'w', newline = '') as ta:
                writer = csv.writer(ta)
                for i in reader:
                    writer.writerow(["N/A"])
        else:
            tc = utils.util.get_csv_path("tag_connect.csv")
            with open(tc, 'r') as ta, open(games, 'r') as ga:
                tag_reader = csv.reader(ta)
                reader = csv.reader(ga)
                for cur, i in zip(reader, tag_reader):
                    #put the tags associated with the game into the dict
                    utils.state.game_tags[i[0]] = cur
    t = utils.util.get_csv_path("tags.csv")
    with open(t, 'r') as tag:
        tag_reader = csv.reader(tag)
        #load tags we have
        for i in tag_reader:
            utils.state.tags.append(i[0])

#adds tags PER GAME. The naming might get confusing here
def add_tag_game(root, name, go_to_journal):
    container = tk.Frame(root)
    container.pack(side = "left", fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, background="#f0f0f0")
    frame = tk.Frame(canvas, background="#f0f0f0")
    vsb = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    csv_file = utils.util.get_csv_path("tags.csv")
    add_tag = tk.StringVar()
    values = []
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            values.append(i[0])
    for text in values:
        Radiobutton(canvas, text = text, variable = add_tag, value = text, indicator = 0, 
        background = "light blue").pack(fill='x', ipady=5)
    add_btn = tk.Button(canvas, text="Add selected", command=lambda:(tag_change(add_tag.get(), name, 1)))
    back_btn = tk.Button(canvas, text="Back to Collection", command=go_to_journal)
    add_btn.pack(pady=10)
    back_btn.pack(pady=10)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#remove tags PER GAME
def remove_tag_game(root, name, go_to_journal):
    container = tk.Frame(root)
    container.pack(side = "left", fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, background="#f0f0f0")
    frame = tk.Frame(canvas, background="#f0f0f0")
    vsb = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    csv_file = utils.util.get_csv_path("tag_connect.csv")
    games = utils.util.get_csv_path("games.csv")
    rem_tag = tk.StringVar()
    values = []
    for i in utils.state.game_store:
        if(name == i["title"]):
            for o in i["tags"]:
                values.append(o)
    for text in values:
        Radiobutton(canvas, text = text, variable = rem_tag, value = text, indicator = 0, 
        background = "light blue").pack(fill='x', ipady=5)
    rem_btn = tk.Button(canvas, text="remove selected", command=lambda:(tag_rem(rem_tag.get(), name, 1)))
    back_btn = tk.Button(canvas, text="Back to Collection", command=go_to_journal)
    rem_btn.pack(pady=10)
    back_btn.pack(pady=10)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#this is to make the messagebox appear and continue action if needed
def tag_change(tag, name, t):
    if(tag == None or tag == ""):
        result = messagebox.askyesno("Invalid", "Can't add tag due to N/A state")
        return False
    result = messagebox.askyesno("Confirm New Tag", "Are you sure you want to add tag " + tag + " ?")
    if result:
        #by game
        if(t == 1):
            write_list(tag, name)
        #whole program
        else:
            write_list_add(tag)
        return True
    else:
        print("User canceled deletion.")
        return False

#remove tag from a game
def tag_rem(tag, name, t):
    if(tag == None or tag == "N/A"):
        result = messagebox.askyesno("Invalid", "Can't remove tag due to N/A state")
        return False
    result = messagebox.askyesno("Confirm New Tag", "Are you sure you want to remove tag " + tag + " ?")
    if result:
        #remove from specific game
        if(t == 1):
            write_rem(tag, name)
        #ifw e are removing from the entire program
        else:
            write_rem_list(tag)
        return True
    else:
        print("User canceled deletion.")
        return False

#write the new tag_connect file without the tags
def write_rem(tag, name):
    csv_file = utils.util.get_csv_path("tag_connect.csv")
    games = utils.util.get_csv_path("games.csv")
    tags = []
    temp = next((entry for entry in utils.state.game_store if entry["title"] == name), None)
    if(tag in temp["tags"]):
        temp["tags"].remove(tag)
        if(temp["tags"] == []):
            temp["tags"] = ["N/A"]
    utils.util.save_games()
    load_tags()

#write the list of tags per game
def write_list(tag, name):
    csv_file = utils.util.get_csv_path("tag_connect.csv")
    games = utils.util.get_csv_path("games.csv")
    tags = []
    temp = next((entry for entry in utils.state.game_store if entry["title"] == name), None)
    if(not tag in temp["tags"]):
        if(temp["tags"] == ['N/A']):
            temp["tags"] = [tag]
        else:
            temp["tags"].append(tag)
        utils.util.save_games()
        load_tags()

#add a tag to the overall program list
def add_tag_list(root, go_to_journal):
    container = tk.Frame(root)
    container.pack(side = "left", fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, background="#f0f0f0")
    frame = tk.Frame(canvas, background="#f0f0f0")
    entry = tk.Entry(root, text = "Type Game Name", font = ("Arial", 16))
    add_btn = tk.Button(canvas, text="Add entry", command=lambda:(tag_change(entry.get(), None, 0)))
    back_btn = tk.Button(canvas, text="Back to Collection", command=go_to_journal)
    entry.pack(pady = 10)
    add_btn.pack(pady=10)
    back_btn.pack(pady=10)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#remove a tag from the overall program list
def rem_tag_list(root, go_to_journal):
    container = tk.Frame(root)
    container.pack(side = "left", fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, background="#f0f0f0")
    frame = tk.Frame(canvas, background="#f0f0f0")
    vsb = tk.Scrollbar(canvas, orient="vertical", command=canvas.yview)
    csv_file = utils.util.get_csv_path("tags.csv")
    rem_tag = tk.StringVar()
    values = []
    with open(csv_file, 'r') as f:
        tag_read = csv.reader(f)
        for i in tag_read:
            values.append(i[0])
    for text in values:
        Radiobutton(canvas, text = text, variable = rem_tag, value = text, indicator = 0, 
        background = "light blue").pack(fill='x', ipady=5)
    rem_btn = tk.Button(canvas, text="remove selected", command=lambda:(tag_rem(rem_tag.get(), None, 0), go_to_journal))
    back_btn = tk.Button(canvas, text="Back to Collection", command=go_to_journal)
    rem_btn.pack(pady=10)
    back_btn.pack(pady=10)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

#write with the tag removed from the overall program list.
#this includes any games in tag_connect that had the tag
def write_rem_list(tag):
    file = utils.util.get_csv_path("tags.csv")
    tags = []
    with open(file, 'r') as g:
        r = csv.reader(g)
        for i in r:
            if(i != [tag]):
                tags.append(i)
    with open(file, 'w', newline = '') as f:
        w = csv.writer(f)
        for i in tags:
            w.writerow(i)
    tags = []
    for i in utils.state.game_store:
        for o in i["tags"]:
            if tag in o:
                i["tags"] = [x for x in i["tags"] if x != tag]
            tags.append(i["tags"])
    save_games()

#add to whole program
def write_list_add(tag):
    file = utils.util.get_csv_path("tags.csv")
    tags = []
    with open(file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            tags.append(row)
    with open(file, 'w', newline = '') as f:
        w = csv.writer(f)
        for i in tags:
            w.writerow(i)
        w.writerow([tag])