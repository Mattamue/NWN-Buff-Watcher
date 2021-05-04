import tkinter as tk
from tkinter import ttk, Menu
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfile
import time

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.grid(row=0, column=0)

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.grid(row=1, column=0)

        # show the frame on the container
        # without this, the "main" window is empty as that is just a plan
        # tkinter window without anything in it, and you shouldn't make more than
        # one Tk class, making Frame (or Toplevel) classes instead allows us to have
        # more than one window if we want in the future
        self.pack()

        # making another frame inside the frame... with a label
        self.frame1 = tk.LabelFrame(self, text="Frame within the \"frame\"")
        self.frame1.grid(row=2, column=0)
        self.button_frame = ttk.Label(self.frame1, text="I'm a label.")
        self.button_frame.grid(row=3, column=0)

        # another button
        self.button1 = ttk.Button(self, text="Testing", command=self.test_func_in_app)
        self.button1.grid(sticky="NW", row=4, column=0)

        self.name_stringvar = tk.StringVar() # setting in constructor so doesn't error when opening file when not set

    def test_func_in_app(self):
        print("Clicked button.")
        print(f"self.name_stringvar.get(): {self.name_stringvar.get()}")





    def character_name(self):
        self.name_entry_window = tk.Toplevel(self)
        self.name_entry_window.title("Enter Character Name")
        self.name_entry_window.geometry('300x50')
        self.name_stringvar = tk.StringVar()
        self.name_entry = tk.Entry(self.name_entry_window, width = 30, textvariable = self.name_stringvar)
        self.name_entry.pack()
        self.button_enter = tk.Button(self.name_entry_window, text="OK", command=lambda: self.name_entry_window.destroy())
        self.button_enter.pack()


    def open_file(self): 
        self.logfile = askopenfile(mode ='r', filetypes =[('Logs', '*.txt'), ('Any', '*.*')]) 
        self.logfile_name = self.logfile.name
        open(self.logfile_name, 'r')
        self.logfile.seek(0, 2)
        self.after(100, self.log_looping)

    def log_looping(self):
        """ Main "loop" of the program, calls every 1 second (if after is 1000)
        and does stuff
        """
        buffs = self.logfile.readlines()
        print(buffs) # debugging
        if self.name_stringvar.get() + " uses Potion of Endurance" in str(buffs):
            print("Bear fired.")
            
        self.after(1000, self.log_looping)

    def button_clicked(self):

        showinfo(title='Information',
                message='Hello, Tkinter!')



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('NWN Buff Watcher')
        self.geometry('300x50')
        self.attributes("-topmost", True)

        self.option_add('*tearOff', False) # docs said something about this... not sure what it changes

        # menu for file > open
        self.menubar = Menu(self)
        self.config(menu=self.menubar)


        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Name', command=lambda: main_frame.character_name())
        self.file_menu.add_command(label='Open...', command=lambda: main_frame.open_file())
        # self.file_menu.add_command(label='Close')
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # self.help_menu = Menu(self.menubar, tearoff=0)
        # self.help_menu.add_command(label='Welcome')
        # self.help_menu.add_command(label='About...')
        # self.menubar.add_cascade(label="Help", menu=self.help_menu)


if __name__ == "__main__":
    app = App()
    main_frame = MainFrame(app)
    app.mainloop()