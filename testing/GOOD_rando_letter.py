"""
GOOD ONE! Lets click and move around and keeps running

"""

import tkinter as tk
import random

def update():
    l.config(text=str(random.random()))
    root.after(1000, update)

root = tk.Tk()
l = tk.Label(text='0')
l.pack()
root.after(1000, update)
root.attributes("-topmost", True) # makes the window float on top, seems to work perfectly
root.mainloop()