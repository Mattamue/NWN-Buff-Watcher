"""
Author: Mattamue
Program: buff_watcher_oop.py
Last updated: 05/04/2021

Watches chat log of the Neverwinter Nights video game
and extends the UI by overlaying a window with more
information than is usually in the game
"""

import tkinter as tk
from tkinter import ttk, Menu
from PIL import ImageTk, Image
import time
from tkinter.filedialog import askopenfile
from get_friends_list import friends_list

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.grid(column=0, row=0, sticky='nsew') # loads the main_frame into the parent window, sticky makes the "main" containing frame stretch when the window is resized

        self.columnconfigure(0, weight=1) # allows the main_frame *in its frame* to grow side to side in the column when the window is resized, since it doesn't share with other widgets it gets 100% of the 1 weight
        self.rowconfigure(0, weight=1) # allows the main_frame *in its frame* to grow up and down in the row when the window is resized, since it doesn't share with other widgets it gets 100% of the 1 weight

        self.buffs_list_frames = [] # setting this to be used later

        self.name_stringvar = tk.StringVar() # setting in constructor so doesn't error when opening file when not set

        # frame for the buttons on the right
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(column=1, row=0)

        # resting removes all buffs
        self.rest_button = ttk.Button(self.buttons_frame, text="Rest", command=lambda: self.rest_off_buffs())
        self.rest_button.grid(column=0, row=0, sticky='ew')

        # putting all the "normal" menus into this button to reduce the height of the window since the traditional file menu adds like another 20 pixels of heigth that do nothing
        self.menu_button = ttk.Menubutton(self.buttons_frame, text="Settings")
        self.menu_button.grid(column=0, row=1, sticky='ew')
        self.menu_button.menu = Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu_button.menu
        self.menu_button.menu.add_command(label='Name', command=lambda: main_frame.character_name())
        self.menu_button.menu.add_command(label='Open log...', command=lambda: main_frame.open_file())
        self.menu_button.menu.add_command(label='Friends', command=lambda: main_frame.friends_list_window())
        self.menu_button.menu.add_command(label='Testing', command=lambda: main_frame.testing_buttons())
        self.menu_button.menu.add_separator()
        self.menu_button.menu.add_command(label='Exit', command=lambda: app.destroy())

        # creating the canvas that will be scrollable and have the buff_frame built into it as a window so it'll be scrollable
        self.canvas_test = tk.Canvas(self, height=75, width=500)
        self.canvas_test.grid(column=0, row=0, sticky='nsew')

        # frame outside of the canvas
        self.buff_holding_frame = tk.Frame(self.canvas_test, bd=1, relief='solid')
        self.buff_holding_frame.pack(side="left")

        # canvas "window" inside the canvas, how its called for things like bbox
        self.buff_window_id = self.canvas_test.create_window(500, 0, anchor='ne', window=self.buff_holding_frame)

        # calls the resize function when the window size is adjusted by user
        self.bind('<Configure>', self.resize_set_buff_window)

        # creating the scroll bar for the canvas that'll ultimately allow resizing of the buff_frame by being the container
        self.hsb = tk.Scrollbar(self, orient="horizontal", command=self.canvas_test.xview)
        self.canvas_test.configure(xscrollcommand=self.hsb.set)
        self.hsb.grid(column=0, row=1, sticky='ew')


    def resize_set_buff_window(self, event):
        self.re_size_move = (self.canvas_test.winfo_width() - ((self.canvas_test.bbox(1)[2] - self.canvas_test.bbox(1)[0]))) + self.canvas_test.canvasx(0)
        self.canvas_test.moveto(1, self.re_size_move, 0)
        self.canvas_test.configure(scrollregion=self.canvas_test.bbox("all"))

        # debugging --- getting the buffs to sit at the right and move correctly with window resizes was HARD ^ that small bit of code doesn't reflect everything that was tried
        # print("-" * 30)
        # print(event)
        # print(f"self.canvas_test.coords(1): {self.canvas_test.coords(1)}")
        # print(f"self.canvas_test.bbox(1): {self.canvas_test.bbox(1)}")
        # print(f"self.canvas_test.bbox(1) calc width: {self.canvas_test.bbox(1)[2] - self.canvas_test.bbox(1)[0]}")
        # print(f"canvas_test.winfo_width: {self.canvas_test.winfo_width()}")
        # print(f"re-size move: {self.re_size_move}")
        # print(f"self.canvas_test.canvasx(0): {self.canvas_test.canvasx(0)}") # this was the key to everything, took a while to find, allows me to track the "drift" on the canvas coordinates and the widget window coordinates when the window is resized down
        # print(f"self.canvas_test.xview(): {self.canvas_test.xview()}")
        # print(dir(self.canvas_test))
        # print(f"buff_frame.winfo_width: {self.buff_frame.winfo_width()}") # errors out if a buff is deleted, using bbox instead
        # print(f"buff_window_id: {self.buff_window_id}")
        # print(f"self.canvas_test.bbox(): {self.canvas_test.bbox()}")
        # print(f"self.canvas_test.cget.scrollregion(): {self.canvas_test.cget.scrollregion()}")
        # print(f'self.canvas_test.cget("scrollregion"): {self.canvas_test.cget("scrollregion")}')
        # print(f'self.canvas_test.configure("scrollregion"): {self.canvas_test.configure("scrollregion")}')
        # print(f'self.canvas_test.cget("confine"): {self.canvas_test.cget("confine")}')
        # print(f'self.canvas_test.configure("confine"): {self.canvas_test.configure("confine")}')


    def character_name(self): # lets user set their character name so only their buffs are captured from the chat log
        self.name_entry_window = tk.Toplevel(self)
        self.name_entry_window.title("Enter Character Name")
        self.name_stringvar = tk.StringVar()
        self.name_label = ttk.Label(self.name_entry_window, text="Enter character name\nExample: Sleve Mcdichael\nAdd quotes for disguise: \"Maskedess Drowess\"\nNote: case and space-sensitive")
        self.name_label.grid(column=0, row=0, columnspan=2)
        self.name_entry = tk.Entry(self.name_entry_window, width = 30, textvariable = self.name_stringvar)
        self.name_entry.grid(column=0, row=1, columnspan=2)
        self.show_name_label = ttk.Label(self.name_entry_window, text="Name:")
        self.show_name_label.grid(column=0, row=2, sticky='e')
        self.show_name_stringvar = ttk.Label(self.name_entry_window, textvariable=self.name_stringvar)
        self.show_name_stringvar.grid(column=1, row=2, sticky='w')
        self.button_enter = tk.Button(self.name_entry_window, text="OK", command=lambda: self.name_entry_window.destroy())
        self.button_enter.grid(column=0, row=3, columnspan=2)
        self.name_entry_window.attributes("-topmost", True) # allows window to appear above the main "topmost" window so it isn't hidden behind

    def testing_buttons(self):
        # seperate window for holding debugging stuff
        self.testing_buttons_window = tk.Toplevel(self)
        self.testing_buttons_window.title("Buttons for testing")
        # bebugging buttons, moved into its down toplevel
        self.debugging_buttons_frame = tk.Frame(self.testing_buttons_window)
        self.debugging_buttons_frame.grid(column=0, row=1)
        self.debugging_label = ttk.Label(self.debugging_buttons_frame, text="Only click if you know what\nyou're doing")
        self.debugging_label.grid(column=0, row=10)
        self.button1 = ttk.Button(self.debugging_buttons_frame)
        self.button1['text'] = "Simulate frame list appended True Strike"
        self.button1['command'] = lambda: self.buffs_frame_list_is_appended(["True Strike", time.time() + 9, "NWN-Buff-Watcher\graphics\p_true.png"])
        self.button1.grid(column=0, row=11)
        self.button2 = ttk.Button(self.debugging_buttons_frame)
        self.button2['text'] = "Simulate frame list appended Bulls"
        self.button2['command'] = lambda: self.buffs_frame_list_is_appended(["Bulls", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_bulls.png"])
        self.button2.grid(column=0, row=12)
        self.button0 = ttk.Button(self.debugging_buttons_frame)
        self.button0['text'] = "Simulate frame list appended Endurance"
        self.button0['command'] = lambda: self.buffs_frame_list_is_appended(["Endurance", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_endu.png"])
        self.button0.grid(column=0, row=13)
        # the simulated looping doesn't work with the logfile stuff activated... need to make a nothing variable when click testing
        self.button4 = ttk.Button(self.debugging_buttons_frame)
        self.button4['text'] = "START loops of time passing"
        self.button4['command'] = lambda: self.buffs_loop_time_passing()
        self.button4.grid(column=0, row=14)
        self.geo_blank = ttk.Button(self.debugging_buttons_frame, text="Set geo to ''", command=lambda: app.geometry(""))
        self.geo_blank.grid(column=0, row=15)
        self.resize_test = ttk.Button(self.debugging_buttons_frame, text="resize call", command=lambda: self.resize_set_buff_window("test"))
        self.resize_test.grid(column=0, row=16)
        self.testing_buttons_window.attributes("-topmost", True) # allows window to appear above the main "topmost" window so it isn't hidden behind


    def open_file(self): # opens the game chat log file to watch, moves to the end so it doesn't scan potentially 1000s of lines, only want most recent
        self.logfile = askopenfile(mode ='r', filetypes =[('Logs', '*.txt'), ('Any', '*.*')]) 
        self.logfile_name = self.logfile.name
        open(self.logfile_name, 'r')
        self.logfile.seek(0, 2)
        self.after(100, self.buffs_loop_time_passing)


    def buffs_loop_time_passing(self):
        
        buffs = self.logfile.readlines() # when readlines is called it gets the newlines that have been written in the file since their last update and puts them as seperate list items into a list
        
        # print(buffs) # debugging, shows the chat lot output from the game in the console

        if self.name_stringvar.get() + " uses Potion of Endurance" in str(buffs): # turning the list input from the chatlog into a string to search with "in" for the matching trigger for the buff
            self.buffs_frame_list_is_appended(["Endurance", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_endu.png"])

        elif self.name_stringvar.get() + " uses Potion of Cat\\'s Grace" in str(buffs):
            self.buffs_frame_list_is_appended(["Cat's Grace", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_cats.png"])

        elif self.name_stringvar.get() + " uses Potion of Bull\\'s Strength" in str(buffs):
            self.buffs_frame_list_is_appended(["Bull's Strength", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_bulls.png"])
        
        elif self.name_stringvar.get() + " uses Potion of Owl\\'s Wisdom" in str(buffs):
            self.buffs_frame_list_is_appended(["Owl's Wisdom", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_owls.png"])
        
        elif self.name_stringvar.get() + " uses Potion of Fox\\'s Cunning" in str(buffs):
            self.buffs_frame_list_is_appended(["Fox's Cunning", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_foxs.png"])
        
        elif self.name_stringvar.get() + " uses Potion of Clarity" in str(buffs):
            self.buffs_frame_list_is_appended(["Clarity", time.time() + 48, "NWN-Buff-Watcher\graphics\p_clar.png"])
            self.buffs_frame_list_is_appended(["Clarity Cooldown", time.time() + 72, "NWN-Buff-Watcher\graphics\p_clar_cooldown.png"])

        elif self.name_stringvar.get() + " uses Potion of Eagle\\'s Splendor" in str(buffs): # not firing, because of \'s... investigate further
            self.buffs_frame_list_is_appended(["Eagle's Splendor", time.time() + 1080, "NWN-Buff-Watcher\graphics\p_eagle.png"])

        elif self.name_stringvar.get() + " uses Potion of Barkskin" in str(buffs):
            self.buffs_frame_list_is_appended(["Barkskin", time.time() + 4320, "NWN-Buff-Watcher\graphics\p_bark.png"])

        elif self.name_stringvar.get() + " uses Potion of True Strike" in str(buffs):
            self.buffs_frame_list_is_appended(["True Strike", time.time() + 9, "NWN-Buff-Watcher\graphics\p_true.png"])

        elif self.name_stringvar.get() + " uses Potion of Freedom" in str(buffs):
            self.buffs_frame_list_is_appended(["Freedom", time.time() + 2520, "NWN-Buff-Watcher\graphics\p_freedom.png"])

        elif self.name_stringvar.get() + " uses Potion of Speed" in str(buffs):
            self.buffs_frame_list_is_appended(["Haste", time.time() + 30, "NWN-Buff-Watcher\graphics\p_freedom.png"])

        elif self.name_stringvar.get() + " uses Shield" in str(buffs):
            self.buffs_frame_list_is_appended(["Shield", time.time() + 300, "NWN-Buff-Watcher\graphics\p_shield.png"])

        elif self.name_stringvar.get() + " uses Shadow Shield" in str(buffs):
            self.buffs_frame_list_is_appended(["Shadow Shield", time.time() + 780, "NWN-Buff-Watcher\graphics\p_shadow_shield.png"])

        elif "Hex has a timer of 30 second(s)." in str(buffs):
            self.buffs_frame_list_is_appended(["Hex", time.time() + 30, "NWN-Buff-Watcher\graphics\p_hex.png"])

        """ TODO: only calculate all the time() countdowns in one place, but move and
        display them in more if needed, process savings?

        TODO: Have an entry for CHA modifier, to calculate things like divine shield and might

        TODO: Have a CL entry to calculate spells cast

        TODO: make the buffs variable into a string instead of string-ifying it on each if statement... isn't slow right now though anyway
        """

        for x in self.buffs_list_frames: # removes any buffs that reach 0, makes them red if they're below 6 s TODO: let user set that threshold
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            if x.buff_birthday < time.time() + 6:
                x['background'] = 'red'
            if x.buff_birthday < time.time():
                self.buffs_list_frames.remove(x)
                x.destroy()
                self.resize_set_buff_window('buff destroy')
        
        self.after(100, self.buffs_loop_time_passing)

    def buffs_frame_list_is_appended(self, added_buff):
        """ includes name, bday, duration
        builds the labelframe for each buff and adds it to the list
        of buffs that gets displayed
        """ 

        self.buff_frame = tk.LabelFrame(self.buff_holding_frame, borderwidth=1, text=added_buff[0][0:4], labelanchor="n")

        # TODO width isn't getting through...

        self.buff_frame.buff_image_reference = ImageTk.PhotoImage(Image.open(added_buff[2]))
        self.buff_frame.buff_image_label = ttk.Label(self.buff_frame, image=self.buff_frame.buff_image_reference)
        self.buff_frame.buff_image_label.image_keep = self.buff_frame.buff_image_reference # keeping image in memory
        self.buff_frame.buff_image_label.grid(column=0, row=0)
        self.buff_frame.buff_birthday = added_buff[1]
        self.buff_frame.buff_timer = tk.StringVar()
        self.buff_frame.buff_timer.set(f"{self.buff_frame.buff_birthday - time.time():.1f}s")
        self.buff_frame.buff_label = ttk.Label(self.buff_frame, textvariable=self.buff_frame.buff_timer)
        self.buff_frame.buff_label.grid(column=0, row=1)
        # Add the Frame to the list
        self.buffs_list_frames.append(self.buff_frame)

        # debugging
        # print(self.buffs_list_frames)
        # print(self.buff_frame.buff_timer.get())
        # print(f"buff_frame.winfo_width: {self.buff_frame.winfo_width()}")

        self.buffs_display_nicely()

    def buffs_display_nicely(self):
        """ takes all the buffs labelframe objects and sorts and displays them
        nicely in the buff_frame in the canvas
        """
        # TODO let user choose how to sort, keeping alphabetical for reference
        # self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z['text'], reverse=True) # sort alphabetically
        self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z.buff_birthday - time.time(), reverse=False) # sort remaining time
        for x in self.buffs_list_frames:
            x.pack_forget()
            x.pack(side="right")
        self.resize_set_buff_window('buff display')

    def rest_off_buffs(self): # removes all buffs and removes the frame border by re-drawing as 1 width when character rests
        for x in self.buffs_list_frames:
            x.destroy()
        self.buffs_list_frames.clear()
        self.buff_holding_frame['width'] = "1"

    def friends_list_window(self):

        self.friends_window = tk.Toplevel(self)
        self.friends_window.title("Friends")
        self.friends_stringvar = tk.StringVar()
        self.directions_label = ttk.Label(self.friends_window, text="Enter friends in the friends.csv")
        self.directions_label.pack()
        self.refresh_button = ttk.Button(self.friends_window, text="Refresh", command=lambda: self.button_friends())
        self.refresh_button.pack()
        self.friends_printout = tk.Label(self.friends_window, textvariable=self.friends_stringvar, font=("Courier", 8), justify='left')
        self.friends_printout.pack()
        self.friends_window.attributes("-topmost", True)

    def button_friends(self):
        self.friends_stringvar.set(friends_list.scrape_portal())
        """
        TODO: learn threading and/or async to remove the window freeze while urllib is getting the portal page
        https://stackoverflow.com/questions/47895765/use-asyncio-and-tkinter-or-another-gui-lib-together-without-freezing-the-gui
        https://www.oreilly.com/library/view/python-cookbook/0596001673/ch09s07.html
        https://stackoverflow.com/questions/48254837/python-async-await-downloading-a-list-of-urls?rq=1  --- this one looks promising, async.Semaphore?
        """


class App(tk.Tk): # creating a tk window object and using it for overall constructor, but otherwise not good practice to do much more with it, instead you build stuff in the "window" inside of a Frame widget that makes up the whole interior of the window
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('NWN Buff Watcher')
        # self.geometry('300x50')
        self.attributes("-topmost", True) # forces the buff watcher to float above all other windows, including NWN, so you can see it while you play!

        # menu for file > open -- not using a menubar to make the window thinner, menu in settings button instead
        # self.menubar = Menu(self)
        # self.config(menu=self.menubar) 
        # self.menubar.add_cascade(label="File", menu=self.file_menu) 

        self.columnconfigure(0, weight=1) # allows the main frame to grow in the 0,0 column and row setup in that main_frame
        self.rowconfigure(0, weight=1) # allows the main frame to grow in the 0,0 column and row setup in that main_frame

        # setting boundaries on resize, not needed but here
        # self.resizable(1, 0) # no reason to resize height, removing abiilty
        # self.maxsize(1080, 96) # alternate way to stop resize height, lets go lower and can set max width... nice effect when attacking to top or side of screen


if __name__ == "__main__":
    app = App()
    main_frame = MainFrame(app)
    app.mainloop()