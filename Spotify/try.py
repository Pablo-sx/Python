import tkinter as tk

# Tworzenie głównego okna
root = tk.Tk()
root.geometry("800x600")
root.config(bg="gray")

def changing_color(label):
    # Funkcja zmienia kolor tła przekazanej etykiety
    label.config(bg='white')

# Wczytywanie obrazków
image_side_bar = tk.PhotoImage(file='Img/icon.png')
image_home = tk.PhotoImage(file='Img/home.png')
side_bar_color = '#383838'

# Tworzenie paska bocznego
side_bar = tk.Frame(root, bg=side_bar_color, width=45)

# Tworzenie przycisków i etykiety
side_bar_btn = tk.Button(side_bar, bg=side_bar_color, image=image_side_bar, bd=0, activebackground=side_bar_color)
home_btn = tk.Button(
    side_bar, 
    bg=side_bar_color, 
    image=image_home, 
    bd=0, 
    activebackground=side_bar_color, 
    command=lambda: changing_color(home_side_place)  # Przekazanie obiektu etykiety
)
home_side_place = tk.Label(side_bar, bg=side_bar_color)

# Ustawianie elementów na pasku bocznym
side_bar.pack(side=tk.LEFT, fill="y", pady=3, padx=3)
side_bar_btn.place(x=4, y=4)
home_btn.place(x=9, y=130, width=30, height=40)  # Przycisk "home" niżej, aby się nie nachodził
home_side_place.place(x=3, y=130, width=3, height=40)

# Uruchomienie pętli głównej
root.mainloop()