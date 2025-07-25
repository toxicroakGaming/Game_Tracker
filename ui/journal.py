import tkinter as tk
import csv
import os, sys
from tkinter import *
from utils.util import *
import utils.Date
from utils.achieve import *
import utils.state
from utils.tag import *
#GAMES.CSV HEADER
# ["title", "platform", "image", "desc", "added", "start", "last", completed]
#The main work of the "collections" screen
app_frame = None
def load_journal_screen(root, go_to_home, go_to_add, go_to_journal):
    #collections label
    label = tk.Label(root, text = "Collection", font = ("Arial", 16))
    #get the games from the CSV. Make a list with every game and the status
    load_collection(root, go_to_journal, games_holder["sort"], games_holder["games"])
    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    add_btn = tk.Button(root, text="Add New Game", command=go_to_add)
    az_btn = tk.Button(root, text="Sort By Name (A-Z)", command=lambda:(clear_screen(root),
                            games_holder.update({"games": sort_games(0), "sort" : 0}),
                            load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    za_btn = tk.Button(root, text="Sort By Name (Z-A)", command=lambda:(        clear_screen(root),
                            games_holder.update({"games": sort_games(1), "sort" : 1}),
                            load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    least_btn = tk.Button(root, text="Sort By Progress (least-most)", command=lambda:(clear_screen(root),
                            games_holder.update({"games": sort_games(2), "sort" : 2}),
                            load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    most_btn = tk.Button(root, text="Sort By Progress (most - least)", command=lambda:(clear_screen(root),
                            games_holder.update({"games": sort_games(3), "sort" : 3}),
                            load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    add_tag_btn = tk.Button(root, text="Add New Tag", command=lambda:(clear_screen(root), add_tag_list(root, go_to_journal) 
                            ))
    rem_tag_btn = tk.Button(root, text="Remove Tag", command=lambda:(clear_screen(root), rem_tag_list(root, go_to_journal) 
                            ))
    label.pack(pady=20)
    add_btn.pack(pady=20)
    az_btn.pack(pady=20)
    za_btn.pack(pady=20)
    least_btn.pack(pady=20)
    most_btn.pack(pady=20)
    add_tag_btn.pack(pady=20)
    rem_tag_btn.pack(pady=20)
    back_btn.pack(pady=20)

def get_game_index(event):
    selection = event.widget.curselection()
    if selection:
        index = selection[0]
        return index

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
        new = [default_game]
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
            #these are the columns we want to have in our games.csv.
            writer.writerow(["title", "platform", "image", "desc", "added", "start", "last", "completed"])  # write header back
        for i in games:
            print("I is " + i[0] + " " + i[1])
            writer.writerow(i)


#change the game in curPlay.csv to the selected game
def change_play_game(name, progress, image):
    global app_frame
    print("this is being called 1234 " + name)
    print(progress)
    data = [name, progress, image]
    csv_path = get_csv_path("curPlay.csv")
    with open(csv_path, 'w', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
    csv_path = get_csv_path("games.csv")
    games = []
    with open(csv_path, 'r', newline = '') as f:
        csv_reader = csv.reader(f)
        for i in csv_reader:
            if(i[1] == "In Progress"):
                i[6] = current_time()
                i[1] = "Some progress not completed"
            if(name == i[0]):
                if(i[1] == "Not Started"):
                    i[6] = current_time()
                    i[5] = current_time()
                print("changing something")
                i[1] = "In Progress"
                check_achieve_play(app_frame)
            print(i)
            games.append(i)
    with open(csv_path, 'w', newline = '') as new_write:
        csv_writer = csv.writer(new_write)
        for i in games:
            print("NEW")
            print(i)
            csv_writer.writerow(i)
    print(data)

def change_prog_game(name, root, ind, go_to_journal):
    print(ind)
    print("above is the index")
    if(ind != -1):
        clear_screen(root)
        temp = []
        game_name = tk.Label(root, text = "Game changing: " + name)
        game_name.pack(pady = 20)
        progress_var = add_options(root)
        change_btn = tk.Button(root, text="Change Progress", command=lambda:(on_click(name, progress_var.get())))
        back_btn = tk.Button(root, text="Back to Home", command=go_to_journal)
        change_btn.pack(pady=20)
        back_btn.pack(pady=20)
        print("we made it!")
        def on_click(name, progress):
            global app_frame
            data = [name, progress]
            print("yes")
            if(prog_change(name, progress_var)):
                csv_path = get_csv_path("curPlay.csv")
                with open(csv_path, 'r', newline = '') as new_file:
                    csv_reader = csv.reader(new_file)
                    cur = next(csv_reader)
                    if(cur[0] == name):
                        change_play_game(name, progress, cur[2])
                csv_path = get_csv_path("games.csv")
                #read the games into a temporary list so that we can write from it
                temp = []
                with open(csv_path, 'r', newline = '') as new_file:
                    csv_reader = csv.reader(new_file)
                    print("temp")
                    for i in csv_reader:
                        temp.append(i)
                        print(i)
                    print("contents of temp")
                    print(temp)
                #write temp to the csv
                with open(csv_path, 'w', newline = '') as new_file:
                    index = 0
                    csv_writer = csv.writer(new_file)
                    for i in temp:
                        if(i[1] == "In Progress"):
                            if(name == i[0] and progress == "Completed"):
                                check_achieve_cons(app_frame)
                            else:
                                cur_no_game = 0
                            print(i)
                            data = [name, progress, i[2], i[3], i[4], i[5], current_time(), i[7]]
                            csv_writer.writerow(data)
                        if(name == i[0]):
                            print("temp")
                            print(name)
                            print(progress)
                            print(i[2])
                            print(i[3])
                            if(i[1] != "Completed" and progress == "Completed"):
                                check_achieve_time(name, root)
                                data = [name, progress, i[2], i[3], i[4], current_time(), current_time(), current_time()]
                            else:
                                if(i[1] == "Not Started"):
                                    data = [name, progress, i[2], i[3], i[4], current_time(), current_time(), i[7]]
                                else:
                                    data = [name, progress, i[2], i[3], i[4], i[5], current_time(), i[7]]
                                csv_writer.writerow(data)
                        else:
                            print(i)
                            csv_writer.writerow(temp[index])
                        index += 1
    else:
        print("INVALID!")

def load_add_screen(root, go_to_home):
    image_path = tk.StringVar()
    image_path.set(default_game[2])
    label = tk.Label(root, text="Add a game", font=("Arial", 16))
    label2 = tk.Label(root, text="Select Progress", font=("Arial", 16))
    label3 = tk.Label(root, text="Type Game Name", font=("Arial", 16))
    image_label = tk.Label(root, text="No image selected")
    entry = tk.Entry(root, text = "Type Game Name", font = ("Arial", 16))
    browse_btn = tk.Button(root, text="Browse Image", command=lambda:(browse_image(image_path, image_label)))

    # Loop is used to create multiple Radiobuttons
    # rather than creating each button separately
    choice = tk.StringVar()
    label.pack(pady=20)
    label2.pack()
    #set the progress values
    progress_var = add_options(root)
    back_btn = tk.Button(root, text="Back", command=go_to_home)
    add_btn = tk.Button(root, text="Add", command=lambda: (on_add(entry.get(), progress_var.get(), image_path.get()), go_to_home()))
    label3.pack(pady=20)
    entry.pack()
    image_label.pack(pady=5)
    browse_btn.pack(pady=5)
    back_btn.pack(pady=20)
    add_btn.pack(pady = 20)


#For adding progress options. Used in multiple places. Could also maybe update to pass in values as
#a parameter in the future
def add_options(root):
    progress_var = StringVar(root)
    progress_var.set("Not Started")
    values = ["Not Started", "In Progress", "Some progress not completed", "Completed", "100%"]
    for text in values:
        Radiobutton(root, text = text, variable = progress_var, value = text, indicator = 0, 
        background = "light blue").pack(fill=X, ipady=5)
    return progress_var

#Update the CSV with the new game, which is the name and the progress
def add_to_list(name, progress, image):
    global app_frame
    desc_file = "ui/desc/" + name + ".txt"
    if(progress != "Not Started"):
        if(progress == "Completed" or progress == "100%"):
            data = [name, progress, image, desc_file, current_time(), current_time(), current_time(), current_time()]
        else:
            data = [name, progress, image, desc_file, current_time(), current_time(), current_time(), "N/A"]
    else:
        data = [name, progress, image, desc_file, current_time(), "N/A", "N/A", "N/A"]
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'a', newline = '') as new_file:
        csv_writer = csv.writer(new_file)
        csv_writer.writerow(data)
    tag_path = get_csv_path("tag_connect.csv")
    with open(tag_path, 'a', newline = '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow("N/A")
        utils.state.game_tags[name] = ["N/A"]

#confirm with the user that they want to remove the game
def on_remove(game):
    if(game == default_game[0]):
        messagebox.askyesno("Can't delete N/A", "Can't delete N/A")
        return
    result = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete " + game + " from the list?")
    if result:
        delete_description(game)
        remove_game(game)
    else:
        print("User canceled deletion.")

#confirm with the user that they want to add the game
def on_add(game, prog, image):
    result = messagebox.askyesno("Confirm Add", "Are you sure you want to add " + game + " with " + prog + " to the list?")
    if result:
        create_description(game)
        add_to_list(game, prog, image)
    else:
        print("User canceled deletion.")

#confirm with the user that they want to Change the game currently being played
def game_change(game, prog, image):
    result = messagebox.askyesno("Confirm New Game Playing", "Are you sure you want to change your game currently being played to " 
                    + game + " with " + prog)
    if result:
        change_play_game(game, prog, image)
    else:
        print("User canceled deletion.")

#confirm with the user that they want to Change the game currently being played
def prog_change(game, prog):
    if(game == "N/A"):
        result = messagebox.askyesno("Invalid", "Can't change progress due to N/A state")
        return False
    result = messagebox.askyesno("Confirm New Game Progress", "Are you sure you want to change  " 
                    + game + " progress to " + prog.get() + "?")
    if result:
        return True
    else:
        print("User canceled deletion.")
        return False

'''type is what sort we are doing
0 A-Z
1 Z-A
2 progress (least-most)
3 progress (most-least)
'''
def sort_games(type):
    csv_path = get_csv_path("games.csv")
    with open(csv_path, 'r', newline = '') as new_file:
        csv_reader = csv.reader(new_file)
        next(csv_reader)
        sorted_list = []
        for i in csv_reader:
            sorted_list.append(i)
        if(type == 0):
            sorted_list = sorted(sorted_list, key=lambda x: x[0])
        elif(type == 1):
            sorted_list = sorted(sorted_list, key=lambda x: x[0], reverse = True)
        elif(type == 2 or type == 3):
            #0 is not started
            #1 is in progress
            #2 is completed
            #3 is 100%
            prog = [[], [], [], [], []]
            for i in sorted_list:
                if(i[1] == "Not Started"):
                    prog[0].append(i)
                if(i[1] == "Some progress not completed"):
                    prog[1].append(i)
                elif(i[1] == "In Progress"):
                    prog[2].append(i)
                elif(i[1] == "Completed"):
                    prog[3].append(i)
                elif(i[1] == "100%"):
                    prog[4].append(i)
            sorted_list = []
            if(type == 2):
                for ind in range(0,4):
                    if(prog[ind] != []):
                        for n in prog[ind]:
                            sorted_list.append(n)
            elif(type == 3):
                for ind in range(3, -1, -1):
                    if(prog[ind] != []):
                        for n in prog[ind]:
                            sorted_list.append(n)
        return sorted_list
    return None

def load_collection(root, go_to_journal, sort, game_list = None):
    utils.state.num_completed = 0
    no_image = False
    print(game_list)
    print("loading...")
    #for index in the listbox
    prog_ind = tk.IntVar()
    prog_ind.set(-1)
    #get the scrollabale for the game options
    frame = tk.Frame(root)
    if(game_list == None):
        game_list = []
        #Read the CSV file
        csv_path = get_csv_path("games.csv")
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                #print(line)
                game_list.append(line)
                if(line[1] == "Completed" or line[1] == "100%"):
                    print("completed game here")
                    utils.state.num_completed += 1
                if(line[2] == r"ui\media\games\no_image.jpg"):
                    no_image = True
            if(game_list == []):
                print(True)
                game_list.append(default_game)
                print("appended default game")
            else:
                if(sort == None):
                    sort = 0
                game_list = sort_games(sort)
    #scrollbox
    # Create canvas with scrollbar
    container = tk.Frame(root)
    container.pack(side = "left", fill="both", expand=True)
    canvas = tk.Canvas(container, borderwidth=0, background="#f0f0f0")
    frame = tk.Frame(canvas, background="#f0f0f0")
    vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    if(no_image):
        check_achieve_image(app_frame)
    print("here we go")
    print(utils.state.num_completed)
    check_achieve_complete(app_frame)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    scroll_frame = tk.Frame(canvas, background="#f0f0f0")
    canvas_window = canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)

    frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", resize_canvas)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    scroll_frame.bind("<Configure>", on_frame_configure)
    canvas.bind("<Configure>", resize_canvas)
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    thumb_size = (120, 120)
    row = 0
    col = 0
    cur_game = tk.StringVar()
    cur_prog = tk.StringVar()
    cur_link = tk.StringVar()
    cur_desc = tk.StringVar()
    cur_prog.set(default_game[0])
    cur_game.set(default_game[1])
    cur_link.set(default_game[2])
    cur_desc.set(default_game[3])
    image_refs = []  # To keep images alive
    ind = 0
    for index, game in enumerate(game_list):
        title = game[0]
        platform = game[1]
        img_path = game[2]
        img_path = get_resource_path(img_path)

        # Create frame for each game
        game_frame = tk.Frame(scroll_frame, bd=2, relief="groove", background="white")
        game_frame.grid(row=row, column=col, padx=10, pady=10)

        # Load image
        if os.path.exists(img_path):
            img = Image.open(img_path)
        else:
            img = Image.new("RGB", thumb_size, color="gray")
        img.thumbnail(thumb_size)
        photo = ImageTk.PhotoImage(img)
        image_refs.append(photo)

        # Image label
        img_label = tk.Label(game_frame, image=photo)
        img_label.bind(
            "<Button-1>",
            lambda event, t=title, p=platform, i = img_path, ind = index + 1: on_game_click(t, p, i, go_to_journal, ind, root, cur_game, cur_prog, cur_link)
        )
        img_label.image = photo
        img_label.pack()


        # Text label
        text = f"{title}\n({platform})"
        text_label = tk.Label(game_frame, text=text, wraplength=120, justify="center")
        text_label.pack()
        # Arrange in grid
        col += 1
        if col >= 5:
            col = 0
            row += 1
        ind += 1
        frame.pack(padx=10, pady=10)

    def on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link):
        print("[DEBUG] on_game_click() img =", img)
        clear_screen(root)
        thumb_size = (120, 120)
        cur_game.set(name)
        cur_prog.set(progress)
        cur_link.set(img)
        title_label = tk.Label(root, text = name)
        title_label.pack(pady = 10)
        new_img = Image.new("RGB", thumb_size, color="gray")
        if os.path.exists(img):
            new_img = Image.open(img)
        else:
            new_img = Image.new("RGB", thumb_size, color="gray")
        new_img.thumbnail(thumb_size)
        photo = ImageTk.PhotoImage(new_img)
        image_refs.append(photo)
        img_label = tk.Label(root, image=photo)
        img_label.image = photo
        img_label.pack()
        back_btn = tk.Button(root, text="Back to Collection", command=go_to_journal)
        remove_btn = tk.Button(root, text="Remove Game", command=lambda: (on_remove(cur_game.get()), go_to_journal()))
        change_btn = tk.Button(root, text="Change Game Currently Being Played to this", command=lambda:(game_change(cur_game.get(), "In Progress", cur_link.get())))
        prog_btn = tk.Button(root, text="Change Progress", command=lambda t=name: change_prog_game(t, root, ind, go_to_journal))
        desc_label = tk.Label(root, text = "Description:")
        browse_btn = tk.Button(root, text="Change Game image", command=lambda:(on_img_click(name, progress, go_to_journal, ind, root, cur_game, cur_prog, cur_link)))
        add_btn = tk.Button(root, text="Add Tags", command=lambda:(clear_screen(root), add_tag_game(root, cur_game.get(), go_to_journal)))
        rem_btn = tk.Button(root, text="Remove Tags", command=lambda:(clear_screen(root), remove_tag_game(root, cur_game.get(), go_to_journal)))
        file = get_csv_path("tag_connect.csv")
        tag_label = tk.Label(root, text = "Tags:")
        tags = ""
        t = get_csv_path("games.csv")
        with open(file, 'r') as f:
            with open(t, 'r') as h:
                read_tag = csv.reader(f)
                read_game = csv.reader(h)
                for i in read_game:
                    cur = next(read_tag)
                    if(i[0] == name):
                        for tag in cur[0]:
                            tags = tags + tag + " "
        desc_text_label = tk.Label(root)
        tags_label = tk.Label(root, text = tags)
        if(name != "N/A"):
            desc_path = os.path.join(get_user_data_dir(), "desc", f"{sanitize_filename(name)}.txt")
            desc_btn = tk.Button(root, text="Edit Description", command=lambda:(edit_text_file(root,desc_path, 
                        lambda:on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link))))
            desc_text = ""
            with open(desc_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    desc_text += line.strip()  # strip() removes trailing newline
            desc_text_label.config(text = desc_text)
            desc_label.pack(pady = 10)
            desc_text_label.pack(pady = 10)
            desc_btn.pack(pady = 10)
            add_btn.pack(pady = 10)
            rem_btn.pack(pady = 10)
            browse_btn.pack(pady = 10)
            prog_btn.pack(pady = 10)
        if(name != "N/A"):    
            change_btn.pack(pady=10)
            remove_btn.pack(pady=10)
        tag_label.pack()
        tags_label.pack()
        back_btn.pack(side="left", padx=20)

        def on_img_click(name, progress, go_to_journal, ind, root, cur_game, cur_prog, cur_link):
            global app_frame
            clear_screen(root)
            path = tk.StringVar()
            temp_label = tk.Label(root)
            browse_image(path, temp_label)
            new_image = path.get()
            print("[DEBUG] New image path selected:", new_image)
            game_path = get_csv_path("games.csv")
            cur_play_path = get_csv_path("curPlay.csv")
            games = []
            with open(cur_play_path, 'r', newline='') as f:
                cur = next(csv.reader(f))
                if cur[0] == name:
                    with open(cur_play_path, 'w', newline='') as f:
                        #print(cur)
                        csv.writer(f).writerow([cur[0], cur[1], new_image])

                # Update games.csv
                game_path = get_csv_path("games.csv")
                updated_games = []
                temp = []
                with open(game_path, 'r', newline='') as f:
                    for row in csv.reader(f):
                        if row[0] == name:
                            updated_games.append([row[0], row[1], new_image, row[3], row[4], row[5], row[6], row[7]])
                            temp = row[2]
                        else:
                            updated_games.append(row)

                with open(game_path, 'w', newline='') as f:
                    csv.writer(f).writerows(updated_games)
            clear_screen(root)
            on_game_click(name, progress, path.get(), go_to_journal, ind, root, cur_game, cur_prog, cur_link)
