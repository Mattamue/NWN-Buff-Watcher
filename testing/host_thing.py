"""
Good, lets you click and move around the window while its running

"""


# from tkinter import * # don't use star imports they flood the namespace
import os
import tkinter
 
UPDATE_RATE = 1000
 
class Application(tkinter.Frame):
    """ GUI """
 
    def __init__(self, master):
        """ Initialize the Frame"""
        tkinter.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.updater()
 
    def create_widgets(self):
        """Create button. """
#         import os # import at top
#         import subprocess # doing nothing
        # Router
        self.button1 = tkinter.Button(self)
        self.button1["text"] = "Router"
        self.button1["fg"] = "white"
        self.button1.grid(row=0, column=5, rowspan=1, columnspan=2)
 
    def update_button1(self):
        # Ping
        hostname = "192.168.0.1"
        response = os.system("ping -n 1 " + hostname)
        # response
        if response == 0:
            self.button1["bg"] = "green"
        else:
            self.button1["bg"] = "red"
 
    def updater(self):
        self.update_button1()
        self.after(UPDATE_RATE, self.updater)
 
root = tkinter.Tk()
root.title("monitor")
root.geometry("500x500")
app = Application(root)
root.mainloop()