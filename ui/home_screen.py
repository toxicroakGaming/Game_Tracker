import tkinter as tk
from PIL import ImageTk, Image 

def load_home_screen(root, go_to_update, go_to_journal):
    label = tk.Label(root, text="Welcome to Game Tracker!", font=("Arial", 16))
    label.pack(pady=20)
    
    image_path = "ui/media/games.png"  
    try:
        image = Image.open(image_path)
        print("✅ Image loaded:", image_path)
    except Exception as e:
        print("❌ Failed to load image:", e)
    resized_image = image.resize((275, 225))
    photo_image = ImageTk.PhotoImage(resized_image)
    label2 = tk.Label(root, image=photo_image)
    label2.image = photo_image
    btn = tk.Button(root, text="Updates", command=go_to_update)
    btn2 = tk.Button(root, text="Collection", command=go_to_journal)
    btn.pack()
    btn2.pack()
    label.pack(pady=20)
    label2.pack()