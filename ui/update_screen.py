import tkinter as tk

def load_update_screen(root, go_to_home):
    label = tk.Label(root, text="Updates", font=("Arial", 16))
    label.pack(pady=20)

    label2 = tk.Label(root, text="1.0.0:\n - Added Updates screen\n - Changed home screen\n - Added Collection screen"+ 
    " where you can see your list of games and add to the list", font=("Arial", 10))
    label2.pack(pady=20)

    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    back_btn.pack(pady=20)