import tkinter as tk
from tkinter import ttk, Menu
from PIL import ImageTk, Image
import time
from tkinter.filedialog import askopenfile

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.grid(column=0, row=0)

        self.buffs_list_frames = []

        self.name_stringvar = tk.StringVar() # setting in constructor so doesn't error when opening file when not set

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(fill="both", side="right")

        self.button1 = ttk.Button(self.buttons_frame)
        self.button1['text'] = "Simulate frame list appended True Strike"
        self.button1['command'] = lambda: self.buffs_frame_list_is_appended(["True Strike", time.time() + 9, "arelith_ui\Is_x1trustr.png"])
        self.button1.grid(column=0, row=0)

        self.button2 = ttk.Button(self.buttons_frame)
        self.button2['text'] = "Simulate frame list appended Bulls"
        self.button2['command'] = lambda: self.buffs_frame_list_is_appended(["Bulls", time.time() + 1080, "arelith_ui\Is_endurce.png"])
        self.button2.grid(column=0, row=1)

        self.button0 = ttk.Button(self.buttons_frame)
        self.button0['text'] = "Simulate frame list appended Endurance"
        self.button0['command'] = lambda: self.buffs_frame_list_is_appended(["Endurance", time.time() + 1080, "arelith_ui\Is_bullstr.png"])
        self.button0.grid(column=0, row=2)

        self.button4 = ttk.Button(self.buttons_frame)
        self.button4['text'] = "START loops of time passing"
        self.button4['command'] = lambda: self.buffs_loop_time_passing()
        self.button4.grid(column=0, row=4)

        self.buff_holding_frame = tk.Frame(self, bd=1, relief='solid', width=500, height=80)
        self.buff_holding_frame.pack(side="left")
        self.buff_holding_frame.pack_propagate(0)

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
        self.after(100, self.buffs_loop_time_passing)


    def buffs_loop_time_passing(self):
        
        # buffs = self.logfile.readlines()
        # print(buffs) # debugging
        # if self.name_stringvar.get() + " uses Potion of Endurance" in str(buffs):
        #     print("Bear fired.")
        
        """ TODO: only calculate all the time() countdowns in one place, but move and
        display them in more if needed, process savings?
        """

        for x in self.buffs_list_frames:
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            if x.buff_birthday < time.time() + 6:
                x['background'] = 'red'
            if x.buff_birthday < time.time():
                self.buffs_list_frames.remove(x)
                x.destroy()
        
        self.after(1000, self.buffs_loop_time_passing)

    def buffs_frame_list_is_appended(self, added_buff):
        """ includes name, bday, duration
        """ 

        self.buff_frame = tk.LabelFrame(self.buff_holding_frame, borderwidth=1, text=added_buff[0][0:4], labelanchor="n")
        # TODO width isn't getting through...
        
        # self.buff_frame.pack() # return to grid, move the grid/pack to the display function where it can destroy/display the frames
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

        print(self.buffs_list_frames)
        print(self.buff_frame.buff_timer.get())

        self.buffs_display_nicely()

    def buffs_display_nicely(self):
        """ used to put into string and format, now
        want to show frame grid and graphic with
        fancy for loop to make list of frames
        """
        # self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z['text'], reverse=True) # sort alphabetically
        self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z.buff_timer.get(), reverse=True) # sort remaining time
        for x in self.buffs_list_frames:
            x.pack_forget()
            x.pack(side="right")



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('NWN Buff Watcher')
        # self.geometry('300x50')
        self.attributes("-topmost", True)

        self.option_add('*tearOff', False) # docs said something about this... not sure what it changes

        # menu for file > open
        self.menubar = Menu(self)
        self.config(menu=self.menubar)
        self.file_menu = Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Name', command=lambda: main_frame.character_name())
        self.file_menu.add_command(label='Open...', command=lambda: main_frame.open_file())

        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy)
        self.menubar.add_cascade(label="File", menu=self.file_menu)


if __name__ == "__main__":
    app = App()
    main_frame = MainFrame(app)
    app.mainloop()