"""
Author: Mattamue
Program: buff_watcher_oop.py
Last updated: 05/20/2021

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
from abilities import abilities_trigger
import json
from summons_cooldown import summons_cd_call

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
        self.smite_iterator = 0
        self.smite_list = []

        # feel like I'm saying this a lot... probably a better place for this...
        # tries to open settings, just goes with defaults if it can't
        try:
            self.char_options = json.load(open('settings.json','r'))
            self.name_stringvar = tk.StringVar() 
            self.name_stringvar.set(self.char_options['name'])
            self.cha_modifier = tk.IntVar()
            self.cha_modifier.set(self.char_options['cha_mod'])
            self.cl_modifier = tk.IntVar()
            self.cl_modifier.set(self.char_options['cl_mod'])
            self.vendor_bool = tk.BooleanVar()
            self.vendor_bool.set(self.char_options['vop_bool'])
            self.lm_modifier = tk.IntVar()
            self.lm_modifier.set(self.char_options['lm_mod'])
            self.sf_illu_state = tk.IntVar()
            self.sf_illu_state.set(self.char_options['illu_mod'])
            self.cot_modifier = tk.IntVar()
            self.cot_modifier.set(self.char_options['cot_mod'])
            self.sf_div_state = tk.IntVar()
            self.sf_div_state.set(self.char_options['div_mod'])
            self.sf_trans_state = tk.IntVar()
            self.sf_trans_state.set(self.char_options['trans_mod'])
            self.character_level = tk.IntVar()
            self.character_level.set(self.char_options['char_level'])
            print("Loaded char settings.")
        except:
            # setting in constructor for main_frame... maybe a better way to do this?
            self.name_stringvar = tk.StringVar() 
            self.cha_modifier = tk.IntVar()
            self.cl_modifier = tk.IntVar()
            self.vendor_bool = tk.BooleanVar()
            self.vendor_bool.set(True) # setting a default... might turn off if impliment csv/options file -- or set there... maybe a json
            self.lm_modifier = tk.IntVar()
            self.sf_illu_state = tk.IntVar()
            self.cot_modifier = tk.IntVar()
            self.sf_div_state = tk.IntVar()
            self.sf_trans_state = tk.IntVar()
            self.character_level = tk.IntVar()
            print("Loaded defaults.")

        # loading up the "use items" json in the constructor... probably a better way to do this
        self.use_items_dict = json.load(open('NWN-Buff-Watcher/buffs_json/use_items.json','r'))
        self.cast_spells_dict = json.load(open('NWN-Buff-Watcher/buffs_json/cast_spells.json','r'))
        self.ability_ref_dict = json.load(open('NWN-Buff-Watcher/buffs_json/ability_ref.json','r'))

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
        self.menu_button.menu.add_command(label='Character', command=lambda: main_frame.character_settings())
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


    def character_settings(self):
        # TODO: refactor this into a class of TopLevel, but still have the name, level, and stuff available?
        
        # lets user set their character name so only their buffs are captured from the chat log
        # expand this out so that it can save settings, and has settings for caster level, LM, player-made zoo pots
        self.character_settings_window = tk.Toplevel(self) # creates a "toplevel" window which just means another pop-out window when called
        self.character_settings_window.title("Character Settings") # name for the window, duh
        self.character_settings_window.attributes("-topmost", True) # allows window to appear above the main "topmost" window so it isn't hidden behind

        # since we're taking user input here we have to validate
        # https://stackoverflow.com/questions/4140437/interactively-validating-entry-widget-content-in-tkinter/4140988#4140988
        # we'll use this later where users are meant to enter intergers
        vcmd = (self.character_settings_window.register(self.validate_int), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        # all the name stuff in a frame
        self.name_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.name_frame.grid(column=0, row=0, sticky='ew')
        self.name_label = ttk.Label(self.name_frame, text="Enter character name\nExample: Sleve Mcdichael\nAdd quotes for disguise: \"Maskedess Drowess\"\nNote: case and space-sensitive")
        self.name_label.grid(column=0, row=0, columnspan=2)
        self.name_entry = tk.Entry(self.name_frame, width = 30, textvariable = self.name_stringvar)
        self.name_entry.grid(column=0, row=1, columnspan=2)
        self.name_entry.focus_set() # sets the focus and cursor here when the window is opened, in the name field
        self.show_name_label = ttk.Label(self.name_frame, text="Name:")
        self.show_name_label.grid(column=0, row=2, sticky='e')
        self.show_name_stringvar = ttk.Label(self.name_frame, textvariable=self.name_stringvar)
        self.show_name_stringvar.grid(column=1, row=2, sticky='w')

        # cha modifier in its own frame
        self.cha_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.cha_frame.grid(column=0, row=1, sticky='ew')
        self.cha_description = ttk.Label(self.cha_frame, text="Enter charisma modifier for\nabilities like divine shield\nin order to estimate duration\n(enter an interger)")
        self.cha_description.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.cha_entry = tk.Entry(self.cha_frame, width=10, textvariable=self.cha_modifier, validate='key', validatecommand=vcmd) # also validating that its interger input
        self.cha_entry.grid(column=1, row=1, sticky='e')
        self.cha_label = ttk.Label(self.cha_frame, text="Cha modifier:")
        self.cha_label.grid(column=0, row=1, sticky='w')
        self.cot_entry = tk.Entry(self.cha_frame, width=10, textvariable=self.cot_modifier, validate='key', validatecommand=vcmd)
        self.cot_entry.grid(column=1, row=2, sticky='e')
        self.cot_label = ttk.Label(self.cha_frame, text="CoT Levels (for Wrath):")
        self.cot_label.grid(column=0, row=2, sticky='w')

        # caster level in its own frame
        self.caster_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.caster_frame.grid(column=0, row=2, sticky='ew')
        self.cl_description = ttk.Label(self.caster_frame, text="Enter caster level for tracking\nof self-cast buffs\n(enter an interger)")
        self.cl_description.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.cl_entry = tk.Entry(self.caster_frame, width=10, textvariable=self.cl_modifier, validate='key', validatecommand=vcmd) # also validating that its interger input
        self.cl_entry.grid(column=1, row=1, sticky='e')
        self.cl_label = ttk.Label(self.caster_frame, text="Caster Level:")
        self.cl_label.grid(column=0, row=1, sticky='w')

        # vendor/player pots in its own frame
        self.vop_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.vop_frame.grid(column=0, row=3, sticky='ew')
        self.vop_description = ttk.Label(self.vop_frame, text="Using vendor or player-made\nzoo or barkskin potions?\n(affects duration)")
        self.vop_description.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.vop_radiobutton_vendor = tk.Radiobutton(self.vop_frame, text="Vendor", variable=self.vendor_bool, value=True)
        self.vop_radiobutton_vendor.grid(column=0, row=1, sticky="w")
        self.vop_radiobutton_player = tk.Radiobutton(self.vop_frame, text="Player", variable=self.vendor_bool, value=False)
        self.vop_radiobutton_player.grid(column=1, row=1, sticky="e")

        # Loremaster levels in its own frame
        self.lm_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.lm_frame.grid(column=0, row=4, sticky='ew')
        self.lm_description = ttk.Label(self.lm_frame, text="Loremaster levels increase the\ncaster level of wands and scrolls\nand therefore the duration. Enter\nyour Loremaster levels\n(enter an interger)")
        self.lm_description.grid(column=0, row=0, columnspan=2, sticky='ew')
        self.lm_entry = tk.Entry(self.lm_frame, width=10, textvariable=self.lm_modifier, validate='key', validatecommand=vcmd) # also validating that its interger input
        self.lm_entry.grid(column=1, row=1, sticky='e')
        self.lm_label = ttk.Label(self.lm_frame, text="Loremaster Level:")
        self.lm_label.grid(column=0, row=1, sticky='w')

        # SF Illusion in its own frame
        self.sf_illu_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.sf_illu_frame.grid(column=1, row=0, sticky='ew')
        self.sf_illu_description = ttk.Label(self.sf_illu_frame, text="Set Spell Focus: Illusion\nstatus, controls length of invsibility\n0 = none\n1 = GSF\n2 = ESF")
        self.sf_illu_description.grid(column=0, row=0, sticky='ew')

        self.option_menu = ttk.OptionMenu(
            self.sf_illu_frame,
            self.sf_illu_state,
            0,
            *range(0, 3)
            #, command=self.option_changed
            )

        self.option_menu.grid(column=0, row=1, sticky='ew')

        # SF Div in its own frame
        self.sf_div_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.sf_div_frame.grid(column=1, row=1, sticky='ew')
        self.sf_div_description = ttk.Label(self.sf_div_frame, text="Set Spell Focus: Divination\nstatus, controls length of true seeing\n0 = none\n1 = SF\n2 = GSF\n3 = ESF")
        self.sf_div_description.grid(column=0, row=0, sticky='ew')
        self.sf_option_menu = ttk.OptionMenu(self.sf_div_frame, self.sf_div_state, 0, *range(0, 4))
        self.sf_option_menu.grid(column=0, row=1, sticky='ew')

        # SF Trans in its own frame
        self.sf_trans_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.sf_trans_frame.grid(column=1, row=2, sticky='ew')
        self.sf_trans_description = ttk.Label(self.sf_trans_frame, text="Set Spell Focus: Trans\nstatus, controls length of\nAura of Vitality\n0 = none\n1 = GSF\n2 = ESF")
        self.sf_trans_description.grid(column=0, row=0, sticky='ew')
        self.sf_trans_option_menu = ttk.OptionMenu(self.sf_trans_frame, self.sf_trans_state, 0, *range(0, 3))
        self.sf_trans_option_menu.grid(column=0, row=1, sticky='ew')

        # character level/innate ability own frame
        self.char_level_frame = tk.Frame(self.character_settings_window, bd=1, relief='solid')
        self.char_level_frame.grid(column=1, row=3, sticky='ew')
        self.char_level_description = ttk.Label(self.char_level_frame, text="Setting total character\nlevel for innate ability duration\n(for the few races that get one)")
        self.char_level_description.grid(column=0, row=0, sticky='ew', columnspan=2)
        self.char_level_entry = tk.Entry(self.char_level_frame, width=10, textvariable=self.character_level, validate='key', validatecommand=vcmd) # also validating that its interger input
        self.char_level_entry.grid(column=1, row=1, sticky='e')
        self.char_level_label = ttk.Label(self.char_level_frame, text="Character Level:")
        self.char_level_label.grid(column=0, row=1, sticky='w')

        # binding return to the OK button, also OK button just kills the window... figure some save/cancel instead?
        self.character_settings_window.bind("<Return>", self.close_character_settings_window)
        self.button_enter = tk.Button(self.character_settings_window, text="Save", command=lambda: self.close_character_settings_window("saved"))
        self.button_enter.grid(column=0, row=7, columnspan=2)

    def validate_int(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        ''' Here we take the vcmd from the entry windows and try to validate if they're intergers
        The "value_if_allowed" argument is %P from above
        The "text" argument is %S from above
        value_if_allowed is more strict in that it doesn't even let you delete data from the cell
        since an empty value isn't an int, but that's not how users expect it to work, so the
        text argument is closer even if it poops out some errors now and then
        '''
        int_set = set("1234567890-")

        """
        this checks if the value being typed into the entry field is part of the 1 to 0 set; allows users
        to delete since that's what usually expected (you don't think about it, but highlighting a 0 and
        changing it to something is really deleting the 0 and typing the new number) the empty values are
        handled later in the close_char_window function since there's no easy way to allow deletes and not
        allow this possible empty field

        Some joker might still mess it up with the "-" but no way around it if the field is going to
        allow negative cha mod
        """

        if int_set.issuperset(value_if_allowed):
            return True
        else:
            self.bell()
            return False

    def close_character_settings_window(self, event):
        # handling if user left these int fields blank when they saved
        # otherwise, the validation will make sure they're at least an int

        savefile = {}

        # name can be anything and the radiobuttons can't get any user input but true and false so they're fine
        savefile['name'] = self.name_stringvar.get()
        savefile['vop_bool'] = self.vendor_bool.get()

        # these three have to be in and the valuechecking in the entry windows keeps non 0-9 getting through,
        # but an empty could still be a problem, so anything that fails just gets set to 0 before being saved
        try:
            savefile['cha_mod'] = self.cha_modifier.get()
        except:
            self.cha_modifier.set(0)
            savefile['cha_mod'] = self.cha_modifier.get()
        try:
            savefile['cl_mod'] = self.cl_modifier.get()
        except:
            self.cl_modifier.set(0)
            savefile['cl_mod'] = self.cl_modifier.get()
        try:
            savefile['lm_mod'] = self.lm_modifier.get()
        except:
            self.lm_modifier.set(0)
            savefile['lm_mod'] = self.lm_modifier.get()
        try:
            savefile['illu_mod'] = self.sf_illu_state.get()
        except:
            self.sf_illu_state.set(0)
            savefile['illu_mod'] = self.sf_illu_state.get()
        try:
            savefile['cot_mod'] = self.cot_modifier.get()
        except:
            self.cot_modifier.set(0)
            savefile['cot_mod'] = self.cot_modifier.get()
        try:
            savefile['div_mod'] = self.sf_div_state.get()
        except:
            self.sf_div_state.set(0)
            savefile['div_mod'] = self.sf_div_state.get()
        try:
            savefile['trans_mod'] = self.sf_trans_state.get()
        except:
            self.sf_trans_state.set(0)
            savefile['trans_mod'] = self.sf_trans_state.get()
        try:
            savefile['char_level'] = self.character_level.get()
        except:
            self.character_level.set(0)
            savefile['char_level'] = self.character_level.get()

        # saving to json, w to overwrite old settings, not appending
        with open('settings.json', 'w') as f:
            json.dump(savefile, f, indent=4)

        # closes the window
        self.character_settings_window.destroy()




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
        self.button1['text'] = "Simulate 'uses Wand of Clarity'"
        self.button1['command'] = lambda: self.uses_call("uses Wand of Clarity")
        self.button1.grid(column=0, row=10)
        self.button2 = ttk.Button(self.debugging_buttons_frame)
        self.button2['text'] = "Simulate 'casts Clarity'"
        self.button2['command'] = lambda: self.casts_call("casts Clarity")
        self.button2.grid(column=0, row=11)
        self.button0 = ttk.Button(self.debugging_buttons_frame)
        self.button0['text'] = "Simulate 'uses Clarity' (scroll)"
        self.button0['command'] = lambda: self.uses_call("uses Clarity")
        self.button0.grid(column=0, row=12)
        self.button3 = ttk.Button(self.debugging_buttons_frame)
        self.button3['text'] = "Simulate 'uses Potion of Clarity'"
        self.button3['command'] = lambda: self.uses_call("uses Potion of Clarity")
        self.button3.grid(column=0, row=13)

        self.button_a = ttk.Button(self.debugging_buttons_frame)
        self.button_a['text'] = "Simulate 'uses True Seeing' (scroll)"
        self.button_a['command'] = lambda: self.uses_call("uses True Seeing")
        self.button_a.grid(column=1, row=10)
        self.button_b = ttk.Button(self.debugging_buttons_frame)
        self.button_b['text'] = "Simulate 'casts True Seeing'"
        self.button_b['command'] = lambda: self.casts_call("casts True Seeing")
        self.button_b.grid(column=1, row=11)
        self.button_c = ttk.Button(self.debugging_buttons_frame)
        self.button_c['text'] = "Simulate 'uses Bull's Strength' (scroll)"
        self.button_c['command'] = lambda: self.uses_call("uses Bull's Strength")
        self.button_c.grid(column=1, row=12)
        self.button_d = ttk.Button(self.debugging_buttons_frame)
        self.button_d['text'] = "Simulate 'uses Potion of Endurance'"
        self.button_d['command'] = lambda: self.uses_call("uses Potion of Endurance")
        self.button_d.grid(column=1, row=13)

        self.button_aa = ttk.Button(self.debugging_buttons_frame)
        self.button_aa['text'] = "Simulate 'uses Icon of the Hunt'"
        self.button_aa['command'] = lambda: self.uses_call("uses Icon of the Hunt")
        self.button_aa.grid(column=2, row=10)
        self.button_bb = ttk.Button(self.debugging_buttons_frame)
        self.button_bb['text'] = "Simulate 'casts Aura of Vitality'"
        self.button_bb['command'] = lambda: self.casts_call("casts Aura of Vitality")
        self.button_bb.grid(column=2, row=11)
        self.button_cc = ttk.Button(self.debugging_buttons_frame)
        self.button_cc['text'] = "Simulate 'uses Wand of Bull's Strength'"
        self.button_cc['command'] = lambda: self.uses_call("uses Wand of Bull's Strength")
        self.button_cc.grid(column=2, row=12)
        self.button_dd = ttk.Button(self.debugging_buttons_frame)
        self.button_dd['text'] = "Simulate 'uses Potion of True Strike'"
        self.button_dd['command'] = lambda: self.uses_call("uses Potion of True Strike")
        self.button_dd.grid(column=2, row=13)

        self.freeform_uses_test = tk.StringVar()
        self.entry_test = tk.Entry(self.debugging_buttons_frame, width=30, textvariable=self.freeform_uses_test)
        self.entry_test.grid(column=2, row=14)
        self.entry_button = ttk.Button(self.debugging_buttons_frame, text='Enter uses freeform', command=lambda: self.uses_call(self.freeform_uses_test.get()))
        self.entry_button.grid(column=2, row=15)

        self.freeform_cast_test = tk.StringVar()
        self.cast_test = tk.Entry(self.debugging_buttons_frame, width=30, textvariable=self.freeform_cast_test)
        self.cast_test.grid(column=1, row=14)
        self.cast_button = ttk.Button(self.debugging_buttons_frame, text='Enter casts freeform', command=lambda: self.casts_call(self.freeform_cast_test.get()))
        self.cast_button.grid(column=1, row=15)

        # don't run simulated looping with actual looping, or click more than once, causes two loops that get weird
        self.button4 = ttk.Button(self.debugging_buttons_frame)
        self.button4['text'] = "START loops of time passing"
        self.button4['command'] = lambda: [self.testing_logloops(), self.buffs_loop_time_passing()]
        self.button4.grid(column=0, row=14)

        self.geo_blank = ttk.Button(self.debugging_buttons_frame, text="Set geo to ''", command=lambda: app.geometry(""))
        self.geo_blank.grid(column=0, row=15)
        self.resize_test = ttk.Button(self.debugging_buttons_frame, text="resize call", command=lambda: self.resize_set_buff_window("test"))
        self.resize_test.grid(column=0, row=16)

        # testing the call functions
        self.call_testing1 = ttk.Button(self.debugging_buttons_frame, text="Simulate 'uses Summon Creature II'", command=lambda: self.uses_call("uses Summon Creature II"))
        self.call_testing1.grid(column=0, row=17)

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
        
        # when readlines is called it gets the newlines that have been written in the file since their last update and puts them
        # as seperate list items into a list
        
        buffs = self.logfile.readlines() 
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

            if self.name_stringvar.get() + " casts " in logline:
                start = logline.split(" ").index("casts")
                stop = len(logline.split(" "))
                output_string = ""
                for x in range(start, stop):
                    output_string = output_string + logline.strip().split(" ")[x] + " "
                # print(output_string[:-1]) # testing
                self.casts_call(output_string[:-1])

            if " has a timer of " in logline:
                ability_list = abilities_trigger(logline)
                # print(f"printing ability list: {ability_list}") # testing
                self.make_buff_labelframe([ability_list[0], time.time() + ability_list[1], self.ability_ref_dict[ability_list[0]]['icon']])

            if " will be available once more in " in logline:
                self.make_buff_labelframe(summons_cd_call(logline))

            if self.name_stringvar.get() + " attempts Smite Evil " in logline or self.name_stringvar.get() + " attempts Smite Good " in logline:
                self.smite_call()

        for x in self.buffs_list_frames: # removes any buffs that reach 0, makes them red if they're below 6 s
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            if x.buff_birthday < time.time() + 6:
                x['background'] = 'red'
            if x.buff_birthday < time.time():
                self.buffs_list_frames.remove(x)
                x.destroy()
                self.resize_set_buff_window('buff destroy')
        
        self.after(100, self.buffs_loop_time_passing) # 1000 works... trying 100

    def smite_call(self):
        """ handles the sequential cooldowns of smite, they don't all start CDs right when used
        but instead recharge 1 use after 10 minutes, will be able to recycle lots of this
        code for the turn undead/divine shield&might cooldowns as well... just calling
        this smite so it works for evil and good
        Maybe bard song too...
        """

        if "CD Smite" not in str([obj.buff_name for obj in self.buffs_list_frames if "CD Smite" in str(obj.buff_name)]):
            self.make_buff_labelframe(["CD Smite", time.time() + 600, "NWN-Buff-Watcher/graphics/smite_both_cd.png"])
            # print(f'in if: {[obj.buff_name for obj in self.buffs_list_frames if "CD Smite" in str(obj.buff_name)]}') # testing
        else:
            self.smite_iterator = self.smite_iterator + 1

            for smite_buff in self.buffs_list_frames:
                if "CD Smite" in str(smite_buff.buff_name):
                    self.smite_list.append(float(smite_buff.buff_birthday))
            
            self.smite_list.sort()
            squential_smite_cd = self.smite_list[-1]

            self.make_buff_labelframe([f"CD Smite {self.smite_iterator}", squential_smite_cd + 600, "NWN-Buff-Watcher/graphics/smite_both_cd.png"])

            self.smite_list = []
            # print(f'in else: {[obj.buff_name for obj in self.buffs_list_frames if "CD Smite" in str(obj.buff_name)]}') # testing

    def uses_call(self, buff_string):
        # takes the string that comes back from the main loop and compares it to a dictionary of all possible "character uses X thing" responses
        # that dictionary has the "char uses X" as the keys so it can easily return the values like duration and icon
        # much faster (I think) than the if > elif > elif... I was using to prototype, easy to put in a json and potentially easy for
        # users to add their own "unique" item uses into the json without having to know the code -- or not have access to the code
        # if/when I make a PyInstaller .exe release
        
        adding_buff = []

        # just added types to everything
        try:
            buff_type = self.use_items_dict[f'{buff_string}']['type']
        except:
            buff_type = 'other'
            print(f"EXCEPTED ON TYPE: {buff_string}")

        # the try handle "uses" lines that aren't defined in the json, otherwise they exception and stop the program
        try: 
            adding_buff.append(self.use_items_dict[f'{buff_string}']['name'])

            # handling the loremaster changes to duration for scrolls and wands
            # also checks if caster level is 1 and doesn't apply LM since the cl 1 signifies it has a default duration that isn't affected by cl
            lm_modifier = 0

            if self.lm_modifier.get() > 0 and int(self.use_items_dict[f'{buff_string}']['caster_level']) > 1:
                if buff_type == 'scroll':
                    lm_modifier = int(self.lm_modifier.get())
                    # adding_buff.append(time.time() + (int(self.use_items_dict[f'{buff_string}']['duration']) * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + self.lm_modifier.get()))) # old way
                    # print(f"scroll: {adding_buff[1]}") # testing
                    # print(f"duration in scroll: {int(self.use_items_dict[f'{buff_string}']['duration'])}") # testing
                elif buff_type == 'wand':
                    lm_modifier = ((self.lm_modifier.get() + 2 // 2) // 2)
                    # adding_buff.append(time.time() + (int(self.use_items_dict[f'{buff_string}']['duration']) * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + (self.lm_modifier.get() + 2 // 2) // 2))) # old way
                    # print(f"wand: {adding_buff[1]}") # testing
                else:
                    pass
            
            adding_buff.append(time.time() + (int(self.use_items_dict[f'{buff_string}']['duration']) * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))))

            # print(f"duration after LM ifs: {int(self.use_items_dict[f'{buff_string}']['duration'])}") # testing
            adding_buff.append(self.use_items_dict[f'{buff_string}']['icon'])

            # handling edge cases clarity
            # print(adding_buff) # testing
            if self.use_items_dict[f'{buff_string}']['name'] == "Clarity":
                if "CD Clarity" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Clarity"]:
                    adding_buff[1] = adding_buff[1] + 30
                    self.make_buff_labelframe(["CD Clarity", time.time() + 72, "NWN-Buff-Watcher/graphics/clar_cooldown.png"])
                else:
                    return

            # handling imp invis, the invis duration part for SF illu
            if self.use_items_dict[f'{buff_string}']['name'] == "Improved Invisibility": # edge case for imp invis tracking invis and concealment seperate -- on just wands of imp invis*** -- need something to juice invis on GSF/ESF and different invis lengths for different items and LM levels...
                if self.sf_illu_state.get() == 0:
                    self.make_buff_labelframe(["Invisibility", time.time() + (6 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))), "NWN-Buff-Watcher/graphics/invisibility.png"])
                elif self.sf_illu_state.get() == 1:
                    self.make_buff_labelframe(["Invisibility", time.time() + (18 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))), "NWN-Buff-Watcher/graphics/invisibility.png"])
                else:
                    self.make_buff_labelframe(["Invisibility", time.time() + (30 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))), "NWN-Buff-Watcher/graphics/invisibility.png"])

            # handling invisibility for SF illu & invis sphere
            if self.use_items_dict[f'{buff_string}']['name'] == "Invisibility" or self.use_items_dict[f'{buff_string}']['name'] == "Invisibility Sphere":
                if self.sf_illu_state.get() == 0:
                    pass
                elif self.sf_illu_state.get() == 1:
                    adding_buff[1] = adding_buff[1] + (12 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))) # only needs another 12*cl to get to 18 since it already has 6*cl as its base
                else:
                    adding_buff[1] = adding_buff[1] + (24 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))) # only needs another 24*cl to get to 30 since it already has 6*cl as its base

            # handling true seeing
            if self.use_items_dict[f'{buff_string}']['name'] == "True Seeing":
                if self.sf_div_state.get() == 0:
                    self.make_buff_labelframe(["True Seeing", time.time() + 6, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 1:
                    self.make_buff_labelframe(["True Seeing", time.time() + 12, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 2:
                    self.make_buff_labelframe(["True Seeing", time.time() + 18, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 3:
                    self.make_buff_labelframe(["True Seeing", time.time() + 30, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                else:
                    print("sf_div went wrong")

                self.make_buff_labelframe(["See Invisibility", adding_buff[1], "NWN-Buff-Watcher/graphics/see_invisibility.png"])
                self.make_buff_labelframe(["Ultravision", adding_buff[1], "NWN-Buff-Watcher/graphics/ultravision.png"])
                return

            # handling Aura of Vitality
            if self.use_items_dict[f'{buff_string}']['name'] == "Aura of Vitality":
                if self.sf_trans_state.get() == 0:
                    pass
                elif self.sf_trans_state.get() == 1:
                    adding_buff[1] = adding_buff[1] + (12 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))) # only needs another 12*cl to get to 18 since it already has 6*cl as its base
                elif self.sf_trans_state.get() == 2:
                    adding_buff[1] = adding_buff[1] + (54 * (int(self.use_items_dict[f'{buff_string}']['caster_level']) + int(lm_modifier))) # only needs another 54*cl to get to 60 (turns/level) since it already has 6*cl as its base
                else:
                    print("Something wrong with AoV")

            # handling greater resto scroll and its cooldown
            if self.use_items_dict[f'{buff_string}']['name'] == "CD Greater Restoration":
                if "CD Greater Restoration" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Greater Restoration"]:
                    pass
                else:
                    return

            # handling time stop scroll and its cooldown
            if self.use_items_dict[f"{buff_string}"]["name"] == "Time Stop":
                if "CD Time Stop" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Time Stop"]:
                    self.make_buff_labelframe(["CD Time Stop", time.time() + 240, "NWN-Buff-Watcher/graphics/time_stop_cd.png"])
                else:
                    return



            # print(f"duration just before pass to make labelframe: {int(self.use_items_dict[f'{buff_string}']['duration'])}") # testing
            self.make_buff_labelframe(adding_buff)
        except:
            print(f"EXCEPTED ON WHOLE THING: {buff_string}") # for now just fart out that it was handled, maybe later user can add to json with a buff-managing window?


    def casts_call(self, buff_string):
        # takes the string that comes back from the main loop and compares it to a dictionary of all possible "character uses X thing" responses
        # that dictionary has the "char uses X" as the keys so it can easily return the values like duration and icon
        # much faster (I think) than the if > elif > elif... I was using to prototype, easy to put in a json and potentially easy for
        # users to add their own "unique" item uses into the json without having to know the code -- or not have access to the code
        # if/when I make a PyInstaller .exe release
        
        adding_buff = []

        # just added types to everything
        # not using in casting, but keeping here for now
        try:
            buff_type = self.cast_spells_dict[f'{buff_string}']['type']
        except:
            buff_type = 'other'
            print(f"EXCEPTED ON TYPE: {buff_string}")

        # the try handle "uses" lines that aren't defined in the json, otherwise they exception and stop the program
        try: 
            adding_buff.append(self.cast_spells_dict[f'{buff_string}']['name'])

            # handling the "1" cl spells since that signifies that they aren't changed by caster level, they just get their duration
            if int(self.cast_spells_dict[f'{buff_string}']['caster_level']) > 1:
                # changed the duration to a float to handle 1.5 rounds per level on greater sanctuary
                # need to test in-game and see how this works out, if it just does 1.5 too, or if there's a break at the round/4 level
                # if there is a break... we'll need to handle its duration in its own section below
                adding_buff.append(time.time() + (float(self.cast_spells_dict[f'{buff_string}']['duration']) * int(self.cl_modifier.get())))
            else:
                adding_buff.append(time.time() + (int(self.cast_spells_dict[f'{buff_string}']['duration'])))

            adding_buff.append(self.cast_spells_dict[f'{buff_string}']['icon'])

            # handling edge cases for clarity
            # print(adding_buff) # testing
            # added a test to make sure cooldown isn't active when trying to add
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Clarity":
                if "CD Clarity" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Clarity"]:
                    adding_buff[1] = adding_buff[1] + 30
                    self.make_buff_labelframe(["CD Clarity", time.time() + 72, "NWN-Buff-Watcher/graphics/clar_cooldown.png"])
                else:
                    return

            # handling imp invis duration if character as SF illu
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Improved Invisibility": # edge case for imp invis tracking invis and concealment seperate -- on just wands of imp invis*** -- need something to juice invis on GSF/ESF and different invis lengths for different items and LM levels...
                if self.sf_illu_state.get() == 0:
                    self.make_buff_labelframe(["Invisibility", time.time() + (6 * int(self.cl_modifier.get())), "NWN-Buff-Watcher/graphics/invisibility.png"])
                elif self.sf_illu_state.get() == 1:
                    self.make_buff_labelframe(["Invisibility", time.time() + (18 * int(self.cl_modifier.get())), "NWN-Buff-Watcher/graphics/invisibility.png"])
                elif self.sf_illu_state.get() == 2:
                    self.make_buff_labelframe(["Invisibility", time.time() + (30 * int(self.cl_modifier.get())), "NWN-Buff-Watcher/graphics/invisibility.png"])
                else:
                    print("Something wrong with imp invis.")


            # handling invisibility for SF illu & invis sphere
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Invisibility" or self.cast_spells_dict[f'{buff_string}']['name'] == "Invisibility Sphere":
                if self.sf_illu_state.get() == 0:
                    pass
                elif self.sf_illu_state.get() == 1:
                    adding_buff[1] = adding_buff[1] + (12 * int(self.cl_modifier.get())) # only needs another 12*cl to get to 18 since it already has 6*cl as its base
                elif self.sf_illu_state.get() == 2:
                    adding_buff[1] = adding_buff[1] + (24 * int(self.cl_modifier.get())) # only needs another 24*cl to get to 30 since it already has 6*cl as its base
                else:
                    print("Something wrong with invis or invis sphere.")

            # handling divine might and shield duration
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Divine Shield" or self.cast_spells_dict[f'{buff_string}']['name'] == "Divine Might":
                adding_buff[1] = time.time() + (6 * self.cha_modifier.get())

            # handling divine wrath
            # uses list comprehension to make sure that the cooldown isn't already active
            # good template for other non-performance areas checking cooldowns, OK here since it's only called on DW cast
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Divine Wrath":
                if "CD Wrath" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Wrath"]:
                    adding_buff[1] = time.time() + ((3 + (self.cot_modifier.get() // 2) + self.cha_modifier.get()) * 6)
                    self.make_buff_labelframe(["CD Wrath", time.time() + 480, "NWN-Buff-Watcher/graphics/divine_wrath_cd.png"])
                    self.make_buff_labelframe(adding_buff)
                else:
                    return

            # handling true seeing
            if self.cast_spells_dict[f'{buff_string}']['name'] == "True Seeing":
                if self.sf_div_state.get() == 0:
                    self.make_buff_labelframe(["True Seeing", time.time() + 6, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 1:
                    self.make_buff_labelframe(["True Seeing", time.time() + 12, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 2:
                    self.make_buff_labelframe(["True Seeing", time.time() + 18, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                elif self.sf_div_state.get() == 3:
                    self.make_buff_labelframe(["True Seeing", time.time() + 30, "NWN-Buff-Watcher/graphics/true_seeing.png"])
                else:
                    print("sf_div went wrong")

                self.make_buff_labelframe(["See Invisibility", adding_buff[1], "NWN-Buff-Watcher/graphics/see_invisibility.png"])
                self.make_buff_labelframe(["Ultravision", adding_buff[1], "NWN-Buff-Watcher/graphics/ultravision.png"])
                return

            # handling aura of vitality
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Aura of Vitality":
                if self.sf_trans_state.get() == 0:
                    pass
                elif self.sf_trans_state.get() == 1:
                    adding_buff[1] = adding_buff[1] + (12 * int(self.cl_modifier.get())) # only needs another 12*cl to get to 18 since it already has 6*cl as its base
                elif self.sf_trans_state.get() == 2:
                    adding_buff[1] = adding_buff[1] + (54 * int(self.cl_modifier.get())) # only needs another 24*cl to get to 30 since it already has 6*cl as its base
                else:
                    print("Something wrong with AoV cast")

            # handling greater resto cooldown on cast
            if self.cast_spells_dict[f'{buff_string}']['name'] == "CD Greater Restoration":
                if "CD Greater Restoration" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Greater Restoration"]:
                    pass
                else:
                    return

            # handling greater sanctuary and its cooldown on cast
            if self.cast_spells_dict[f'{buff_string}']['name'] == "Greater Sanctuary":
                if "CD Greater Sanctuary" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Greater Sanctuary"]:
                    self.make_buff_labelframe(["CD Greater Sanctuary", time.time() + 240, "NWN-Buff-Watcher/graphics/greater_sanc_cd.png"])
                else:
                    return

            # handling time stop and its cooldown on cast
            if self.cast_spells_dict[f"{buff_string}"]["name"] == "Time Stop":
                if "CD Time Stop" not in [(obj.buff_name) for obj in self.buffs_list_frames if obj.buff_name == "CD Time Stop"]:
                    self.make_buff_labelframe(["CD Time Stop", time.time() + 240, "NWN-Buff-Watcher/graphics/time_stop_cd.png"])
                else:
                    return

            self.make_buff_labelframe(adding_buff)
        except:
            print(f"EXCEPTED ON WHOLE THING: {buff_string}") # for now just fart out that it was handled, maybe later user can add to json with a buff-managing window?


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

        self.buff_epoch = time.time()
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

        self.click_menu = tk.Menu(self, tearoff=0)
        self.innate_cascade = tk.Menu(self, tearoff=0)

        self.click_menu.add_command(label=f'{self.buff_name}')

        if self.buff_name == "Innate Ability":
            # TODO: revisit this, cascade working good, or just move back to adding the huge list since its context specific...
            self.click_menu.add_separator()
            self.click_menu.add_cascade(label="Innate Abilities:", menu=self.innate_cascade)
            self.innate_cascade.add_command(label='Darkness (Drow/Derro)', command=lambda: [self.menu_destroy_buff_labelframe(), main_frame.make_buff_labelframe(["Darkness", self.buff_epoch + (6 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/darkness.png"])])
            self.innate_cascade.add_command(label='Invis (Duergar)', command=lambda: [self.menu_destroy_buff_labelframe(), self.innate_invis_duerg()]) 
            self.innate_cascade.add_command(label='Invis (Svir/Fey/Imp)', command=lambda: [self.menu_destroy_buff_labelframe(), self.innate_invis_most()]) 
            self.innate_cascade.add_command(label='Polymorph Self (Imp)', command=lambda: [self.menu_destroy_buff_labelframe(), main_frame.make_buff_labelframe(["Polymorph Self", self.buff_epoch + (60 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/polymorph.png"])])
            self.innate_cascade.add_command(label='Warcry (Gnoll)', command=lambda: [self.menu_destroy_buff_labelframe(), main_frame.make_buff_labelframe(["Warcry", self.buff_epoch + (6 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/war_cry.png"])])

        self.click_menu.add_separator()
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

    def innate_invis_duerg(self):
        print("Innate invis fired")
        # handling invisibility for innate and SF illu
        # for whatever undocumented reason in Arelith, duergar get 2x character level to their invis
        if main_frame.sf_illu_state.get() == 0:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (6 * (main_frame.character_level.get() * 2)), "NWN-Buff-Watcher/graphics/invisibility.png"])
        elif main_frame.sf_illu_state.get() == 1:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (18 * (main_frame.character_level.get() * 2)), "NWN-Buff-Watcher/graphics/invisibility.png"])
        elif main_frame.sf_illu_state.get() == 2:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (30 * (main_frame.character_level.get() * 2)), "NWN-Buff-Watcher/graphics/invisibility.png"])
        else:
            print("Something wrong with duerg innate invis.")

    def innate_invis_most(self):
        print("Innate invis fired")
        # handling invisibility for innate and SF illu
        if main_frame.sf_illu_state.get() == 0:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (6 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/invisibility.png"])
        elif main_frame.sf_illu_state.get() == 1:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (18 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/invisibility.png"])
        elif main_frame.sf_illu_state.get() == 2:
            main_frame.make_buff_labelframe(["Invisibility", self.buff_epoch + (30 * main_frame.character_level.get()), "NWN-Buff-Watcher/graphics/invisibility.png"])
        else:
            print("Something wrong with innate invis.")

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