import tkinter as tk
from tkinter import ttk


def return_pressed(event):
    print('Return key pressed.')


root = tk.Tk()

btn = ttk.Button(root, text='Save')
btn.bind('<Return>', return_pressed)


btn.focus()
btn.pack(expand=True)

root.mainloop()