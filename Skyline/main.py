import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import io
import sys

side_bar_color = '#181818'
top_bar_color = '#181818'
root_color='#282828'
purple_color='#642266'
l_purple_color='#842B87'

########################################################################## FUNKCJE ##########################################################################
connection = mysql.connector.connect(host="localhost", user="root", password="", database="projekt")
mycur=connection.cursor()

user_id = sys.argv[1]
query1="SELECT name FROM users WHERE user_id=%s"
mycur.execute(query1,(user_id,))
user_name=mycur.fetchone()

def show_song(page, x, y, song_title, artist_name, song_id, user_id):
    mycur.execute("SELECT like_id FROM likes WHERE song_id = %s AND user_id = %s", (song_id, user_id))
    result = mycur.fetchone()

    if result:
        is_liked = result[0]
    else:
        is_liked = False  

    frame = tk.Frame(page, height=200, width=250, bg=root_color, relief="solid", bd=1)
    frame.place(x=x, y=y)

    disc = PhotoImage(file="img/disc.png")
    lb = tk.Label(frame, image=disc, bg=root_color)
    lb.image = disc
    lb.pack(pady=10)

    title_label = tk.Label(frame, text=song_title, bg=root_color, fg="white", font=("Arial", 10, "bold"), wraplength=180)
    title_label.pack(pady=5)

    artist_label = tk.Label(frame, text=artist_name, bg=root_color, fg="white", font=("Arial", 8), wraplength=180)
    artist_label.pack()

    like_img = Image.open("Img/like_f.png")
    like_img = like_img.resize((20, 20))
    like = ImageTk.PhotoImage(like_img)

    like_filled_img = Image.open("Img/like_t.png")  # Polubiony
    like_filled_img = like_filled_img.resize((20, 20))
    like_filled = ImageTk.PhotoImage(like_filled_img)

    def toggle_like():
        nonlocal is_liked
        
        if is_liked:
            like_btn.config(image=like)
            like_btn.image = like
            is_liked = False
            mycur.execute("DELETE FROM likes WHERE song_id = %s AND user_id = %s", (song_id, user_id))
        else:
            like_btn.config(image=like_filled)
            like_btn.image = like_filled
            is_liked = True
            mycur.execute("INSERT INTO likes (user_id, song_id) VALUES (%s, %s)", (user_id, song_id))
        connection.commit()

    initial_image = like_filled if is_liked else like
    like_btn = tk.Button(frame, image=initial_image, bg=root_color, bd=0, activebackground=root_color, command=toggle_like)
    like_btn.image = initial_image

    def browse_album():
        mycur.execute("SELECT album_id, title FROM albums WHERE user_id = %s", (user_id,))
        albums = mycur.fetchall()

        browse_window = tk.Toplevel()
        browse_window.title("Wybierz album")
        browse_window.geometry("300x200")
        browse_window.configure(bg=root_color)

        album_var = tk.StringVar()

        album_combobox = ttk.Combobox(browse_window, textvariable=album_var, values=[album[1] for album in albums])
        album_combobox.pack(pady=20)

        def select_album():
            selected_album = album_var.get()
            if selected_album:
                album_id = next(album[0] for album in albums if album[1] == selected_album)
                mycur.execute("UPDATE songs SET album_id = %s WHERE song_id = %s", (album_id, song_id))
                connection.commit()
                messagebox.showinfo("Sukces", f"Piosenka została przypisana do albumu: {selected_album}")
                browse_window.destroy()
            else:
                messagebox.showwarning("Brak albumu", "Proszę wybrać album.")

        select_button = tk.Button(browse_window, text="Wybierz album", command=select_album, bg=purple_color, bd=0, font=("Calibri", 12,"bold"),fg="white")
        select_button.pack(pady=10)

    browse_img = Image.open("Img/browse.png")
    browse_img = browse_img.resize((20, 20))
    browse_icon = ImageTk.PhotoImage(browse_img)

    browse_button = tk.Button(frame, image=browse_icon, bg=root_color, bd=0, activebackground=root_color, command=browse_album)
    browse_button.image = browse_icon

    like_btn.pack(side="left", padx=5)
    browse_button.pack(side="left", padx=5)

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
    label_info.config(text="Strone stworzył Paweł Winowicz i Mateusz Kwolek", font=("Calibri", 14,"bold"))

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
    def navigate_to(page_function):
        """Funkcja nawigacji, która zamyka obecny frame i otwiera nową stronę."""
        for widget in page_frame.winfo_children():
            widget.destroy()
        page_function()

    home_page_frame = tk.Frame(page_frame, bg=root_color)

    welcome_label = tk.Label(
        home_page_frame,
        text=f"Witaj, {user_name[0]}!",
        font=("Arial", 30, "bold"),
        bg=root_color,
        fg="white"
    )
    welcome_label.place(x=160, y=30)
    recent_label = tk.Label(
        home_page_frame,
        text="Ostatnio dodane utwory:",
        font=("Calibri", 18,"bold"),
        bg=root_color,
        fg=l_purple_color
    )
    recent_label.place(x=50, y=100)

    query_recent_songs = """
    SELECT s.title, a.name
    FROM songs s
    JOIN artists a ON s.artist_id = a.artist_id
    ORDER BY s.song_id DESC
    LIMIT 5
    """
    mycur.execute(query_recent_songs)
    recent_songs = mycur.fetchall()

    y_position = 140
    for title, artist in recent_songs:
        song_label = tk.Label(
            home_page_frame,
            text=f"{title} - {artist}",
            font=("Arial", 12),
            bg=root_color,
            fg="white"
        )
        song_label.place(x=60, y=y_position)
        y_position += 30

    recommended_label = tk.Label(
        home_page_frame,
        text="Polecane dla Ciebie:",
        font=("Calibri", 18,"bold"),
        bg=root_color,
        fg=l_purple_color
    )
    recommended_label.place(x=650, y=100)

    def get_most_liked_type():
        query = """
        SELECT s.type, COUNT(*) AS like_count
        FROM likes l
        JOIN songs s ON l.song_id = s.song_id
        WHERE l.user_id = %s
        GROUP BY s.type
        ORDER BY like_count DESC
        LIMIT 1
        """
        mycur.execute(query, (user_id,))
        result = mycur.fetchone()
        return result[0] if result else None

    def fetch_recommended_songs():
        most_liked_type = get_most_liked_type()
        if not most_liked_type:
            return []

        query_recommended_songs = """
        SELECT s.title, a.name
        FROM songs s
        JOIN artists a ON s.artist_id = a.artist_id
        WHERE s.type = %s
        AND s.song_id NOT IN (
            SELECT song_id
            FROM likes
            WHERE user_id = %s
        )
        LIMIT 3
        """
        mycur.execute(query_recommended_songs, (most_liked_type, user_id))
        return mycur.fetchall()

    recommended_songs = fetch_recommended_songs()

    y_position_recommended = 140
    for title, artist in recommended_songs:
        rec_song_label = tk.Label(
            home_page_frame,
            text=f"{title} - {artist}",
            font=("Arial", 12),
            bg=root_color,
            fg="white"
        )
        rec_song_label.place(x=650, y=y_position_recommended)
        y_position_recommended += 30

    quick_access_label = tk.Label(
        home_page_frame,
        text="Szybki dostęp:",
        font=("Calibri", 18,"bold"),
        bg=root_color,
        fg=l_purple_color
    )
    quick_access_label.place(x=50, y=300)

    tk.Button(
        home_page_frame,
        text="Biblioteka",
        bg=purple_color,
        fg="white",
        bd=0,
        font=("Calibri", 12,"bold"),
        command=lambda: navigate_to(library_page),
    ).place(x=60, y=340)

    tk.Button(
        home_page_frame,
        text="Polubione",
        bg=purple_color,
        fg="white",
        bd=0,
        font=("Calibri", 12,"bold"),
        command=lambda: navigate_to(liked_page)
    ).place(x=160, y=340)

    tk.Button(
        home_page_frame,
        text="Dodaj utwór",
        bg=purple_color,
        fg="white",
        bd=0,
        font=("Calibri", 12,"bold"),
        command=lambda: navigate_to(create_page)
    ).place(x=260, y=340)

    home_page_frame.pack(fill=tk.BOTH, expand=True)

def library_page():
    library_page_frame = tk.Frame(page_frame, bg=root_color)
    
    query = "SELECT album_id, title FROM albums WHERE user_id = %s"
    mycur.execute(query, (user_id,))
    albums = mycur.fetchall()

    x = 100
    y = 100
    spacing = 200
  
    for album in albums:
        album_id, title = album

        album_frame = tk.Frame(library_page_frame, height=200, width=150, bg=root_color , relief="solid", bd=1, 
                               highlightbackground="gray", highlightthickness=1)
        album_frame.place(x=x, y=y)

        default_img = PhotoImage(file="Img/wave.png")
        album_label = tk.Label(album_frame, image=default_img, bg=root_color)
        album_label.image = default_img
        album_label.pack(pady=10)

        title_label = tk.Label(album_frame, text=title, bg=root_color, fg="white", font=("Arial", 12, "bold"))
        title_label.pack(pady=5)

        view_songs_button = tk.Button(album_frame, text="Pokaż piosenki", bg=root_color,bd=0, fg='#D04BCB',
                                      command=lambda a_id=album_id, a_title=title: view_songs(a_id, a_title))
        view_songs_button.pack(pady=5)

        delete_album_button = tk.Button(album_frame, text="Usuń album", bg=root_color, bd=0, fg='#FF4B4B',
                                         command=lambda a_id=album_id, a_frame=album_frame: delete_album(a_id, a_frame))
        delete_album_button.pack(pady=5)

        x += spacing
        if x > 700:
            x = 100
            y += 300

    add_album_frame = tk.Frame(library_page_frame, height=200, width=150, bg=root_color, relief="solid", bd=1, 
                               highlightbackground="gray", highlightthickness=1)
    add_album_frame.place(x=x, y=y)

    add_icon = PhotoImage(file="Img/add.png")  # Ikonka do dodawania
    add_button = tk.Button(add_album_frame, image=add_icon, bg=root_color, bd=0, command=lambda: add_album_form(library_page_frame))
    add_button.image = add_icon
    add_button.pack(pady=50)

    library_page_frame.pack(fill=tk.BOTH, expand=True)

def delete_album(album_id, album_frame):
    response = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć ten album?")
    if response:
        try:
            mycur.execute("DELETE FROM songs WHERE album_id = %s", (album_id,))
            mycur.execute("DELETE FROM albums WHERE album_id = %s", (album_id,))
            connection.commit()

            album_frame.destroy()

            messagebox.showinfo("Sukces", "Album został usunięty!")
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Błąd", f"Wystąpił problem podczas usuwania albumu: {str(e)}")


def add_album_form(parent_frame):
    add_window = tk.Toplevel(parent_frame)
    add_window.title("Dodaj album")
    add_window.geometry("400x200")
    add_window.config(bg=root_color)

    tk.Label(add_window, text="Tytuł albumu:", bg=root_color, fg="white").place(x=50, y=50)
    album_title_entry = tk.Entry(add_window, width=30)
    album_title_entry.place(x=150, y=50)

    def save_album():
        title = album_title_entry.get()
        
        if title:
            query = "INSERT INTO albums (title, user_id) VALUES (%s, %s)"
            mycur.execute(query, (title, user_id))
            connection.commit()
            messagebox.showinfo("Sukces", "Album został dodany!")
            add_window.destroy()
            create_page()
        else:
            messagebox.showerror("Błąd", "Tytuł albumu jest wymagany!")

    tk.Button(add_window, text="Zapisz", bg=purple_color,bd=0,
                font=("Calibri", 12,"bold"), fg="white", command=save_album).place(x=150, y=100)

    add_window.mainloop()

def view_songs(album_id, album_title):
    songs_window = tk.Toplevel()
    songs_window.title(f"Piosenki w albumie: {album_title}")
    songs_window.geometry("400x300")
    songs_window.config(bg=root_color)

    query = """
        SELECT s.song_id, s.title, a.name AS artist_name
        FROM songs s
        JOIN artists a ON s.artist_id = a.artist_id
        WHERE s.album_id = %s
    """
    mycur.execute(query, (album_id,))
    songs = mycur.fetchall()

    tk.Label(songs_window, text=f"Piosenki w albumie: {album_title}", bg=root_color, fg="white",
             font=("Arial", 14, "bold")).pack(pady=10)

    if songs:
        for song_id, song_title, artist_name in songs:
            song_frame = tk.Frame(songs_window, bg=root_color)
            song_frame.pack(fill="x", padx=10, pady=5)

            tk.Label(song_frame, text=f"{song_title} - {artist_name}", bg=root_color, fg="white",
                     font=("Arial", 12)).pack(side="left", padx=10)

            def delete_song(song_id, album_id, song_frame):
                try:
                    # Ustaw album_id na NULL, aby odłączyć piosenkę od albumu
                    mycur.execute("UPDATE songs SET album_id = NULL WHERE song_id = %s AND album_id = %s", (song_id, album_id))
                    connection.commit()

                    song_frame.destroy()
                    messagebox.showinfo("Sukces", "Piosenka została usunięta z albumu!")
                except Exception as e:
                    connection.rollback()
                    messagebox.showerror("Błąd", f"Nie udało się usunąć piosenki z albumu: {str(e)}")

            delete_button = tk.Button(song_frame, text="Usuń", bg=purple_color, bd=0, font=("Calibri", 12, "bold"),
                                       fg="white",
                                       command=lambda song_id=song_id, song_frame=song_frame: delete_song(song_id, album_id, song_frame))
            delete_button.pack(side="right")
    else:
        tk.Label(songs_window, text="Brak piosenek w tym albumie.", bg=root_color, fg="white",
                 font=("Arial", 12)).pack(pady=10)

    tk.Button(songs_window, text="Zamknij", bg=purple_color, bd=0, font=("Calibri", 12, "bold"),
              fg="white", command=songs_window.destroy).pack(pady=10)

    
def browse_page():
    query = """
        SELECT s.type
        FROM likes l
        JOIN songs s ON l.song_id = s.song_id
        WHERE l.user_id = %s
        GROUP BY s.type
        ORDER BY COUNT(*) DESC
        LIMIT 1;
    """
    mycur.execute(query, (user_id,))
    result = mycur.fetchone()

    if result:
        most_liked_type = result[0]

        query2 = """
            SELECT songs.song_id, songs.title, artists.name
            FROM songs
            INNER JOIN artists ON songs.artist_id = artists.artist_id
            WHERE songs.type = %s
            AND songs.song_id NOT IN (SELECT song_id FROM likes WHERE user_id = %s)
            LIMIT 5;
        """
        mycur.execute(query2, (most_liked_type, user_id))
        songs_to_show = mycur.fetchall()
    else:
        songs_to_show = []

    browse_page_frame = tk.Frame(page_frame, bg=root_color)
    browse_page_frame.pack(fill=tk.BOTH, expand=True)

    tk.Label(browse_page_frame, text="Polecane dla Ciebie", font=('arial', 24), bg=root_color, fg="white").place(x=100, y=100)

    if songs_to_show:
        x = 100
        y = 175

        for song in songs_to_show:
            song_id, title, artist = song
            show_song(page=browse_page_frame, x=x, y=y, song_title=title, artist_name=artist, song_id=song_id, user_id=user_id)
            x += 200
    else:
        tk.Label(browse_page_frame, text="Brak piosenek do wyświetlenia.", font=('arial', 16), bg=root_color, fg="white").pack(pady=20)

def create_page():
    create_page_frame = tk.Frame(page_frame, bg=root_color)
    create_page_frame.pack(fill=tk.BOTH, expand=True)

    header = tk.Label(create_page_frame, text="Dodaj nowy utwór", font=("Arial", 20), bg=root_color, fg="white")
    header.place(x=100, y=50)

    header2 = tk.Label(create_page_frame, text="Dodaj nowego artyste", font=("Arial", 20), bg=root_color, fg="white")
    header2.place(x=550, y=50)

    tk.Label(create_page_frame, text="Tytuł utworu:", bg=root_color, fg="white").place(x=100, y=100)
    song_title_entry = tk.Entry(create_page_frame, width=40)
    song_title_entry.place(x=250, y=100)

    query_albums = "SELECT album_id, title FROM albums WHERE user_id = %s"
    mycur.execute(query_albums, (user_id,))
    albums = mycur.fetchall()

    album_options = [("Brak", None)] + [(title, album_id) for album_id, title in albums]

    tk.Label(create_page_frame, text="Album:", bg=root_color, fg="white").place(x=100, y=150)
    album_combobox = ttk.Combobox(create_page_frame, width=37, state="readonly")
    album_combobox.place(x=250, y=150)

    album_titles = [option[0] for option in album_options]
    album_combobox['values'] = album_titles
    album_combobox.current(0)

    query_artists = "SELECT artist_id, name FROM artists"
    mycur.execute(query_artists)
    artists = mycur.fetchall()

    artist_options = [("Wybierz artystę", None)] + [(name, artist_id) for artist_id, name in artists]

    tk.Label(create_page_frame, text="Artysta:", bg=root_color, fg="white").place(x=100, y=200)
    artist_combobox = ttk.Combobox(create_page_frame, width=37, state="readonly")
    artist_combobox.place(x=250, y=200)

    artist_names = [option[0] for option in artist_options]
    artist_combobox['values'] = artist_names
    artist_combobox.current(0)

    tk.Label(create_page_frame, text="Dodaj nowego artystę:", bg=root_color, fg="white").place(x=550, y=100)
    artist_name_entry = tk.Entry(create_page_frame, width=40)
    artist_name_entry.place(x=700, y=100)

    def add_new_artist():
        new_artist_name = artist_name_entry.get().strip()
        if new_artist_name:
            try:
                query = "INSERT INTO artists (name) VALUES (%s)"
                mycur.execute(query, (new_artist_name,))
                connection.commit()
                messagebox.showinfo("Sukces", f"Artysta '{new_artist_name}' został dodany!")
                artist_combobox['values'] = [option[0] for option in artist_options] + [new_artist_name]
                artist_combobox.current(len(artist_combobox['values']) - 1)
                artist_name_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się dodać artysty: {str(e)}")
        else:
            messagebox.showerror("Błąd", "Wprowadź nazwisko artysty!")

    add_artist_button = tk.Button(create_page_frame, text="Dodaj artystę", bg=purple_color,
        fg="white",
        bd=0,
        font=("Calibri", 12, "bold"), command=add_new_artist)
    add_artist_button.place(x=700, y=140)

    tk.Label(create_page_frame, text="Typ piosenki:", bg=root_color, fg="white").place(x=100, y=250)
    song_types = ["rock", "pop", "classic", "hip-hop", "techno", "jazz"]
    type_combobox = ttk.Combobox(create_page_frame, width=37, state="readonly")
    type_combobox.place(x=250, y=250)
    type_combobox['values'] = song_types
    type_combobox.current(0)

    def save_song():
        song_title = song_title_entry.get()
        selected_album_index = album_combobox.current()
        selected_artist_index = artist_combobox.current()
        selected_type_index = type_combobox.current()

        album_id = album_options[selected_album_index][1]
        artist_id = artist_options[selected_artist_index][1]
        song_type = song_types[selected_type_index]

        if not song_title or artist_id is None:
            messagebox.showerror("Błąd", "Tytuł utworu, artysta i typ piosenki są wymagane!")
            return

        try:
            query = "INSERT INTO songs (title, artist_id, album_id, type) VALUES (%s, %s, %s, %s)"
            mycur.execute(query, (song_title, artist_id, album_id, song_type))
            connection.commit()
            messagebox.showinfo("Sukces", "Utwór został dodany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się dodać utworu: {str(e)}")

        song_title_entry.delete(0, tk.END)
        album_combobox.current(0)
        artist_combobox.current(0)
        type_combobox.current(0)

    save_button = tk.Button(create_page_frame, text="Zapisz utwór", fg="white", bg=purple_color,
        bd=0,
        font=("Calibri", 12, "bold"), command=save_song)
    save_button.place(x=250, y=300)

def liked_page():
    liked_page_frame = tk.Frame(page_frame, bg=root_color)

    query = """
        SELECT s.song_id, s.title, a.name AS artist_name
        FROM likes l
        JOIN songs s ON l.song_id = s.song_id
        JOIN artists a ON s.artist_id = a.artist_id
        WHERE l.user_id = %s
    """
    mycur.execute(query, (user_id,))
    result = mycur.fetchall()

    max_songs_per_page = 6

    def display_songs(page_frame, page=0):
        for widget in page_frame.winfo_children():
            widget.destroy()

        lb1 = tk.Label(liked_page_frame, text="Polubione utwory", font=("Arial", 20), bg=root_color, fg="white")
        lb1.place(x=100, y=125)

        start_index = page * max_songs_per_page
        end_index = start_index + max_songs_per_page
        songs_to_display = result[start_index:end_index]

        x = 100
        y = 175

        for song_id, song_title, artist_name in songs_to_display:
            show_song(page=liked_page_frame, x=x, y=y, song_title=song_title, artist_name=artist_name, song_id=song_id, user_id=user_id)
            x += 200


        if page > 0:
            prev_button = tk.Button(
                liked_page_frame,
                text="Poprzednia strona",
                command=lambda: display_songs(liked_page_frame, page-1),
                bg=purple_color,
                bd=0,
                font=("Calibri", 12,"bold"),
                fg="white"
            )
            prev_button.place(x=200, y=450)

        if end_index < len(result):
            next_button = tk.Button(
                liked_page_frame,
                text="Następna strona",
                command=lambda: display_songs(liked_page_frame, page+1),
                bg=purple_color,
                bd=0,
                font=("Calibri", 12,"bold"),
                fg="white"
            )
            next_button.place(x=300, y=450)

    display_songs(liked_page_frame, page=0)

    liked_page_frame.pack(fill=tk.BOTH, expand=True)


def update_combobox(*args):
        search_text = search_var.get()
        if search_text:
            query = """
            SELECT songs.title 
            FROM songs 
            WHERE songs.title LIKE %s
            """
            mycur.execute(query, (f"%{search_text}%",))
            result = mycur.fetchall()

            song_list = [row[0] for row in result]
            search_combobox['values'] = song_list
        else:
            search_combobox['values'] = []

def on_select(event=None):
    selected_song = search_var.get()
    if selected_song:
        mycur.execute("""
        SELECT songs.song_id, songs.title, artists.name 
        FROM songs 
        INNER JOIN artists ON songs.artist_id = artists.artist_id 
        WHERE songs.title = %s
        """, (selected_song,))
        result = mycur.fetchone()
        if result:
            song_id, song_title, artist_name = result

            new_window = tk.Toplevel()
            new_window.title("Szczegóły utworu")
            new_window.geometry("300x300")
            new_window.configure(bg=root_color)

            show_song(page=new_window, x=10, y=10, song_title=song_title, artist_name=artist_name, song_id=song_id, user_id=user_id)
        else:
            messagebox.showerror("Błąd", "Nie znaleziono utworu.")

########################################################################## ELEMENTY W OKNIE ##########################################################################

root = tk.Tk()
root.geometry("900x600")
root.config(bg=root_color)
root.minsize(900, 600)
root.wm_iconbitmap('Img/skyl.ico')
root.wm_title('Skyline Music City')

image_side_bar = tk.PhotoImage(file='Img/icon.png')
image_home = tk.PhotoImage(file='Img/home.png')
image_library= tk.PhotoImage(file='Img/library.png')
image_browse=tk.PhotoImage(file='Img/browse.png')
image_create=tk.PhotoImage(file='Img/create.png')
image_liked=tk.PhotoImage(file='Img/liked.png')
image_info=tk.PhotoImage(file=('Img/info.png'))
image_close=tk.PhotoImage(file='Img/close.png')

page_frame=tk.Frame(root)
side_bar = tk.Frame(root, bg=side_bar_color, width=45)
top_bar = tk.Frame(root, bg=top_bar_color, height=45)

home_page_lb=tk.Label(side_bar, text='Home', bg=side_bar_color, fg='white', font=('Bold', 15))
library_page_lb=tk.Label(side_bar, text='Library', bg=side_bar_color, fg='white', font=('Bold', 15))
browse_page_lb=tk.Label(side_bar, text='Browse', bg=side_bar_color, fg='white', font=('Bold', 15))
create_page_lb=tk.Label(side_bar, text='Create', bg=side_bar_color, fg='white', font=('Bold', 15))
liked_page_lb=tk.Label(side_bar, text='Liked', bg=side_bar_color, fg='white', font=('Bold', 15))

page_frame.place(relwidth=1.0, relheight=1.0, x=200)
home_page()

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

search_label = tk.Label(top_bar, text="Szukaj:", bg=top_bar_color, fg="white", font=('Arial', 12), pady=6)
search_label.place(x=10, y=2, height=30)

search_var = tk.StringVar()
search_var.trace("w", update_combobox)

search_combobox = ttk.Combobox(top_bar, textvariable=search_var)
search_combobox.place(x=70, y=2, height=30, width=400)

search_combobox.bind("<<ComboboxSelected>>", on_select)

user=tk.Label(top_bar,bg=top_bar_color, text=user_name, fg='white', font=('Arail', 15)).pack(side=tk.RIGHT, padx=(10,60))

root.mainloop()