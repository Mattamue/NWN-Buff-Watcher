"""
creates a constant line while held down...
"""

from tkinter import *
from tkinter import ttk

draw_id = 0

def savePosn(event):
    global lastx, lasty
    lastx, lasty = event.x, event.y

def addLine(event):
    global draw_id
    draw_id = canvas.create_line((lastx, lasty, event.x, event.y), fill='red', width=3, stipple='gray75', dash=2, arrow='last')
    savePosn(event)

root = Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

canvas = Canvas(root)
canvas.grid(column=0, row=0, sticky=(N, W, E, S)) # this makes the canvas grow when window is resized...
canvas.bind("<Button-1>", savePosn)
canvas.bind("<B1-Motion>", addLine)

fart_poop = canvas.create_line(10, 10, 200, 50, 90, 150, 50, 80)

canvas.create_line(1000, 1000, 500, 500) # yes you can create stuff "off screen" -- the coordinates are just pixels I think

button1 = ttk.Button(root, text="Just changes last drawn heartbeat item", command=lambda: canvas.itemconfigure(draw_id, fill='blue', width=20))
button1.grid(column=1, row=0, sticky='nsew')

# button2 = ttk.Button(root, text="Change fartpoop", command=lambda: canvas.itemconfigure(fart_poop, fill='blue', width=2 + 1, smooth=True, arrow='both', arrowshape=[10, 20, 5]))
# button2.grid(column=0, row=2)

# b = ttk.Button(canvas, text='Implode!', command=lambda: print("Fart"))
# canvas.create_window(10, 10, anchor='nw', window=b)

"""
^ putting "canvas" in the button instead of root makes the button work in the canvas
"""

root.mainloop()