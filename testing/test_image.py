from tkinter import *      
root = Tk()      
canvas = Canvas(root)      
canvas.pack()      
img = PhotoImage(file="arelith_ui\Is_bullstr.gif")      
canvas.create_image(0, 0, anchor=NW, image=img)      
mainloop()   

