import tkinter as tki
from tkinter import *
from PIL import ImageTk, Image

class App(object):

    def __init__(self):
        self.root = tki.Tk()
        self.root.wm_title("NWN buff watcher")

        # Create a list of the Frames in the order they were created
        frames = []
        j = 0
        for i in range(1,5):
            frame_test = tki.LabelFrame(self.root, borderwidth=1, text="Frame")
            frame_test.grid(row = 0, column = j)
            frame_test.x = "fart" # creating an attribute on the fly
            label_test = tki.Label(frame_test, text=f"j: {j}")
            label_test.pack()
            image_test_image = ImageTk.PhotoImage(Image.open("arelith_ui\Is_bullstr.png"))
            image_test_label = tki.Label(frame_test, image=image_test_image)
            image_test_label.image_keep = image_test_image # keeping image in memory
            image_test_label.pack()

            # Add the Frame to the list
            frames.append(frame_test)

            # Also, just as an FYI, j = j + 2 can be better written like this
            j += 1

        # To demonstrate
        print(frames)

        # This is the first Frame created
        print(frames[0])

        # testing attributes
        print(str(frames[0].image_types()))

        print(frames[0].x) # calling an attribute created on the fly in the for loop

        print(frames[1].x)



app = App()
app.root.mainloop()