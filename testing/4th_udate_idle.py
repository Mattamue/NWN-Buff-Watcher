from tkinter import *
from time import sleep

# making the main window
root = Tk()


# setting up a text variable to change
var = StringVar()
var.set('Hello')
l = Label(root, textvariable = var)
l.pack()


def flipper():
    for i in range(6):
        var.after(1).set(i)
        root.update_idletasks()


# making a button, it calls the function
my_button = Button(root, text = "Start flipper", command = flipper)
my_button.pack()



root.mainloop()

