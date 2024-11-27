import tkinter as tk
from tkinter import ttk


class SrotifyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Srotify")
        self.geometry("800x600")
        self.config(bg="#181818")
        self.minsize(800, 400)

        self.frames = {}  # Słownik przechowujący różne widoki
        self.container = tk.Frame(self, bg="#181818")
        self.container.pack(fill="both", expand=True)

        # Dodanie wszystkich widoków
        for F in (HomePage, BrowsePage, LibraryPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)  # Ustawienie początkowego widoku

    def show_frame(self, page_class):
        """Przełączanie widoków."""
        frame = self.frames[page_class]
        frame.tkraise()


class Sidebar(tk.Frame):
    """Menu boczne wspólne dla wszystkich widoków."""
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black", width=200)
        self.controller = controller

        buttons = [
            ("Home", HomePage),
            ("Browse", BrowsePage),
            ("Your Library", LibraryPage),
        ]

        for button_text, page in buttons:
            button = tk.Button(
                self, text=button_text, bg="black", fg="white",
                font=("Arial", 10), relief="flat",
                command=lambda p=page: controller.show_frame(p)
            )
            button.pack(fill="x", pady=5, padx=10)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#181818")
        self.controller = controller

        # Menu boczne
        sidebar = Sidebar(self, controller)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        # Górny pasek
        top_bar = tk.Frame(self, bg="#121212", height=50)
        top_bar.grid(row=0, column=1, sticky="ew")
        
        search_label = tk.Label(top_bar, text="Search:", bg="#78DE78", fg="black")
        search_label.pack(side="left", padx=10)
        
        search_entry = tk.Entry(top_bar, width=50, font=("Arial", 12))
        search_entry.pack(side="left", padx=5, pady=10)
        
        search_button = tk.Button(top_bar, text="Go!", bg="#27D75C", fg="black", command=lambda: print(search_entry.get()))
        search_button.pack(side="left", padx=10)

        # Główna zawartość
        main_content = tk.Frame(self, bg="#181818")
        main_content.grid(row=1, column=1, sticky="nsew")

        song_label = tk.Label(
            main_content, text="Twoj stary w betoniarce", bg="#181818", fg="white", font=("Arial", 10)
        )
        song_label.pack(anchor="w", padx=20, pady=2)


class BrowsePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#181818")
        self.controller = controller

        sidebar = Sidebar(self, controller)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        content = tk.Label(self, text="Browse Page", bg="#181818", fg="white", font=("Arial", 16))
        content.grid(row=0, column=1, pady=20, padx=20)


class LibraryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#181818")
        self.controller = controller

        sidebar = Sidebar(self, controller)
        sidebar.grid(row=0, column=0, rowspan=2, sticky="ns")

        content = tk.Label(self, text="Your Library", bg="#181818", fg="white", font=("Arial", 16))
        content.grid(row=0, column=1, pady=20, padx=20)


if __name__ == "__main__":
    app = SrotifyApp()
    app.mainloop()
