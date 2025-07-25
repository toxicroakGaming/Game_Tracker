import tkinter as tk

def load_update_screen(root, go_to_home):
    do_screen(root, go_to_home)

def do_screen(root, go_to_home, width = 300, height = 20):
    
    message = ("1.0.0:\n - Added Updates screen\n - Changed home screen\n - Added Collection screen"+ 
    " where you can see your list of games and add to the list\n" +
    "\n1.0.1:\n - Changed collections and home screens\n" + 
    " - different list system for collection list\n" +
    " - Home screen now shows game being currently played\n"+
    " - You can set game being currently played in the collections menu\n" + 
    "\n1.0.2\n - Bugfixes\n" +
    " - Added the ability to remove games from your collection\n" + 
    " - Added confirmation when any action is done\n" +
    "1.0.3\n - Added Backgrounds\n" + 
    " - You can also add custom backgrounds" +
    "\n1.0.4\n - You can change the status of games in the list" +
    "\n1.0.5\n - Revamped collection screen. Now includes images" + 
    "\n - Current game being played also includes an image on the home screen\n" +
    " - *mini update to 1.0.5* Added new default background\n" + 
    "\n1.0.6\n" +
    " - bugfixes" + 
    " - made everything persistent\n" + 
    "\n1.0.7\n" + 
    "- Added sorting features on the collections screen\n" + 
    "\n1.0.8\n" +
    " - Added the choice to let the program randomly choose a game for you to play" + 
    "\n1.1.0\n" + 
    " - UI changes\n" + 
    " - bugfixes\n" + 
    "\n1.1.1\n" +
    " - Stability update, future plans added behind the scenes\n" +
    "\n1.1.2\n" + 
    " - Added achievements\n" + 
    "\n1.1.3\n" + 
    " - major bugfixes\n" +
    "\n1.1.4\n" + 
    " - Added tags!\n")
    
    label = tk.Label(root, text="Updates\n" + 
    "CURRENT VERSION: 1.1.4", font=("Arial", 16))
    label.pack(pady=20)
    frame = tk.Frame(root)
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")
    frame.pack(fill="both", expand=False, padx=10, pady=10)
    text = tk.Text(
        frame,
        wrap="word",
        yscrollcommand=scrollbar.set,
        width = width,
        height = height,
        bg=root["bg"],
        borderwidth=0,
    )
    text.insert("end", message)
    text.config(state="disabled")
    text.pack(side="left", fill="x", expand=True)
    text.configure(padx=0, pady=0)  # Removes internal padding
    text.tag_configure("all", spacing1=0, spacing3=0)  # Removes spacing before/after lines
    text.tag_add("all", "1.0", "end")
    back_btn = tk.Button(root, text="Back to Home", command=go_to_home)
    back_btn.pack(pady=20)
    scrollbar.config(command=text.yview)