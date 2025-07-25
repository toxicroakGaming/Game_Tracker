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
    with open(csv_file, 'r') as f:
        with open(games, 'r') as g:
            tag_read = csv.reader(f)
            game_read = csv.reader(g)
            for i in game_read:
                cur = next(tag_read)
                if(name == i[0]):
                    for t in cur:
                        values.append(t)
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


def tag_change(tag, name, t):
    if(tag == None or tag == ""):
        result = messagebox.askyesno("Invalid", "Can't add tag due to N/A state")
        return False
    result = messagebox.askyesno("Confirm New Tag", "Are you sure you want to add tag " + tag + " ?")
    if result:
        if(t == 1):
            write_list(tag, name)
        else:
            write_list_add(tag)
        return True
    else:
        print("User canceled deletion.")
        return False

def tag_rem(tag, name, t):
    if(tag == None or tag == "N/A"):
        result = messagebox.askyesno("Invalid", "Can't remove tag due to N/A state")
        return False
    result = messagebox.askyesno("Confirm New Tag", "Are you sure you want to remove tag " + tag + " ?")
    if result:
        if(t == 1):
            write_rem(tag, name)
        else:
            write_rem_list(tag)
        return True
    else:
        print("User canceled deletion.")
        return False

def write_rem(tag, name):
    csv_file = utils.util.get_csv_path("tag_connect.csv")
    games = utils.util.get_csv_path("games.csv")
    tags = []
    with open(games, 'r') as f:
        with open(csv_file, 'r') as h:
            read_tag = csv.reader(h)
            reader = csv.reader(f)
            for i in reader:
                temp = next(read_tag)
                if(name != i[0]):
                    tags.append(temp)
                else:
                    if(tag not in temp):
                        tags.append(temp)
                        print("tag does not exist!")
                    else:
                        temp.remove(tag)
                        if(temp == []):
                            temp.append("N/A")
                        tags.append(temp)
            with open(csv_file, 'w', newline = '') as g:
                writer = csv.writer(g)
                writer.writerows(tags)
                load_tags()


def write_list(tag, name):
    csv_file = utils.util.get_csv_path("tag_connect.csv")
    games = utils.util.get_csv_path("games.csv")
    tags = []
    with open(csv_file, 'r', newline = '') as g:
        with open(games, 'r') as f:
            writer = csv.reader(g)
            reader = csv.reader(f)
            for i in reader:
                temp = next(writer)
                if(name != i[0]):
                    tags.append(temp)
                else:
                    if(tag in temp):
                        tags.append(temp)
                        print("tag already exists!")
                    else:
                        if(temp == ["N/A"]):
                            temp = [tag]
                            tags.append(temp)
                        else:   
                            temp.append(tag)
                            tags.append(temp)
            with open(csv_file, 'w', newline = '') as new_file:
                writer = csv.writer(new_file)
                writer.writerows(tags)
                load_tags()

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
    rem_btn = tk.Button(canvas, text="remove selected", command=lambda:(tag_rem(rem_tag.get(), None, 0)))
    back_btn = tk.Button(canvas, text="Back to Collection", command=go_to_journal)
    rem_btn.pack(pady=10)
    back_btn.pack(pady=10)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

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
    file = utils.util.get_csv_path("tag_connect.csv")
    tags = []
    with open(file, 'r', newline='') as g:
        r = csv.reader(g)
        for i in r:
            if tag in i:
                i = [x for x in i if x != tag]
            tags.append(i)
        with open(file, 'w', newline = '') as f:
            w = csv.writer(f)
            w.writerows(tags)

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