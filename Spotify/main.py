import tkinter as tk
from tkinter import ttk

def run_gui():
    # głowne okno łównego okna
    root = tk.Tk()
    root.title("Srotify")
    root.geometry("800x600")
    root.config(bg="#181818")
    root.minsize(800, 400)
    def entry_but():
        entry=search_entry.get()
        print(entry)
    
    # dynamicznego dopasowania
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    root.rowconfigure(1, weight=1)

    # menu boczny
    sidebar = tk.Frame(root, bg="black", width=200)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
    
    # przycisków w menu bocznym
    buttons = ["Home", "Browse", "Your Library", "Create Playlist", "Liked Songs"]
    for button_text in buttons:
        button = tk.Button(sidebar, text=button_text, bg="black", fg="white", font=("Arial", 10), relief="flat")
        button.pack(fill="x", pady=5, padx=10)
    
    # polem wyszukiwania
    top_bar = tk.Frame(root, bg="#121212", height=50)
    top_bar.grid(row=0, column=1, sticky="ew")
    
    # wyszukiwanie
    search_label = tk.Label(top_bar, text="Search:", bg="#78DE78", fg="black")
    search_label.pack(side="left", padx=10)
    
    search_entry = tk.Entry(top_bar, width=50, font=("Arial", 12))
    search_entry.pack(side="left", padx=5, pady=10)
    
    search_button = tk.Button(top_bar, text="Go!", bg="#27D75C", fg="black", command=entry_but)
    search_button.pack(side="left", padx=10)

    #  wyszukiwania
    main_content = tk.Frame(root, bg="#181818")
    main_content.grid(row=1, column=1, sticky="nsew")
    
    # piosenki pole:
    for i in range(69, 70):
        song_label = tk.Label(main_content, text=f"Twoj stary w betoniarce {i}", bg="#181818", fg="white", font=("Arial", 10))
        song_label.pack(anchor="w", padx=20, pady=2)

    root.mainloop()

run_gui()