from tkinter import *

root = Tk()

def myClick():
    myLabel = Label(root, text="Look! I clicked a Button!!")
    myLabel.pack()

# define the widget
# myButton = Button(root, text="Click Me!", state=DISABLED) # state example
myButton = Button(root, text="Click Me!", padx=5, pady=50, command=myClick, fg="blue", bg="red") # note note adding () to function when called as what the button does, can use hex color codes
# putting it on screen
myButton.pack()


# This is the main loop that keeps the window "running"
root.mainloop()

