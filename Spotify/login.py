import tkinter as tk
from tkinter import messagebox
import mysql.connector

connection=mysql.connector.connect(host="localhost", user="root", password="", database="test")
mycur=connection.cursor()

def loguj():
    # Pobranie wartości z pól tekstowych
    name = name_entry.get()
    pasw = pass_entry.get()
    
    # Poprawne zapytanie SQL z placeholderami
    query = "SELECT id FROM test WHERE imie = %s AND nazwisko = %s"
    values = (name, pasw)  # Tuple z wartościami
    
    try:
        mycur.execute(query, values)
        result = mycur.fetchall()  # Pobranie wyników zapytania
        print("Wynik zapytania:", result)
    except Exception as e:
        print("Wystąpił błąd podczas wykonywania zapytania:", e)


root_color = "#282828"

root = tk.Tk()
root.geometry("800x600")
root.minsize(800, 600)
root.maxsize(800, 600)
root.config(bg=root_color)

lb_sq=tk.Label(root, width=43, height=20, bg="#181818").place(x=180, y=100)

login_lb = tk.Label(root, text="Zaloguj sie ;3", font=("Arial,12,0"), fg="White", bg=root_color)
login_lb.place(x=250, y=150)

name_entry = tk.Entry(root, width=30)
name_entry.place(x=250, y=200)

pass_entry = tk.Entry(root, width=30)
pass_entry.place(x=250, y=235)

login_but = tk.Button(root, text="Loguj", command=loguj)
login_but.place(x=320, y=270)

root.mainloop()