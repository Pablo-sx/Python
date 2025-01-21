from PIL import Image, ImageTk, ImageFilter
import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Połączenie z bazą danych MySQL
connection = mysql.connector.connect(host="localhost", user="root", password="", database="projekt")
mycur = connection.cursor()

def loguj():
    """Funkcja logowania"""
    name = name_entry.get()
    pasw = pass_entry.get()

    query = "SELECT user_id FROM users WHERE name = %s AND pass = %s"
    values = (name, pasw)
    
    mycur.execute(query, values)
    result = mycur.fetchone()
        
    if result:
        id = result[0]
        root.destroy()
        subprocess.run(["py", "main.py", str(id)])
    else:
        messagebox.showerror("Błąd", "Niepoprawne dane")

def open_register_window():
    """Funkcja otwierająca okno rejestracji"""
    global reg_name_entry, reg_pass_entry
    reg_window = tk.Toplevel(root)
    reg_window.geometry("400x300")
    reg_window.title("Rejestracja")
    reg_window.config(bg="#282828")

    reg_label = tk.Label(reg_window, text="Zarejestruj się", font=("Arial", 16, "bold"), fg="White", bg="#282828")
    reg_label.pack(pady=10)

    reg_name_label = tk.Label(reg_window, text="Nazwa użytkownika:", fg="White", bg="#282828")
    reg_name_label.pack(pady=5)
    reg_name_entry = tk.Entry(reg_window, width=30)
    reg_name_entry.pack(pady=5)

    reg_pass_label = tk.Label(reg_window, text="Hasło:", fg="White", bg="#282828")
    reg_pass_label.pack(pady=5)
    reg_pass_entry = tk.Entry(reg_window, width=30, show="*")
    reg_pass_entry.pack(pady=5)

    reg_button = tk.Button(reg_window, text="Zarejestruj", command=rejestruj, bg="#5D3FD3", fg="White", width=15)
    reg_button.pack(pady=10)

def rejestruj():
    """Funkcja rejestracji"""
    name = reg_name_entry.get()
    pasw = reg_pass_entry.get()

    query_check = "SELECT * FROM users WHERE name = %s"
    mycur.execute(query_check, (name,))
    if mycur.fetchone():
        messagebox.showerror("Błąd", "Użytkownik istnieje")
        return

    query_insert = "INSERT INTO users (name, pass) VALUES (%s, %s)"
    mycur.execute(query_insert, (name, pasw))
    connection.commit()

    messagebox.showinfo("Sukces", "Rejestracja zakończona sukcesem!")
    reg_window.destroy()

# Główne okno aplikacji
root = tk.Tk()
root.geometry("800x600")
root.title("Skyline Music City")
root.resizable(False, False)

# Tło jako PNG z nałożeniem blura
image_path = r"C:\Users\Kwol\Desktop\python app\san.png"  # Zmień na odpowiednią ścieżkę
bg_image = Image.open(image_path)
bg_image = bg_image.resize((800, 600))  # Dopasowanie rozmiaru tła
bg_image = bg_image.filter(ImageFilter.GaussianBlur(5))  # Nałożenie blura (15%)
bg_image_tk = ImageTk.PhotoImage(bg_image)

# Canvas do wyświetlenia tła
canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

# Ekran logowania (ciemniejsze fioletowe okno z paddingiem 20 px)
login_frame = tk.Frame(root, bg="#320e6b", width=590, height=440, padx=20, pady=20)
login_frame.place(relx=0.5, rely=0.5, anchor="center")

# Nagłówek "Skyline Music City" w oknie logowania
login_label = tk.Label(login_frame, text="Skyline Music City", font=("Arial", 18, "bold"), bg="#320e6b", fg="White",)
login_label.pack(pady=15)

# Pole tekstowe do logowania
name_label = tk.Label(login_frame, text="Login", font=("Arial", 12), bg="#320e6b", fg="White")
name_label.pack(pady=5)
name_entry = tk.Entry(login_frame, font=("Arial", 10), width=22)
name_entry.pack()

# Pole tekstowe do hasła
pass_label = tk.Label(login_frame, text="Hasło", font=("Arial", 12), bg="#320e6b", fg="White")
pass_label.pack(pady=5)
pass_entry = tk.Entry(login_frame, font=("Arial", 10), width=22, show="*")
pass_entry.pack()

# Przycisk "Login"
login_button = tk.Button(login_frame, text="Zaloguj się", command=loguj, font=("Arial", 12, "bold"), bg="#4CAF50", fg="White", width=15)
login_button.pack(pady=20)

# Tekst "Nie masz konta? Zarejestruj się"
footer_frame = tk.Frame(login_frame, bg="#320e6b")
footer_frame.pack(pady=10)

no_account_label = tk.Label(footer_frame, text="Nie masz konta?", font=("Arial", 10), bg="#320e6b", fg="White")
no_account_label.pack(side="left")

register_link = tk.Label(footer_frame, text="Zarejestruj się", font=("Arial", 10, "underline"), bg="#320e6b", fg="#FFFFFF", cursor="hand2")
register_link.pack(side="left", padx=5)
register_link.bind("<Button-1>", lambda e: open_register_window())

root.mainloop()