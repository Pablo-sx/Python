import subprocess
import tkinter as tk
from tkinter import messagebox
import mysql.connector

connection = mysql.connector.connect(host="localhost", user="root", password="", database="projekt")
mycur = connection.cursor()

def loguj():
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

def rejestruj():
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

    reg_window.destroy()

root_color = "#282828"
root = tk.Tk()
root.geometry("800x600")
root.minsize(800, 600)
root.maxsize(800, 600)
root.config(bg=root_color)

lb_sq = tk.Label(root, width=43, height=20, bg="#181818").place(x=180, y=100)

login_lb = tk.Label(root, text="Zaloguj się ;3", font=("Arial,12,0"), fg="White", bg=root_color)
login_lb.place(x=250, y=150)

name_entry = tk.Entry(root, width=30)
name_entry.place(x=250, y=200)

pass_entry = tk.Entry(root, width=30, show="*")
pass_entry.place(x=250, y=235)

login_but = tk.Button(root, text="Loguj", command=loguj)
login_but.place(x=320, y=270)

def open_register_window():
    global reg_window, reg_name_entry, reg_pass_entry
    reg_window = tk.Toplevel(root)
    reg_window.geometry("400x300")
    reg_window.title("Rejestracja")
    reg_window.config(bg=root_color)

    reg_label = tk.Label(reg_window, text="Zarejestruj się", font=("Arial,12,0"), fg="White", bg=root_color)
    reg_label.pack(pady=10)

    reg_name_label = tk.Label(reg_window, text="Nazwa użytkownika:", fg="White", bg=root_color)
    reg_name_label.pack(pady=5)
    reg_name_entry = tk.Entry(reg_window, width=30)
    reg_name_entry.pack(pady=5)

    reg_pass_label = tk.Label(reg_window, text="Hasło:", fg="White", bg=root_color)
    reg_pass_label.pack(pady=5)
    reg_pass_entry = tk.Entry(reg_window, width=30, show="*")
    reg_pass_entry.pack(pady=5)

    reg_button = tk.Button(reg_window, text="Zarejestruj", command=rejestruj)
    reg_button.pack(pady=10)

register_but = tk.Button(root, text="Zarejestruj się", command=open_register_window)
register_but.place(x=300, y=310)

root.mainloop()
