import tkinter as tk
import csv
import os, sys
from tkinter import *
import tkinter.font as tkfont
from utils.util import *
from utils.Date import *
import utils.state
'''
There will be a csv file once again for tracking achievment progress.
These are all the achievements that are available:
Played X amount of games
Completed X amount of games
Writing jounral entries
added X amount of games
Spin the wheel X amount of times
use the wheel X amount of times without picking a game
Complete X games in a row without starting a new one
Complete a game within X days of starting it
Change currently playing game X times in a day
Add a game with no image

The CSV will store variables related to each achievment. The CSV will be
loaded into a list and only be updated when it needs to be

'''


#this function is kinda long, but the idea is that we want to load the variables from the CSV
#we could make the CSV longer, but I chose to make it shorter since values can be inferred
def load_achieve():
    csv_file = utils.util.get_csv_path("achieve.csv")
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        '''achieve.csv stores 11 things:
        #games played
        #completed
        #entries write
        #times spin wheel
        max #have we spun the wheel x times without picking a game?
        also cur
        max#games completed without starting new in between
        cur times too
        3 for timeframes
        5 for times changed in a day
        1 for image
        '''
        ind = 0
        for i in f:
            #played (0 - 3)
            if ind == 0:
                utils.state.num_played = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[0] = 1
                    if(int(i[0]) >= 10):
                        utils.state.achievements[1] = 1
                        if(int(i[0]) >= 50):
                            utils.state.achievements[2] = 1
                            if(int(i[0]) >= 100):
                                utils.state.achievements[3] = 1
            #completed (4 - 7)
            if ind == 1:
                print("game completed")
                utils.state.num_completed = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[4] = 1
                    if(int(i[0]) >= 10):
                        utils.state.achievements[5] = 1
                        if(int(i[0]) >= 50):
                            utils.state.achievements[6] = 1
                            if(int(i[0]) >= 100):
                                utils.state.achievements[7] = 1
            #entries written (8 - 12)
            if ind == 2:
                utils.state.num_written = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[8] = 1
                    if(int(i[0]) >= 10):
                        utils.state.achievements[9] = 1
                        if(int(i[0]) >= 20):
                            utils.state.utils.state.achievements[10] = 1
                            if(int(i[0]) >= 50):
                                utils.state.achievements[11] = 1
                                if(int(i[0]) >= 100):
                                    utils.state.achievements[12] = 1
            #spins done (13 - 17)
            if ind == 3:
                utils.state.num_spin = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[13] = 1
                    if(int(i[0]) >= 10):
                        utils.state.achievements[14] = 1
                        if(int(i[0]) >= 50):
                            utils.state.achievements[15] = 1
                            if(int(i[0]) >= 100):
                                utils.state.achievements[16] = 1
                                if(int(i[0]) >= 1000):
                                    utils.state.achievements[17] = 1
            #Spins without starting new game (18-23)
            if ind == 4:
                utils.state.max_no_game = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[18] = 1
                    if(int(i[0]) >= 5):
                        utils.state.achievements[19] = 1
                        if(int(i[0]) >= 10):
                            utils.state.achievements[20] = 1
                            if(int(i[0]) >= 20):
                                utils.state.achievements[21] = 1
                                if(int(i[0]) >= 50):
                                    utils.state.achievements[22] = 1
                                    if(int(i[0]) >= 100):
                                        utils.state.achievements[23] = 1
            if ind == 5:
                utils.state.cur_no_game = int(i[0])
            #without playing in between (24 - 27)
            if ind == 6:
                utils.state.max_no_choose = int(i[0])
                if(int(i[0]) >= 1):
                    utils.state.achievements[24] = 1
                    if(int(i[0]) >= 10):
                        utils.state.achievements[25] = 1
                        if(int(i[0]) >= 20):
                            utils.state.achievements[26] = 1
                            if(int(i[0]) >= 50):
                                utils.state.achievements[27] = 1
            if ind == 7:
                utils.state.cur_no_choose = int(i[0])
            #dates (28-30)
            if ind == 8:
                utils.state.achievements[28] = int(i[0])
            if ind == 9:
                utils.state.achievements[29] = int(i[0])
            if ind ==10:
                utils.state.achievements[30] = int(i[0])
            #times changed in day(31 - 35)
            if ind == 11:
                utils.state.achievements[31] = int(i[0])
            if ind == 12:
                utils.state.achievements[32] = int(i[0])
            if ind ==13:
                utils.state.achievements[33] = int(i[0])
            if ind == 14:
                utils.state.achievements[34] = int(i[0])
            if ind == 15:
                utils.state.achievements[35] = int(i[0])
            #incognito achievement
            if ind == 16:
                utils.state.achievements[36] = int(i[0])
            ind += 1   
        print("loaded achievments!")

#these functions will be chunky, but the idea is that they will update achievements and the csv as needed
#this function updates if the number of times we have chosen a game as "in progress" changes
def check_achieve_play(frame):
    utils.state.num_played += 1
    if(utils.state.num_played >= 1 and utils.state.achievements[0] == 0):
        utils.state.achievements[0] = 1
        overlay_notification(frame, "Newbie achievement achieved! Played 1 game")
    if(utils.state.num_played >= 10 and utils.state.achievements[1] == 0):
        utils.state.achievements[1] = 1
        overlay_notification(frame, "Getting the hang of it achievement achieved! Played 10 games")
    if(utils.state.num_played >= 50 and utils.state.achievements[2] == 0):
        utils.state.achievements[2] = 1
        overlay_notification(frame, "The regular achievement achieved! Played 50 games")
    if(utils.state.num_played >= 100 and utils.state.achievements[3] == 0):
        utils.state.achievements[3] = 1
        overlay_notification(frame, "Professional achievement achieved! Played 100 games")
    write_achieve()
    
#this updates when the number of games completed changes
def check_achieve_complete(frame):
    print("completed")
    print(utils.state.num_completed)
    print(utils.state.achievements)
    if(utils.state.num_completed >= 1 and utils.state.achievements[4] == 0):
        utils.state.achievements[4] = 1
        overlay_notification(frame, "First game! achievement achieved! Completed 1 game")
    if(utils.state.num_completed >= 10 and utils.state.achievements[5] == 0):
        utils.state.achievements[5] = 1
        overlay_notification(frame, "Seasoned gamer achievement achieved! Completed 10 games")
    if(utils.state.num_completed >= 50 and utils.state.achievements[6] == 0):
        utils.state.achievements[6] = 1
        overlay_notification(frame, "Completionist achievement achieved! Completed 50 games")
    if(utils.state.num_completed >= 100 and utils.state.achievements[7] == 0):
        utils.state.achievements[7] = 1
        overlay_notification(frame, "Completionist ++ achievement achieved! Completed 100 games")
    write_achieve()

#this updates when the number of descriptions written changes
def check_achieve_write(frame):
    print("this was called")
    utils.state.num_written += 1
    if(utils.state.num_written >= 1 and utils.state.achievements[8] == 0):
        utils.state.achievements[8] = 1
        overlay_notification(frame, "Tracking thoughts achievement achieved! Wrote 1 game entry")
    if(utils.state.num_written >= 10 and utils.state.achievements[9] == 0):
        utils.state.achievements[9] = 1
        overlay_notification(frame, "Reviewer achievement achieved! Wrote 10 game entries")
    if(utils.state.num_written >= 20 and utils.state.achievements[10] == 0):
        utils.state.achievements[10] = 1
        overlay_notification(frame, "Any good games yet? achievement achieved! Wrote 20 game entries")
    if(utils.state.num_written >= 50 and utils.state.achievements[11] == 0):
        utils.state.achievements[11] = 1
        overlay_notification(frame, "Yelp reviewer achievement achieved! Wrote 50 game entries")
    if(utils.state.num_written >= 100 and utils.state.achievements[12] == 0):
        utils.state.achievements[12] = 1
        overlay_notification(frame, "Documentarian achievement achieved! Wrote 100 game entries")
    write_achieve()

#updates when the number of times the wheel has been spun changes
def check_achieve_spin(frame):
    utils.state.num_spin += 1
    if(utils.state.num_spin >= 1 and utils.state.achievements[13] == 0):
        utils.state.achievements[13] = 1
        overlay_notification(frame, "Switching it up achievement achieved! Spin the wheel 1 time")
    if(utils.state.num_spin >= 10 and utils.state.achievements[14] == 0):
        utils.state.achievements[14] = 1
        overlay_notification(frame, "Up to luck achievement achieved! Spin the wheel 10 times")
    if(utils.state.num_spin >= 50 and utils.state.achievements[15] == 0):
        utils.state.achievements[15] = 1
        overlay_notification(frame, "Variety gamer achievement achieved! Spin the wheel 50 times")
    if(utils.state.num_spin >= 100 and utils.state.achievements[16] == 0):
        utils.state.achievements[16] = 1
        overlay_notification(frame, "Making it fun achievement achieved! Spin the wheel 100 times")
    if(utils.state.num_spin >= 1000 and utils.state.achievements[17] == 0):
        utils.state.achievements[17] = 1
        overlay_notification(frame, "Variety challenge achievement achieved! Spin the wheel 1000 times")
    write_achieve()

#updates when you spin the wheel
def check_achieve_pick(frame):
    utils.state.cur_no_game += 1
    if(utils.state.cur_no_game > utils.state.max_no_game):
        utils.state.max_no_game = utils.state.cur_no_game
        if(utils.state.max_no_game >= 1 and utils.state.achievements[18] == 0):
            utils.state.achievements[18] = 1
            overlay_notification(frame, "Russian Roulette achievement achieved! Spin once without choosing a game")
        if(utils.state.max_no_game >= 5 and utils.state.achievements[19] == 0):
            utils.state.achievements[19] = 1
            overlay_notification(frame, "Red or Black? achievement achieved! Spin 5 times without choosing a game")
        if(utils.state.max_no_game >= 10 and utils.state.achievements[20] == 0):
            utils.state.achievements[20] = 1
            overlay_notification(frame, "Double Whammy achievement achieved! Spin 10 times without choosing a game")
        if(utils.state.max_no_game >= 20 and utils.state.achievements[21] == 0):
            utils.state.achievements[21] = 1
            overlay_notification(frame, "Found one yet? achievement achieved! Spin 20 times without choosing a game")
        if(utils.state.max_no_game >= 50 and utils.state.achievements[22] == 0):
            utils.state.achievements[22] = 1
            overlay_notification(frame, "Green? achievement achieved! Spin 50 times without choosing a game")
        if(utils.state.max_no_game >= 100 and utils.state.achievements[23] == 0):
            utils.state.achievements[23] = 1
            overlay_notification(frame, "Unlucky? achievement achieved! Spin 100 times without choosing a game")
        write_achieve()

#updates every time a new game is chosen
def check_achieve_cons(frame):
    utils.state.cur_no_choose += 1
    if(utils.state.cur_no_choose > utils.state.max_no_choose):
        utils.state.max_no_choose = utils.state.cur_no_choose
        if(utils.state.max_no_choose >= 1 and utils.state.achievements[24] == 0):
            utils.state.achievements[24] = 1
            overlay_notification(frame, "Follow through achieved! Complete a game without choosing another")
        if(utils.state.max_no_choose >= 10 and utils.state.achievements[25] == 0):
            utils.state.achievements[25] = 1
            overlay_notification(frame, "Dedicated to luck achieved! Complete 10 games without choosing another")
        if(utils.state.max_no_choose >= 20 and utils.state.achievements[26] == 0):
            utils.state.achievements[26] = 1
            overlay_notification(frame, "Luck of the draw achieved! Complete 20 games without choosing another")
        if(utils.state.max_no_choose >= 50 and utils.state.achievements[27] == 0):
            utils.state.achievements[27] = 1
            overlay_notification(frame, "A fun challenge achieved! Complete 50 games without choosing another")
        write_achieve()

#updates when a game is completed
def check_achieve_time(name, frame):
    csv_path = utils.util.get_csv_path("games.csv")
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for i in reader:
            if(name == i[0]):
                #N/A means we havent started the game
                #this could happen if someone adds a game as "not started"
                #and immediately goes to "completed"
                if(i[5] != "N/A"):
                    dt_obj = datetime.strptime(i[5], "%Y-%m-%d %H:%M:%S.%f")
                    #automatically uses current time within X days of starting it and we
                    #havent gotten the achievment yet, do the following
                    diff = time_diff(dt_obj).days
                    #if we completed the game
                    if(diff <= 1 and utils.state.achievements[28] == 0):
                        utils.state.achievements[28] = 1
                        print("speedrunner achieved")
                        overlay_notification(frame, "Speedrunner achievement achieved! Complete a game in under a day")
                        write_achieve()
                    if(diff <= 7 and utils.state.achievements[29] == 0):
                        utils.state.achievements[29] = 1
                        print("one week wonder")
                        write_achieve()
                        overlay_notification(frame, "One week wonder achievement achieved! Complete a game in under a week")
                    if(diff <= 30 and utils.state.achievements[30] == 0):
                        utils.state.achievements[30] = 1
                        print("Game enjoyer achieved")
                        write_achieve()
                        overlay_notification(frame, "Game enjoyer achieved! Complete a game in under a month")
                #we could call write_achieve() here, but it wastes time
                #redundancy seems like the better choice for now

#this will be added later. call the function still as usual in the normal places
def check_achieve_day():
    return None

#updates once when a game is added with no image
def check_achieve_image(frame):
    if(utils.state.achievements[36] == 0):
        print("incognito get")
        utils.state.achievements[36] = 1
        overlay_notification(frame, "incognito achievement achieved! Add a game with no image")
        write_achieve()

#writes the csv file. called quite a few times, but we need to ensure persistence
def write_achieve():
    csv_path = utils.util.get_csv_path("achieve.csv")
    with open(csv_path, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow([utils.state.num_played])
        writer.writerow([utils.state.num_completed])
        writer.writerow([utils.state.num_written])
        writer.writerow([utils.state.num_spin])
        writer.writerow([utils.state.max_no_game])
        writer.writerow([utils.state.cur_no_game])
        writer.writerow([utils.state.max_no_choose])
        writer.writerow([utils.state.cur_no_choose])
        writer.writerow([utils.state.achievements[28]])
        writer.writerow([utils.state.achievements[29]])
        writer.writerow([utils.state.achievements[30]])
        writer.writerow([utils.state.achievements[31]])
        writer.writerow([utils.state.achievements[32]])
        writer.writerow([utils.state.achievements[33]])
        writer.writerow([utils.state.achievements[34]])
        writer.writerow([utils.state.achievements[35]])
        writer.writerow([utils.state.achievements[36]])
        print("wrote to CSV file achievements")

#for displaying the notification that an achievement has been gotten happens
def overlay_notification(frame, message="Achievement!", duration=5000):
    label = tk.Label(frame, text=message, bg="#222", fg="white", font=("Arial", 11, "bold"))
    label.place(relx=0.5, rely=0.05, anchor="n")

    def fade_out():
        label.destroy()

#chunky, but essentially, just loads the text when the screen is loaded
def load_achieve_screen(root, go_to_home):
    back_btn = tk.Button(root, text="Back", command=go_to_home)
    
    achieve_label = ach_label(root, [("Achievements:\n", "black"), ("Played games\n", "black"),
    ("Newbie: Play one game: ", "black"), ("COMPLETE" if utils.state.achievements[0] else "NOT COMPLETE", "green" if utils.state.achievements[0] else "red"),
    ("\nGetting the hang of it: Play 10 games: ", "black"), ("COMPLETE" if utils.state.achievements[1] else "NOT COMPLETE", "green" if utils.state.achievements[1] else "red"),
    ("\nThe regular: Play 50 games: ", "black"), ("COMPLETE" if utils.state.achievements[2] else "NOT COMPLETE", "green" if utils.state.achievements[2] else "red"),
    ("\nProfessional Gamer: Play 100 games: ", "black"), ("COMPLETE" if utils.state.achievements[3] else "NOT COMPLETE", "green" if utils.state.achievements[3] else "red"),
    ("\nCompleted games", "black"),
    ("\nFirst game!: Complete one game: ", "black"), ("COMPLETE" if utils.state.achievements[4] else "NOT COMPLETE", "green" if utils.state.achievements[4] else "red"),
    ("\nSeasoned gamer: Complete 10 games: ", "black"), ("COMPLETE" if utils.state.achievements[5] else "NOT COMPLETE", "green" if utils.state.achievements[5] else "red"),
    ("\nCompletionist: Complete 50 games: ", "black"), ("COMPLETE" if utils.state.achievements[6] else "NOT COMPLETE", "green" if utils.state.achievements[6] else "red"),
    ("\nCompletionist ++: Complete 100 games: ", "black"), ("COMPLETE" if utils.state.achievements[7] else "NOT COMPLETE", "green" if utils.state.achievements[7] else "red"),
    ("\nDescriptions", "black"),
    ("\nTracking thoughts: Change the description in one game: ", "black"), ("COMPLETE" if utils.state.achievements[8] else "NOT COMPLETE", "green" if utils.state.achievements[8] else "red"),
    ("\nReviwer: Change the description of 10 games: ", "black"), ("COMPLETE" if utils.state.achievements[9] else "NOT COMPLETE", "green" if utils.state.achievements[9] else "red"),
    ("\nAny good games yet?: Change the description of 20 games: ", "black"), ("COMPLETE" if utils.state.achievements[10] else "NOT COMPLETE", "green" if utils.state.achievements[10] else "red"),
    ("\nYelp reviewer: Change the description of 50 games: ", "black"), ("COMPLETE" if utils.state.achievements[11] else "NOT COMPLETE", "green" if utils.state.achievements[11] else "red"),
    ("\nDocumentarian: Change the description of 100 games: ", "black"), ("COMPLETE" if utils.state.achievements[12] else "NOT COMPLETE", "green" if utils.state.achievements[12] else "red"),
    ("\nThe Wheel", "black"),
    ("\nSwitching it up: Spin the wheel of choice once: ", "black"), ("COMPLETE" if utils.state.achievements[13] else "NOT COMPLETE", "green" if utils.state.achievements[13] else "red"),
    ("\nUp ot luck: Spin the wheel of choice 10 times: ", "black"), ("COMPLETE" if utils.state.achievements[14] else "NOT COMPLETE", "green" if utils.state.achievements[14] else "red"),
    ("\nVariety gamer: Spin the wheel of choice 50 times: ", "black"), ("COMPLETE" if utils.state.achievements[15] else "NOT COMPLETE", "green" if utils.state.achievements[15] else "red"),
    ("\nMaking it fun: Spin the wheel of choice 100 times: ", "black"), ("COMPLETE" if utils.state.achievements[16] else "NOT COMPLETE", "green" if utils.state.achievements[16] else "red"),
    ("\nVariety challenge: Spin the wheel of choice 1000 times: ", "black"), ("COMPLETE" if utils.state.achievements[17] else "NOT COMPLETE", "green" if utils.state.achievements[17] else "red"),
    ("\nRussian roulette: Spin the wheel of choice once without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[18] else "NOT COMPLETE", "green" if utils.state.achievements[18] else "red"),
    ("\nRed or black?: Spin the wheel of choice 5 times in a row without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[19] else "NOT COMPLETE", "green" if utils.state.achievements[19] else "red"),
    ("\nDouble whammy: Spin the wheel of choice 10 times in a row without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[20] else "NOT COMPLETE", "green" if utils.state.achievements[20] else "red"),
    ("\nFound one yet?: Spin the wheel of choice 20 times in a row without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[21] else "NOT COMPLETE", "green" if utils.state.achievements[21] else "red"),
    ("\nGreen?: Spin the wheel of choice 50 times in a row without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[22] else "NOT COMPLETE", "green" if utils.state.achievements[22] else "red"),
    ("\nUnlucky?: Spin the wheel of choice 100 times in a row without choosing a game: ", "black"), ("COMPLETE" if utils.state.achievements[23] else "NOT COMPLETE", "green" if utils.state.achievements[23] else "red"),
    ("\nFinishing games", "black"),
    ("\nFollow through: Finish one game without starting another: ", "black"), ("COMPLETE" if utils.state.achievements[24] else "NOT COMPLETE", "green" if utils.state.achievements[24] else "red"),
    ("\nDedicated to luck: Finish 10 games in a row without starting another: ", "black"), ("COMPLETE" if utils.state.achievements[25] else "NOT COMPLETE", "green" if utils.state.achievements[25] else "red"),
    ("\nLuck of the draw: Finish 20 games in a row without starting another: ", "black"), ("COMPLETE" if utils.state.achievements[26] else "NOT COMPLETE", "green" if utils.state.achievements[26] else "red"),
    ("\nA fun challenge: Finish 50 games in a row without starting another: ", "black"), ("COMPLETE" if utils.state.achievements[27] else "NOT COMPLETE", "green" if utils.state.achievements[27] else "red"),
    ("\nTime", "black"),
    ("\nSpeedrunner: Finish a game in a day: ", "black"), ("COMPLETE" if utils.state.achievements[28] else "NOT COMPLETE", "green" if utils.state.achievements[28] else "red"),
    ("\nOne week wonder: Finish a game in a week: ", "black"), ("COMPLETE" if utils.state.achievements[29] else "NOT COMPLETE", "green" if utils.state.achievements[29] else "red"),
    ("\nGame enjoyer: Finish a game in a month: ", "black"), ("COMPLETE" if utils.state.achievements[30] else "NOT COMPLETE", "green" if utils.state.achievements[30] else "red"),
    ("\nIncognito: Add a game without an image: ", "black"), ("COMPLETE" if utils.state.achievements[36] else "NOT COMPLETE", "green" if utils.state.achievements[36] else "red")
    ])
    achieve_label.pack()
    back_btn.pack()

#helper funciton to laod text with colors
def ach_label(parent, text_parts):
    size_of_text = 39
    # text_parts = [("Normal ", "black"), ("Red", "red"), (" again", "black")]
    widget = tk.Text(parent, height=size_of_text, borderwidth=0, bg=parent["bg"])
    widget.configure(state='normal')
    default_font = tkfont.Font(family="Arial", size=10, weight="normal")

    for i, (part, color) in enumerate(text_parts):
        start_index = widget.index("end-1c")  # Start BEFORE inserting
        widget.insert("end", part)
        end_index = widget.index("end-1c")    # End AFTER inserting

        tag_name = f"tag_{i}"
        widget.tag_add(tag_name, start_index, end_index)
        widget.tag_config(tag_name, foreground=color, font=default_font)

    widget.configure(state='disabled')  # Make it uneditable
    widget.pack()
    return widget