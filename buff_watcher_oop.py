"""
Author: Mattamue
Program: buff_watcher_oop.py
Last updated: 05/0/2021

Watches chat log of the Neverwinter Nights video game
and extends the UI by overlaying a window with more
information than is usually in the game

"""


# probably need to clean these up

import tkinter as tk
from tkinter import ttk, Menu
from PIL import ImageTk, Image
import time
from tkinter.filedialog import askopenfile
from get_friends_list import friends_list
import json

"""
the MainFrame class is the main object of the program, when the driver in the "if __main__" below runs, it instantiates an instance of this class
as an object, and everything else runs from there -- this class has gotten very big and needs to be broken down, probably starting with
making the buff_frame its own class and functions
"""

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.grid(column=0, row=0, sticky='nsew') # loads the main_frame into the parent window, sticky makes the "main" containing frame stretch when the window is resized

        self.columnconfigure(0, weight=1) # allows the main_frame *in its frame* to grow side to side in the column when the window is resized, since it doesn't share with other widgets it gets 100% of the 1 weight
        self.rowconfigure(0, weight=1) # allows the main_frame *in its frame* to grow up and down in the row when the window is resized, since it doesn't share with other widgets it gets 100% of the 1 weight

        self.buffs_list_frames = [] # setting this to be used later

        self.name_stringvar = tk.StringVar() # setting in constructor so doesn't error when opening file when not set

        # loading up the "use items" json in the constructor... probably a better way to do this
        self.use_items_dict = json.load(open('NWN-Buff-Watcher/buffs_json/use_items.json','r'))

        # frame for the buttons on the right
        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.grid(column=1, row=0)

        # resting removes all buffs
        self.rest_button = ttk.Button(self.buttons_frame, text="Rest", command=lambda: self.rest_off_buffs())
        self.rest_button.grid(column=0, row=0, sticky='ew')

        # putting all the "normal" menus into this button to reduce the height of the window since the traditional file menu adds like another 20 pixels of heigth that do nothing
        self.menu_button = ttk.Menubutton(self.buttons_frame, text="Settings")
        self.menu_button.grid(column=0, row=1, sticky='ew')
        # tearoff is an old unix (I think) thing that allows you to click and have the menu be its own window, we don't want that so its set to 0
        self.menu_button.menu = Menu(self.menu_button, tearoff=0)
        self.menu_button["menu"] = self.menu_button.menu
        self.menu_button.menu.add_command(label='Name', command=lambda: main_frame.character_name())
        self.menu_button.menu.add_command(label='Open log...', command=lambda: main_frame.open_file())
        self.menu_button.menu.add_command(label='Friends', command=lambda: main_frame.friends_list_window())
        self.menu_button.menu.add_command(label='Testing', command=lambda: main_frame.testing_buttons())
        self.menu_button.menu.add_separator()
        self.menu_button.menu.add_command(label='Exit', command=lambda: app.destroy())

        # creating the canvas that will be scrollable and have the buff_frame built into it as a window so it'll be scrollable
        self.canvas_test = tk.Canvas(self, height=70, width=500)
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
        # draws a canvas widget that we're going to put a frame with the buffs into later
        # these three lines were a lot more work than they seem
        self.re_size_move = (self.canvas_test.winfo_width() - ((self.canvas_test.bbox(1)[2] - self.canvas_test.bbox(1)[0]))) + self.canvas_test.canvasx(0)
        self.canvas_test.moveto(1, self.re_size_move, 0)
        self.canvas_test.configure(scrollregion=self.canvas_test.bbox("all"))

        # debugging --- getting the buffs to sit at the right and move correctly with window resizes was HARD
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


    def character_name(self):
        # lets user set their character name so only their buffs are captured from the chat log
        # expand this out so that it can save settings, and has settings for caster level, LM, player-made zoo pots
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
        # seperate window for holding debugging stuff, nice when not want to boot up NWN all the time
        self.testing_buttons_window = tk.Toplevel(self)
        self.testing_buttons_window.title("Buttons for testing")
        self.debugging_buttons_frame = tk.Frame(self.testing_buttons_window)
        self.debugging_buttons_frame.grid(column=0, row=1)
        self.debugging_label = ttk.Label(self.debugging_buttons_frame, text="Only click if you know what\nyou're doing")
        self.debugging_label.grid(column=0, row=9)
        # re-tooling for the BuffLabelFrame object
        self.button1 = ttk.Button(self.debugging_buttons_frame)
        self.button1['text'] = "Simulate frame list appended True Strike"
        self.button1['command'] = lambda: self.make_buff_labelframe(["True Strike", time.time() + 9, "NWN-Buff-Watcher/graphics/true.png"])
        self.button1.grid(column=0, row=11)
        self.button2 = ttk.Button(self.debugging_buttons_frame)
        self.button2['text'] = "Simulate frame list appended Bulls"
        self.button2['command'] = lambda: self.make_buff_labelframe(["Bulls", time.time() + 1080, "NWN-Buff-Watcher/graphics/bulls.png"])
        self.button2.grid(column=0, row=12)
        self.button0 = ttk.Button(self.debugging_buttons_frame)
        self.button0['text'] = "Simulate frame list appended Endurance"
        self.button0['command'] = lambda: self.make_buff_labelframe(["Endurance", time.time() + 1080, "NWN-Buff-Watcher/graphics/endu.png"])
        self.button0.grid(column=0, row=13)
        self.button3 = ttk.Button(self.debugging_buttons_frame)
        self.button3['text'] = "Simulate frame list appended Clarity"
        self.button3['command'] = lambda: self.make_buff_labelframe(["Clarity", time.time() + 48, "NWN-Buff-Watcher/graphics/clar.png"])
        self.button3.grid(column=0, row=10)

        # don't run simulated looping with actual looping, or click more than once, causes two loops that get weird
        self.button4 = ttk.Button(self.debugging_buttons_frame)
        self.button4['text'] = "START loops of time passing"
        self.button4['command'] = lambda: [self.testing_logloops(), self.buffs_loop_time_passing()]
        self.button4.grid(column=0, row=14)

        self.geo_blank = ttk.Button(self.debugging_buttons_frame, text="Set geo to ''", command=lambda: app.geometry(""))
        self.geo_blank.grid(column=0, row=15)
        self.resize_test = ttk.Button(self.debugging_buttons_frame, text="resize call", command=lambda: self.resize_set_buff_window("test"))
        self.resize_test.grid(column=0, row=16)
        self.testing_buttons_window.attributes("-topmost", True) # allows window to appear above the main "topmost" window so it isn't hidden behind

    def make_buff_labelframe(self, added_buff):
        """ Makes a labelframe object with some special
        buff parameters passed in a list
        :param: list, expecting this type of format ["Clarity", time.time() + 48, "NWN-Buff-Watcher/graphics/clar.png"]
        :return: also returns the object
        """
        self.buff_labelframe = BuffLabelFrame(self.buff_holding_frame, added_buff)
        return self.buff_labelframe

    def testing_logloops(self):
        # sets a dummy file when testing without actually opening an active NWN log file
        self.logfile = open("dummy.tmp","w+")

    def open_file(self):
        # opens the game chat log file to watch
        # when first runs, moves the pointer (where it reads from) to the end so it doesn't scan potentially 1000s of lines, only want most recent
        self.logfile = askopenfile(mode ='r', filetypes =[('Logs', '*.txt'), ('Any', '*.*')]) 
        self.logfile_name = self.logfile.name
        open(self.logfile_name, 'r')
        self.logfile.seek(0, 2)
        self.after(100, self.buffs_loop_time_passing)


    def buffs_loop_time_passing(self):
        # the main "loop" of the watcher, calls itself at the end to keep watching the chat log for new lines and updating timers
        
        buffs = self.logfile.readlines() # when readlines is called it gets the newlines that have been written in the file since their last update and puts them as seperate list items into a list
        
        # print(buffs) # debugging, shows the chat lot output from the game in the console

        for logline in buffs:
            if self.name_stringvar.get() + " uses " in logline: # need a modifier for vendor vs player potions
                start = logline.split(" ").index("uses")
                stop = len(logline.split(" "))
                output_string = ""
                for x in range(start, stop):
                    output_string = output_string + logline.strip().split(" ")[x] + " "
                # print(output_string[:-1]) # testing
                self.uses_call(output_string[:-1])

        for x in self.buffs_list_frames: # removes any buffs that reach 0, makes them red if they're below 6 s
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            if x.buff_birthday < time.time() + 6:
                x['background'] = 'red'
            if x.buff_birthday < time.time():
                self.buffs_list_frames.remove(x)
                x.destroy()
                self.resize_set_buff_window('buff destroy')
        
        self.after(100, self.buffs_loop_time_passing) # 1000 works... trying 100

    def uses_call(self, buff_string):
        # takes the string that comes back from the main loop and compares it to a dictionary of all possible "character uses X thing" responses
        # that dictionary has the "char uses X" as the keys so it can easily return the values like duration and icon
        # much faster (I think) than the if > elif > elif... I was using to prototype, easy to put in a json and potentially easy for
        # users to add their own "unique" item uses into the json without having to know the code -- or not have access to the code
        # if/when I make a PyInstaller .exe release
        
        adding_buff = []
        
        try: # handle "uses" lines that aren't defined in the json, otherwise they exception and stop the program
            adding_buff.append(self.use_items_dict[f'{buff_string}']['name'])
            adding_buff.append(time.time() + (int(self.use_items_dict[f'{buff_string}']['duration']) *
                                            int(self.use_items_dict[f'{buff_string}']['caster_level'])))
            adding_buff.append(self.use_items_dict[f'{buff_string}']['icon'])
            # print(adding_buff) # testing
            if self.use_items_dict[f'{buff_string}']['name'] == "Clarity": # edge cases for clarity... not sure if this is the best way to handle -- gets wand and potion
                adding_buff[1] = adding_buff[1] + 30
                self.make_buff_labelframe(["CD Clarity", time.time() + 72, "NWN-Buff-Watcher/graphics/clar_cooldown.png"])
            if self.use_items_dict[f'{buff_string}']['name'] == "Improved Invisibility": # edge case for imp invis tracking invis and concealment seperate -- on just wands of imp invis*** -- need something to juice invis on GSF/ESF
                self.make_buff_labelframe(["Invisibility", time.time() + 42, "NWN-Buff-Watcher/graphics/invisibility.png"])
            self.make_buff_labelframe(adding_buff)
        except:
            print(f"EXCEPTED ON SOMETHING: {buff_string}") # for now just fart out that it was handled, maybe later add to a CSV and user can add to json with a buff-managing window?

    def buffs_display_nicely(self):
        """ takes all the buffs labelframe objects and sorts and displays them
        nicely in the buff_frame in the canvas
        """

        # self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z['text'], reverse=True) # sort alphabetically instead... see TODO above

        # remove duplicates

        self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z.buff_birthday - time.time(), reverse=True) # sort remaining reverse so the old duplicates get removed

        unique_buffs_set = set() # sets don't allow duplicates, we'll use this property in a few lines
        non_duplicates = [] # empty set to re-build with the non-duplicates
        for obj in self.buffs_list_frames: # looping through our buffs list
            if obj.buff_name not in unique_buffs_set: # if the buff name is not in the list (will always be true 1st time)
                non_duplicates.append(obj) # add the non-duplicate to the new list
                unique_buffs_set.add(obj.buff_name) # add the "name" identifier to the set, logically we wouldn't be able to anyway in this loop, but helps be sure
            else:
                obj.destroy() # if it is a duplicate it isn't getting built into the new list, so we don't want it hanging around in the window, destroy it so there's no "ghost" of a buff

        self.buffs_list_frames = non_duplicates # rebuild the buff list with just the non-duplicates

        # sort the list before packing and displaying
        self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z.buff_birthday - time.time(), reverse=False) # sort remaining time back to oldest to the left

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



class BuffLabelFrame(tk.LabelFrame):
    def __init__(self, container, buff_added):
        super().__init__(container)

        self.added_buff = buff_added

        self.config(width=44, height=70, borderwidth=1, text=self.added_buff[0][0:4], labelanchor="n")
        self.grid_propagate(0)
        self.columnconfigure(0, weight=1) 
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.buff_name = self.added_buff[0]
        self.buff_image_reference = ImageTk.PhotoImage(Image.open(self.added_buff[2]))
        self.buff_image_label = ttk.Label(self, image=self.buff_image_reference)
        self.buff_image_label.image_keep = self.buff_image_reference # keeping image in memory
        self.buff_image_label.grid(column=0, row=0)
        self.buff_birthday = self.added_buff[1]
        self.buff_timer = tk.StringVar()
        self.buff_timer.set(f"{self.buff_birthday - time.time():.1f}s")
        self.buff_label = ttk.Label(self, textvariable=self.buff_timer)
        self.buff_label.grid(column=0, row=1)

        # adding click-ability to click the buff frame image
        self.buff_image_label.bind("<Button-1>", self.clicked_in_buff_frame)

        self.click_menu = Menu(self, tearoff=0)

        self.click_menu.add_command(label='Extended (nothing yet)')
        self.click_menu.add_command(label='Sub-buff (ie shadow conj) (nothing yet)')
        self.click_menu.add_command(label='Destroy', command=lambda: self.menu_destroy_buff_labelframe())

        # When the object is created, add the Frame to the buffs list in the main_frame
        # probably move this elsewhere
        main_frame.buffs_list_frames.append(self)

        # When the object is created, call the function in the main_frame that organizes and displays them
        # probably move this elsewhere
        main_frame.buffs_display_nicely()

    def clicked_in_buff_frame(self, event):
        self.click_menu.post(event.x_root, event.y_root)

    def menu_destroy_buff_labelframe(self):
        main_frame.buffs_list_frames.remove(self)
        self.destroy()
        main_frame.resize_set_buff_window('buff destroy')


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