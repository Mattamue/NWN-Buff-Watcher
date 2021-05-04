from tkinter import *
import time

root = Tk()

# Creating a Label widget
myLabel1 = Label(root, text = "Hello World!")
myLabel2 = Label(root, text = "My name is John Elder")

# Putting the text into a grid rather than .pack
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=5)

# This is the main loop that keeps the window "running"
root.mainloop()

print("Stuff happens after the mainloop.")

time.sleep(10)

myLabel2 = Label(root, text = "My name is fart poop")

myLabel2.grid(row=1, column=5)