import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import io
import sys

#kolory dla programu
side_bar_color = '#181818'
top_bar_color = '#181818'
root_color='#282828'

########################################################################## FUNKCJE ##########################################################################
connection = mysql.connector.connect(host="localhost", user="root", password="", database="projekt")
mycur=connection.cursor()
#zmiana pasek pojawiający się przy ikonach w side bar

def show_song(page, x, y):

    frame = tk.Frame(page, height=200, width=150, bg="red")
    frame.place(x=x, y=y)


    like_img = Image.open("Img/liked.png")
    like_img = like_img.resize((20, 20))
    like = ImageTk.PhotoImage(like_img)
    disc=PhotoImage(file="img/disc.png")
    lb = tk.Label(frame, image=disc, bg=root_color)
    lb.image = disc
    lb.pack()
    
    like_btn = tk.Button(frame, image=like, bg=root_color, bd=0, activebackground=root_color)
    like_btn.image = like
    like_btn.pack(pady=5)

def changing_color(label, page):

    home_side_place.config(bg=side_bar_color)
    library_side_place.config(bg=side_bar_color)
    browse_side_place.config(bg=side_bar_color)
    create_side_place.config(bg=side_bar_color)
    liked_side_place.config(bg=side_bar_color)

    label.config(bg="white")

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
    user_id=1
    home_page_frame.pack(fill=tk.BOTH, expand=True)


def library_page():
    library_page_frame = tk.Frame(page_frame, bg=root_color)

    mycur.execute("SELECT img FROM albums LIMIT 5")
    result = mycur.fetchall()

    x = 100
    y = 175
    lb1 = tk.Label(library_page_frame, text="Polubione utwory", font=("Arial", 20), bg=root_color, fg="white")
    lb1.place(x=100, y=125)

    for row in result:
        show_song(page=library_page_frame, x=x, y=y)
        x += 200
     
    library_page_frame.pack(fill=tk.BOTH, expand=True)
    
def browse_page():
    browse_page_frame=tk.Frame(page_frame,bg=root_color)
    lb=tk.Label(browse_page_frame, text="Browse page", font=('arial', 50)).place(x=100, y=200)
    browse_page_frame.pack(fill=tk.BOTH, expand=True)


def create_page():
    global add_imie, add_nazwisko, add_nralb

    create_page_frame=tk.Frame(page_frame,bg=root_color)
    main_label=tk.Label(create_page_frame, text="Dodaj piosenki do listy",font=("Arial, 20"),fg='white',bg=root_color).place(x=100, y=100)
    lb_imie=tk.Label(create_page_frame, text="Nazwa:", bg=root_color, fg=("gray")).place(x=100,y=150)
    lb_album=tk.Label(create_page_frame, text="Album:", bg=root_color, fg=("gray")).place(x=100,y=190)
    lb_nrpes=tk.Label(create_page_frame, text="Nr:", bg=root_color, fg=("gray")).place(x=100,y=230)


    add_imie=tk.Entry(create_page_frame, width=40, bg=root_color,bd=0,relief="flat", fg="white").place(x=145, y=152)
    add_nazwisko=tk.Entry(create_page_frame, width=40, bg=root_color,bd=0,relief="flat", fg="white").place(x=145, y=192)
    add_nralb=tk.Entry(create_page_frame, width=40, bg=root_color,bd=0,relief="flat", fg="white").place(x=145, y=232)
    submit=tk.Button(create_page_frame, text="Add!", bg="gray",bd=0,relief="flat" ,command=add_to_db).place(x=100, y=270)
    create_page_frame.pack(fill=tk.BOTH, expand=True)

def liked_page():
    liked_page_frame = tk.Frame(page_frame, bg=root_color)
    liked_page_frame.pack(fill=tk.BOTH, expand=True)
    lb=tk.Label(liked_page_frame, text="Liked page", font=('arial', 50)).place(x=100, y=200)

def entry_but(event=None):
    entry=search.get()
    if entry!="":
        mycur.execute("SELECT * FROM studnets WHERE imie LIKE %s", (f"%{entry}%",))
        result=mycur.fetchall()
        print(result)
        search.delete(0, "end")


def add_to_db():
    imie = add_imie.get()
    nazwisko = add_nazwisko.get()
    nralb = add_nralb.get()
    query = "INSERT INTO students (Imie, Nazwisko, Numer_alb) VALUES (%s)"
    mycur.execute(query, (imie,nazwisko,nralb))

########################################################################## ELEMENTY W OKNIE ##########################################################################

root = tk.Tk()
root.geometry("900x600")
root.config(bg=root_color)
root.minsize(900, 600)

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
page_frame=tk.Frame(root)
side_bar = tk.Frame(root, bg=side_bar_color, width=45)
top_bar = tk.Frame(root, bg=top_bar_color, height=45)

search=tk.Entry(top_bar, width=70)
search.bind("<Return>", entry_but)
search_label = tk.Label(top_bar, text="Search:", bg="#78DE78", fg="black")
search_btn = tk.Button(top_bar, text="Go!", bg="#27D75C", fg="black", command=entry_but)

home_page_lb=tk.Label(side_bar, text='Home', bg=side_bar_color, fg='white', font=('Bold', 15))
library_page_lb=tk.Label(side_bar, text='Library', bg=side_bar_color, fg='white', font=('Bold', 15))
browse_page_lb=tk.Label(side_bar, text='Browse', bg=side_bar_color, fg='white', font=('Bold', 15))
create_page_lb=tk.Label(side_bar, text='Create', bg=side_bar_color, fg='white', font=('Bold', 15))
liked_page_lb=tk.Label(side_bar, text='Liked', bg=side_bar_color, fg='white', font=('Bold', 15))

page_frame.place(relwidth=1.0, relheight=1.0, x=200)
home_page()
#przyciski w side bar
side_bar_btn = tk.Button(side_bar, bg=side_bar_color, image=image_side_bar, bd=0, activebackground=side_bar_color, command=extend_side_bar)
home_btn = tk.Button(side_bar, bg=side_bar_color, image=image_home, 
    bd=0, activebackground=side_bar_color, 
    command=lambda: changing_color(label=home_side_place, 
                                    page=home_page)
)

library_btn = tk.Button(
    side_bar, bg=side_bar_color, image=image_library,
    bd=0, activebackground=side_bar_color,
    command=lambda: changing_color(label=library_side_place, page=library_page)
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

########################################################################## ROZMIESZCZANIE ELEMENTÓW W OKNIE ##########################################################################

side_bar.pack(side=tk.LEFT, fill="y", pady=3, padx=3)
top_bar.place(x=45, relwidth=1.0)

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
label_info = tk.Label(root, text="", bg="white", fg="black", font=("Arial, 40"), relief="solid")

home_page_lb.place(x=45, y=130, width=100, height=40)
library_page_lb.place(x=45, y=200, width=100, height=40)
browse_page_lb.place(x=45, y=270, width=100, height=40)
create_page_lb.place(x=45, y=340, width=100, height=40)
liked_page_lb.place(x=45, y=410, width=100, height=40)

user_id = sys.argv[1]

search.place(x=220,y=6, height=30)
search_label.place(x=160,y=6, height=30)
search_btn.place(x=660, y=6, height=30)
query1="SELECT name FROM users WHERE user_id=%s"
mycur.execute(query1,(user_id,))
result=mycur.fetchone()
user=tk.Label(top_bar,bg=top_bar_color, text=result[0], fg='white', font=('Arail', 15)).pack(side=tk.RIGHT, padx=(10,60))

root.mainloop()
