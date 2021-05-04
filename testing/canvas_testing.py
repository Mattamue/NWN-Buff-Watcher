import tkinter as tk

root = tk.Tk()

w = tk.Canvas(root, width =200, height = 100)
w.pack()

w.create_line(0, 0, 200, 100, fill = "red", width = 6)
w.create_line(200, 0, 0, 100, fill = "red", width = 6)
w.create_rectangle(40, 20, 160, 80, fill = "blue")
w.create_rectangle(65, 35, 135, 65, fill = "white")

w.create_text(100, 50, text = "Tkinter")

def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        w.create_oval(x1, y1, x2, y2, fill = "red")

w.bind("<B1-Motion>", paint)

tk.Label(root, text = "tkinter paint").pack(side = "bottom")

root.mainloop()