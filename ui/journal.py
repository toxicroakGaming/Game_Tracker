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
    search_label = tk.Label(root, text = "Search", font = ("Arial", 16))
    search_entry = tk.Entry(root, text = "Type Game Name", font = ("Arial", 16))
    search_btn = tk.Button(root, text="Search", command=lambda:(games_holder.update({"games": search_games(search_entry.get())}),
                            clear_screen(root), load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
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
    fav_btn = tk.Button(root, text="Sort By Favorites", command=lambda:(clear_screen(root),
                        games_holder.update({"games": sort_games(5), "sort" : 5}),
                        load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    add_tag_btn = tk.Button(root, text="Add New Tag", command=lambda:(clear_screen(root), add_tag_list(root, go_to_journal) 
                            ))
    rem_tag_btn = tk.Button(root, text="Remove Tag", command=lambda:(clear_screen(root), rem_tag_list(root, go_to_journal) 
                            ))
    label.pack(pady=10)
    search_label.pack(pady=10)
    search_entry.pack(pady=10)
    search_btn.pack(pady=10)
    add_btn.pack(pady=5)
    az_btn.pack(pady=5)
    za_btn.pack(pady=5)
    least_btn.pack(pady=5)
    most_btn.pack(pady=5)
    fav_btn.pack(pady=5)
    utils.state.sel_tags = load_tags(root)
    sort_tag_btn = tk.Button(root, text="Sort by selected tags", command=lambda:(clear_screen(root),
                        games_holder.update({"games": sort_tags([tag for tag, var in utils.state.sel_tags.items() if var.get()], 0), "sort" : 4}),
                        load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    filt_tag_btn = tk.Button(root, text="Filter by selected tags", command=lambda:(clear_screen(root),
                    games_holder.update({"games": sort_tags([tag for tag, var in utils.state.sel_tags.items() if var.get()], 1), "sort" : 4}),
                    load_journal_screen(root, go_to_home, go_to_add, go_to_journal)))
    filt_tag_btn.pack(pady=10)
    sort_tag_btn.pack(pady=10)
    add_tag_btn.pack(pady=10)
    rem_tag_btn.pack(pady=10)
    back_btn.pack(pady=10)

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
        cur_play = read_games("curPlay.csv", 0)
        fav_path = get_csv_path("favorites.csv")
        tag_path = get_csv_path("tag_connect.csv")
        favorites = []
        tags = []
        #removing entry from favorites and tag_connect
        temp = utils.state.game_store
        rem = False
        for i in utils.state.game_store:
            if(i["title"] == title_to_remove):
                temp.remove(i)
                rem = True
        utils.state.game_store = temp
        #write everything with the game removed
        save_games()
        #if the game was currently being played, we need to change it to N/A
        path = get_csv_path("curPlay.csv")
        with open(path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for i in csv_reader:
                if(i[0] == title_to_remove and i[0] != "N/A"):
                    write_games(new, "curPlay.csv", 0)
        if (not rem):
            print("no game found")
        else:
            utils.util.save_games()
            utils.util.load_games()
    else:
        print("cant remove nothing") 
    utils.util.load_games()


def read_games(game, header):
    ret = []
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
    games = []
    for i in utils.state.game_store:
        #Since we can't play two games at once in this, change the 
        #current in progress game to being some progress
        if(i["status"] == "In Progress"):
            i["last"] = current_time()
            i["status"] = "Some progress not completed"

        if(name == i["title"]):
            #update time intervals. this is for an achievement
            if(i["status"] == "Not Started"):
                i["last"] = current_time()
                i["start"] = current_time()
            print("changing something")
            i["status"] = "In Progress"
            check_achieve_play(app_frame)
        games.append(i)
    #write the games to the csv
    save_games()
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
        print(name)
        print("above me is the name")
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
                    if(cur[0] != name):
                        temp = next((entry for entry in utils.state.game_store if entry["title"] == name), None)
                        n = temp["image"]
                        change_play_game(name, progress, n)
                csv_path = get_csv_path("games.csv")
                #read the games into a temporary list so that we can write from it
                temp = []
                print(progress)
                with open(csv_path, 'r', newline = '') as new_file:
                    csv_reader = csv.reader(new_file)
                    print("temp2")
                    for i in csv_reader:
                        temp.append(i)
                    print("contents of temp")
                #write temp to the csv
                with open(csv_path, 'w', newline = '') as new_file:
                    index = 0
                    #to avoid double write
                    doub = False
                    csv_writer = csv.writer(new_file)
                    for i in temp:
                        if(i[1] == "In Progress"):
                            if(name == i[0] and (progress == "Completed" or progress == "100%")):
                                print("this is called to change progress!")
                                check_achieve_cons(app_frame)
                                change_play_game(default_game["title"], default_game["status"], default_game["image"])
                            else:
                                cur_no_game = 0
                            data = [name, progress, i[2], i[3], i[4], i[5], current_time(), i[7]]
                            doub = True
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
                                if(not doub):
                                    csv_writer.writerow(data)
                                doub = False
                        else:
                            #print(i)
                            csv_writer.writerow(temp[index])
                        index += 1
    else:
        print("INVALID!")

def load_add_screen(root, go_to_home):
    image_path = tk.StringVar()
    image_path.set(default_game["image"])
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
        csv_writer.writerow(["N/A"])
        utils.state.game_tags[name] = ["N/A"]
    fav_path = get_csv_path("favorites.csv")
    with open(fav_path, 'a', newline = '') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["False"])
    utils.util.load_games()

#confirm with the user that they want to remove the game
def on_remove(game):
    if(game == default_game["title"]):
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
    #print("sorting...")
    #print(type)
    csv_path = get_csv_path("games.csv")
    sorted_list = []
    if(type == 5):
        print("sorting by favorite")
        fav = []
        not_fav = []
        for i in utils.state.game_store:
            cur = i["favorite"]
            if(cur[0] == "True"):
                fav.append(i)
                print("yes, added")
            else:
                not_fav.append(i)
        #print("adding favorites")
        for i in fav:
            sorted_list.append(i)
        for i in not_fav:
            sorted_list.append(i)
        return sorted_list
    with open(csv_path, 'r', newline = '') as new_file:
        csv_reader = csv.reader(new_file)
        next(csv_reader)
        sorted_list = []
        for i in utils.state.game_store:
            sorted_list.append(i)
        if(type == 0):
            sorted_list = sorted(sorted_list, key=lambda x: x["title"].lower())
        elif(type == 1):
            sorted_list = sorted(sorted_list, key=lambda x: x["title"].lower(), reverse = True)
        elif(type == 2 or type == 3):
            #0 is not started
            #1 is in progress
            #2 is completed
            #3 is 100%
            prog = [[], [], [], [], []]
            for i in sorted_list:
                st = i["status"]
                if(st == "Not Started"):
                    prog[0].append(i)
                if(st == "Some progress not completed"):
                    prog[1].append(i)
                elif(st == "In Progress"):
                    prog[2].append(i)
                elif(st == "Completed"):
                    prog[3].append(i)
                elif(st == "100%"):
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
    print("loading...")
    #for index in the listbox
    prog_ind = tk.IntVar()
    prog_ind.set(-1)
    #get the scrollabale for the game options
    frame = tk.Frame(root)
    if(game_list == None):
        game_list = []
        #Read the CSV file
        for line in utils.state.game_store:
            print(line["title"])
            game_list.append(line)
            if(line["status"] == "Completed" or line["status"] == "100%"):
                utils.state.num_completed += 1
            if(line["image"] == r"ui\media\games\no_image.jpg"):
                no_image = True    
            if(game_list == []):
                print(True)
                game_list.append(default_game)
                print("appended default game")
            else:
                if(sort == None):
                    sort = 0
                if(sort == 4):
                    game_list = sort_tags([], 0)
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
    canvas.bind("<Configure>", lambda e: lazy_load_images(canvas, thumb_size))
    canvas.bind_all("<MouseWheel>", lambda e: lazy_load_images(canvas, thumb_size))

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    thumb_size = (120, 120)
    row = 0
    col = 0
    cur_game = tk.StringVar()
    cur_prog = tk.StringVar()
    cur_link = tk.StringVar()
    cur_desc = tk.StringVar()
    cur_prog.set(default_game["status"])
    cur_game.set(default_game["title"])
    cur_link.set(default_game["image"])
    cur_desc.set(default_game["desc"])
    image_refs = []  # To keep images alive
    ind = 0
    for title, frame in list(utils.state.game_frames.items()):
        if not frame.winfo_exists():
            del utils.state.game_frames[title]
        # Create frame for each game
    for frame in utils.state.game_frames.values():
        frame.grid_forget()
    for index, game in enumerate(game_list):
        title = game["title"]
        platform = game["status"]
        img_path = game["image"]
        img_path = get_resource_path(img_path)

        if(title in utils.state.game_frames):
            if title in utils.state.game_frames and utils.state.game_frames[title].winfo_exists():
                utils.state.game_frames[title].grid(row=row, column=col)
        else:
            game_frame = tk.Frame(scroll_frame, bd=2, relief="groove", background="white")
            game_frame.grid(row=row, column=col, padx=10, pady=10)
            utils.state.game_frames[title] = game_frame
            photo = get_cached_image(img_path, thumb_size)

            # Image label
            img_label = tk.Label(game_frame, image=photo)
            img_label.bind(
                "<Button-1>",
                lambda event, t=title, p=platform, i = img_path, ind = index + 1: on_game_click(t, p, i, go_to_journal, ind, root, cur_game, cur_prog, cur_link)
            )
            img_label.image = photo
            img_label.pack()
            utils.state.widget_image_map[img_label] = img_path
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
        prog_btn = tk.Button(root, text="Change Progress", command=lambda t=name: change_prog_game(t, root, ind, lambda:on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link)))
        desc_label = tk.Label(root, text = "Description:")
        browse_btn = tk.Button(root, text="Change Game image", command=lambda:(on_img_click(name, progress, go_to_journal, ind, root, cur_game, cur_prog, cur_link)))
        add_btn = tk.Button(root, text="Add Tags", command=lambda:(clear_screen(root), add_tag_game(root, cur_game.get(), lambda:on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link))))
        rem_btn = tk.Button(root, text="Remove Tags", command=lambda: (clear_screen(root),remove_tag_game(root, cur_game.get(), lambda: on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link))))
        tag_label = tk.Label(root, text = "Tags:")
        tags = ""
        for i in utils.state.game_store:
            if(i["title"] == name):
                fin = len(i["tags"])
                index = 0
                for tag in i["tags"]:
                    if(index != fin - 1):
                        tags = tags + tag + ", "
                    else:
                        tags = tags + tag
                    index += 1
                fav_btn = tk.Button(root, text="Add To Favorites", command=lambda:(clear_screen(root), add_favorite(name, "True"),
                                    on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link)))
                if(i["favorite"] == ["True"]):
                    fav_btn = tk.Button(root, text="Remove From Favorites", command=lambda:(clear_screen(root), add_favorite(name, "False"),
                                        on_game_click(name, progress, img, go_to_journal, ind, root, cur_game, cur_prog, cur_link)))
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
        fav_btn.pack(pady=10)
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
            for cur in utils.game_store:
                if cur["title"] == name:
                    with open(cur_play_path, 'w', newline='') as f:
                        #print(cur)
                        csv.writer(f).writerow([cur[0], cur[1], new_image])

                # Update games.csv
                game_path = get_csv_path("games.csv")
                updated_games = []
                temp = []
                for row in utils.state.game_store:
                    if row["title"] == name:
                        updated_games.append([row["title"], row["status"], new_image, row["desc"], row["added"], row["start"], row["last"], 
                        row["completed"]])
                        temp = row["image"]
                    else:
                        updated_games.append(row)

                with open(game_path, 'w', newline='') as f:
                    csv.writer(f).writerows(updated_games)
            clear_screen(root)
            on_game_click(name, progress, path.get(), go_to_journal, ind, root, cur_game, cur_prog, cur_link)

def load_tags(root):
    container = tk.Frame(root)
    canvas = tk.Canvas(container, width = 100, height = 100)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    container.pack(fill="both", expand=True)
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Add checkbuttons
    csv_path = get_csv_path("tags.csv")
    tags = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            tags.append(i[0])
    check_vars = {}
    for tag in tags:
        var = tk.BooleanVar()
        chk = tk.Checkbutton(scrollable_frame, text=tag, variable=var)
        chk.pack(anchor="w")
        check_vars[tag] = var  # Save reference for later use
    return check_vars

#sorts by the oder it is in selected_tags. no further sorting of selected_tags is done
def sort_tags(selected_tags, fil):
    print("these are selected")
    #print(selected_tags)
    tags = []
    not_tags = []
    for i in utils.state.game_store:
        added = False
        for cur in selected_tags:
            if(cur in i["tags"]):
                added = True
                tags.append(i)
        if (not fil or selected_tags == []):
            if(not added):
                not_tags.append(i)
    for i in not_tags:
        tags.append(i)
    return tags

def search_games(cur):
    cur = cur.lower()
    games = []
    for i in utils.state.game_store:
        #print(i["title"])
        if(cur in i["title"].lower()):
            games.append(i)
        elif(cur == ''):
            games.append(i)
    return games

def add_favorite(name, fav):
    fav_path = get_csv_path("favorites.csv")
    for i in utils.state.game_store:
        if(i["title"]  == name):
            i["favorite"] = [fav]
    with open(fav_path, 'w', newline = '') as f:
        writer = csv.writer(f)
        for i in utils.state.game_store:
            writer.writerow(i["favorite"])

def lazy_load_images(canvas, thumb_size):
    for widget, path in list(utils.state.widget_image_map.items()):
        if not widget.winfo_exists():
            # remove it from cache if destroyed
            del utils.state.widget_image_map[widget]
            continue
        widget_y = widget.winfo_y()
        visible_top = canvas.canvasy(0)
        visible_bottom = visible_top + canvas.winfo_height()
        if widget_y + widget.winfo_height() >= visible_top and widget_y <= visible_bottom:
            if not getattr(widget, "loaded", False):
                photo = get_cached_image(path, thumb_size)
                widget.configure(image=photo)
                widget.image = photo
                widget.loaded = True