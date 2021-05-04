from tkinter import *

ws = Tk()
ws.title('Messing windowsize')
# ws.config() # nothing... don't know why this was in the example code

window_width = 300
window_height = 400

# ws.geometry(f'{str(window_width)}x{str(window_height)}') # sets the startup window size

# ws.maxsize(350, 450)
# ws.minsize(250, 350)

""" all mean cannot resize
ws.resizable(0, 0)
ws.resizable(False, False)
ws.resizable(width=False, Height=False)
"""

# ws.winfo_screenheight() # Returns screen height in pixels
# ws.winfo_screenmmheight() # Returns screen height in mm
# ws.winfo_screenwidht() # Returns screen width in pixels
# ws.winfo_screenmmwidth() # Returns screen width in mm
print(ws.winfo_screenheight()) # this is the overall resolution of the screen
print(ws.winfo_screenwidth()) # this is the overall resolution of the screen

# ws.attributes('-fullscreen', True) # fullscreen... removes default top bar menus...



label1 = Label(ws, text=f'winfo_reqh/w: "Width", {ws.winfo_reqwidth()},"Height", {ws.winfo_reqheight()}')
label1.pack()

label2 = Label(ws, text=f'winfo_h/w: "Width", {ws.winfo_width()},"Height", {ws.winfo_height()}')
label2.pack()

button1 = Button(ws, text="Print", command=lambda: print(f'winfo_reqh/w: "Width", {ws.winfo_reqwidth()},"Height", {ws.winfo_reqheight()}\nwinfo_h/w: "Width", {ws.winfo_width()},"Height", {ws.winfo_height()}'))
button1.pack()

button2 = Button(ws, text="Update", command=lambda: update_shit)
button2.pack()

def update_shit(): # doesn't work...
    update()
    label1.forget()
    label1.pack()
    label2.forget()

ws.mainloop()