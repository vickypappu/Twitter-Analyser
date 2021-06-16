import tkinter as tk
from tkinter import ttk, Button, messagebox

# Creating tkinter window
window = tk.Tk()

# Combobox creation
ids = tk.StringVar()
userlist = ttk.Combobox(window, width = 27, textvariable = ids)
userlist['values'] = ('Jan','Feb')
userlist.grid(column = 1, row = 5)

def print1():
    if ids.get() == "":
        messagebox.showerror("Error", "Please enter an twitter ID....")

        return
    print('Running ', ids.get())
    
Button(window, text="print", width=12, height=1, font="none 15 bold", command=print1) .grid(column = 1, row = 6) #button exit





window.mainloop()
