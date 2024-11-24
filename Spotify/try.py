import tkinter as tk
from tkinter import messagebox

#zmiana pasek pojawiający się przy ikonach w side bar
def changing_color(label, page):
    home_side_place.config(bg=side_bar_color)
    library_side_place.config(bg=side_bar_color)
    browse_side_place.config(bg=side_bar_color)
    create_side_place.config(bg=side_bar_color)
    liked_side_place.config(bg=side_bar_color)

    label.config(bg='white')

    for frame in page_frame.winfo_children():
        frame.destroy()

    page()

def info_show(event):
    label_info.place(x=event.x_root - root.winfo_rootx() + 10, 
                     y=event.y_root - root.winfo_rooty() + 10)
    label_info.config(text="Strone stworzył Pablo-sx <3")

def info_hide(event):
    label_info.config(text="")
    label_info.place_forget()

def extend_side_bar():
    side_bar.config(width=200)
    side_bar_btn.config(image=image_close, command=hide_side_bar)

def hide_side_bar():
    side_bar.config(width=45)
    side_bar_btn.config(image=image_side_bar,command=extend_side_bar)

def home_page():
    home_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(home_page_frame, text="Home Page", font=('arial', 50)).place(x=100, y=200)
    home_page_frame.pack(fill=tk.BOTH, expand=True)

def library_page():
    library_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(library_page_frame, text="Library page", font=('arial', 50)).place(x=100, y=200)
    library_page_frame.pack(fill=tk.BOTH, expand=True)

def browse_page():
    browse_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(browse_page_frame, text="Browse page", font=('arial', 50)).place(x=100, y=200)
    browse_page_frame.pack(fill=tk.BOTH, expand=True)

def create_page():
    create_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(create_page_frame, text="Create page", font=('arial', 50)).place(x=100, y=200)
    create_page_frame.pack(fill=tk.BOTH, expand=True)

def liked_page():
    liked_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(liked_page_frame, text="Liked page", font=('arial', 50)).place(x=100, y=200)
    liked_page_frame.pack(fill=tk.BOTH, expand=True)

#kolory dla programu
side_bar_color = '#383838'
root_color='gray'

root = tk.Tk()
root.geometry("800x600")
root.config(bg=root_color)
root.minsize(800, 600)

#obrazki dla ikon z side bar
image_side_bar = tk.PhotoImage(file='Img/icon.png')
image_home = tk.PhotoImage(file='Img/home.png')
image_library= tk.PhotoImage(file='Img/library.png')
image_browse=tk.PhotoImage(file='Img/browse.png')
image_create=tk.PhotoImage(file='Img/create.png')
image_liked=tk.PhotoImage(file='Img/liked.png')
image_info=tk.PhotoImage(file=('Img/info.png'))
image_close=tk.PhotoImage(file='Img/close.png')

#web frames
side_bar = tk.Frame(root, bg=side_bar_color, width=45)
page_frame=tk.Frame(root)

page_frame.place(relwidth=1.0, relheight=1.0, x=200)
home_page()
#przyciski w side bar
side_bar_btn = tk.Button(side_bar, bg=side_bar_color, image=image_side_bar, bd=0, activebackground=side_bar_color, command=extend_side_bar)
home_btn = tk.Button(side_bar, bg=side_bar_color, image=image_home, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(label=home_side_place, 
                                    page=home_page)
)

library_btn = tk.Button(side_bar, bg=side_bar_color, image=image_library, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(library_side_place, 
                                    page=library_page)
)

browse_btn = tk.Button(side_bar, bg=side_bar_color, image=image_browse, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(browse_side_place, page=browse_page)
)

create_btn = tk.Button(side_bar, bg=side_bar_color, image=image_create, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(create_side_place, page=create_page)
)

liked_btn = tk.Button(side_bar, bg=side_bar_color, image=image_liked, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(liked_side_place, page=liked_page)
)

info_btn = tk.Button(side_bar, bg=side_bar_color, image=image_info, 
    bd=0, activebackground=side_bar_color
)

#pasek przy ikonach side bar
home_side_place = tk.Label(side_bar, bg='white')
library_side_place = tk.Label(side_bar, bg=side_bar_color)
browse_side_place = tk.Label(side_bar, bg=side_bar_color)
create_side_place = tk.Label(side_bar, bg=side_bar_color)
liked_side_place = tk.Label(side_bar, bg=side_bar_color)

side_bar.pack(side=tk.LEFT, fill="y", pady=3, padx=3)

side_bar_btn.place(x=4, y=4)

home_btn.place(x=9, y=130, width=30, height=40)
library_btn.place(x=9, y=200, width=30, height=40)
browse_btn.place(x=9, y=270, width=30, height=40)
create_btn.place(x=9, y=340, width=30, height=40)
liked_btn.place(x=9, y=410, width=30, height=40)

info_btn.place(x=9, y=480,width=30, height=40)
info_btn.bind("<Enter>", info_show)
info_btn.bind("<Leave>", info_hide)

home_side_place.place(x=3, y=130, width=3, height=40)
library_side_place.place(x=3, y=200, width=3, height=40) 
browse_side_place.place(x=3, y=270, width=3, height=40) 
create_side_place.place(x=3, y=340, width=3, height=40) 
liked_side_place.place(x=3, y=410, width=3, height=40) 
label_info = tk.Label(root, text="", bg="white", fg="black", font=("Arial", 10), relief="solid")

root.mainloop()