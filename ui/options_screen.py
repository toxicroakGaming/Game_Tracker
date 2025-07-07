import tkinter as tk
from PIL import ImageTk, Image 
import csv
import sys, os
from utils.util import *
from utils.state import *

#size of the images on the backgrounds page
thumb_size = (150, 100)
#where are the backgrounds stored?
bg_folder = get_resource_path(r'ui\media\bg')
#keep alive
image_buttons = []


def load_image_screen(root, show_home_screen, show_image_screen):
    global image_buttons
    image_buttons = []  # Clear old references

    # Clear existing widgets if you haven't already
    clear_screen(root)

    # Top label
    top_label = tk.Label(root, text="Change Background", font=("Arial", 16))
    top_label.pack(pady=10)

    # Container for the scrollable area
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    # Canvas and scrollbar
    canvas = tk.Canvas(container, bg = "#ffffff", highlightthickness=0)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ffffff")

    # Configure scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Load all background images
    image_files = [f for f in os.listdir(bg_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    row = 0
    col = 0
    max_cols = 4

    for img_file in image_files:
        full_path = os.path.join(bg_folder, img_file)
        try:
            pil_img = Image.open(full_path).resize((150, 150))
            tk_img = ImageTk.PhotoImage(pil_img)
            image_buttons.append(tk_img)  # keep reference

            btn = tk.Button(
                scrollable_frame,
                image=tk_img,
                command=lambda path=full_path: (
                    on_background_click(root, path),
                    clear_screen(root),
                    load_image_screen(root, show_home_screen, show_image_screen)
                )
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        except Exception as e:
            print(f"[ERROR] Could not load {img_file}: {e}")

    # Buttons at the bottom (not inside scrollable area)
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=20)

    load_btn = tk.Button(
        btn_frame,
        text="Load Custom Images",
        command=lambda: (
            load_custom_background(root, background_data, bg_folder),
            clear_screen(root),
            load_image_screen(root, show_home_screen, show_image_screen)
        )
    )
    load_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(
        btn_frame,
        text="Back to Home",
        command=show_home_screen
    )
    back_btn.grid(row=0, column=1, padx=10)

#what happens when we click a background image? we want to request to change the background to that image!
def on_background_click(root, path):
    print("click")
    data = [path]
    background_label, bg_image = change_bg(root, path, background_data)
    print("[DEBUG] background_data id:", id(background_data))