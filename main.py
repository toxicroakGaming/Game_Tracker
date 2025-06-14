import tkinter as tk
from ui.update_screen import load_update_screen
from ui.home_screen import load_home_screen
from ui.journal import load_journal_screen, load_add_screen
import csv
import sys, os

def get_csv_path(filename):
    """Returns the correct writable path for CSV in both dev and PyInstaller"""
    if getattr(sys, 'frozen', False):  # Running in a PyInstaller bundle
        base_path = os.path.dirname(sys.executable)
    else:  # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

def ensure_csv_exists():
    csv_path = get_csv_path("games.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['name', 'progress'])

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

ensure_csv_exists()
root = tk.Tk()
root.title("Game Tracker")
root.geometry("1000x800")

# Start at home screen
show_home_screen()

root.mainloop()