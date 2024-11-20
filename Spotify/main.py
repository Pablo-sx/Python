import tkinter as tk
from tkinter import ttk

# Funkcja uruchamiająca interfejs aplikacji
def run_gui():
    # Inicjalizacja głównego okna
    root = tk.Tk()
    root.title("Srotify")
    root.geometry("800x600")
    root.config(bg="#181818")
    root.minsize(600, 400)
    
    # Konfiguracja grid layoutu dla dynamicznego dopasowania
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=4)
    root.rowconfigure(1, weight=1)

#niw 


    # Pasek boczny zmieniam sobie to cos
    sidebar = tk.Frame(root, bg="black", width=200)
    sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")
    
    # Lista przycisków w pasku bocznym
    buttons = ["Home", "Browse", "Your Library", "Create Playlist", "Liked Songs"]
    for button_text in buttons:
        button = tk.Button(sidebar, text=button_text, bg="black", fg="white", font=("Arial", 10), relief="flat")
        button.pack(fill="x", pady=5, padx=10)
    
    # Górny pasek z polem wyszukiwania
    top_bar = tk.Frame(root, bg="#121212", height=50)
    top_bar.grid(row=0, column=1, sticky="ew")
    
    # Wyszukiwanie
    search_label = tk.Label(top_bar, text="Search:", bg="#78DE78", fg="black")
    search_label.pack(side="left", padx=10)
    
    search_entry = tk.Entry(top_bar, width=40, font=("Arial", 12))
    search_entry.pack(side="left", padx=5, pady=10)

    # Sekcja główna na wyniki wyszukiwania
    main_content = tk.Frame(root, bg="#181818")
    main_content.grid(row=1, column=1, sticky="nsew")
    
    # Lista piosenek (jako placeholder)
    for i in range(69, 70):
        song_label = tk.Label(main_content, text=f"Twoj stary w betoniarce {i}", bg="#181818", fg="white", font=("Arial", 10))
        song_label.pack(anchor="w", padx=20, pady=2)
    
    # Uruchomienie głównej pętli
    root.mainloop()

# Uruchomienie interfejsu
run_gui()