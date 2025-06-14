import tkinter as tk
from ui.update_screen import load_update_screen
from ui.home_screen import load_home_screen
from ui.journal import load_journal_screen, load_add_screen
import csv

def show_home_screen():
    clear_screen()
    load_home_screen(root, show_update_screen, show_journal_screen)

def show_update_screen():
    clear_screen()
    load_update_screen(root, show_home_screen)

def show_journal_screen():
    clear_screen()
    load_journal_screen(root, show_home_screen, show_add_screen)

def show_add_screen():
    clear_screen()
    load_add_screen(root, show_journal_screen)

def show_remove_screen():
    clear_screen()
    load_remove_screen(root, show_journal_screen)

def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Game Tracker")
root.geometry("1000x800")

# Start at home screen
show_home_screen()

root.mainloop()