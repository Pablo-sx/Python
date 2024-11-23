import tkinter as tk

root=tk.Tk()
root.geometry("800x600")

images_side_bar=tk.PhotoImage(file='Img/icon.png')

side_menu_frame= tk.Frame(root, bg="#383838", width="45")
icon_btn=tk.Button(side_menu_frame, bg="#383838", image=images_side_bar, bd=0)


side_menu_frame.pack(side=tk.LEFT, fill="y", pady=3, padx=3)
icon_btn.place(x=4, y=4)

root.mainloop()