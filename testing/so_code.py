import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.grid(column=0, row=0)

        self.buffs_list_frames = []

        self.button1 = ttk.Button(self)
        self.button1['text'] = "Simulate frame list appended True Strike"
        self.button1['command'] = lambda: self.buffs_frame_list_is_appended(["True Strike", time.time() + 9])
        self.button1.grid(column=0, row=0)

        self.button2 = ttk.Button(self)
        self.button2['text'] = "Simulate frame list appended Bulls"
        self.button2['command'] = lambda: self.buffs_frame_list_is_appended(["Bulls", time.time() + 1080])
        self.button2.grid(column=0, row=1)

        self.button0 = ttk.Button(self)
        self.button0['text'] = "Simulate frame list appended Endurance"
        self.button0['command'] = lambda: self.buffs_frame_list_is_appended(["Endurance", time.time() + 1080])
        self.button0.grid(column=0, row=2)

        self.button3 = ttk.Button(self)
        self.button3['text'] = "Simulate frame list put into .grid() and displayed"
        self.button3['command'] = lambda: self.buffs_display_nicely()
        self.button3.grid(column=0, row=3)

        self.button4 = ttk.Button(self)
        self.button4['text'] = "START loops of time passing"
        self.button4['command'] = lambda: self.buffs_loop_time_passing()
        self.button4.grid(column=0, row=4)

        self.test_label_frame = ttk.LabelFrame(self, text="Testing putting buffs into a frame with grid")
        self.test_label_frame.grid(column=1, row=0)


    def buffs_loop_time_passing(self):
        for x in self.buffs_list_frames:
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            if x.buff_birthday < time.time() + 6:
                x['background'] = 'red'
            if x.buff_birthday < time.time():
                self.buffs_list_frames.remove(x)
                x.destroy()
        self.after(1000, self.buffs_loop_time_passing)

    def buffs_frame_list_is_appended(self, added_buff):
        """ makes the buff frame and adds to the list of frame widgets
        """ 

        self.buff_frame = tk.LabelFrame(self.test_label_frame, borderwidth=1, text=added_buff[0][0:4], labelanchor="n") 

        # self.buff_frame.buff_image_reference = ImageTk.PhotoImage(Image.open(added_buff[2]))
        # self.buff_frame.buff_image_label = ttk.Label(self.buff_frame, image=self.buff_frame.buff_image_reference)
        # self.buff_frame.buff_image_label.image_keep = self.buff_frame.buff_image_reference
        # self.buff_frame.buff_image_label.grid(column=0, row=0)
        self.buff_frame.buff_birthday = added_buff[1]
        self.buff_frame.buff_timer = tk.StringVar()
        self.buff_frame.buff_timer.set(f"{self.buff_frame.buff_birthday - time.time():.1f}s")
        self.buff_frame.buff_label = ttk.Label(self.buff_frame, textvariable=self.buff_frame.buff_timer)
        self.buff_frame.buff_label.grid(column=0, row=1)
        self.buffs_list_frames.append(self.buff_frame)

        self.buffs_display_nicely()

    def buffs_display_nicely(self):
        """ takes the list of frames, sorts by name, and .grids()s them into the test frame
        """
        self.buffs_list_frames = sorted(self.buffs_list_frames, key=lambda z: z['text'])
        print(f"sorted? {self.buffs_list_frames}")
        j = 0
        for x in self.buffs_list_frames:
            x.grid(row=0, column=j)
            j += 1

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('NWN Buff Watcher')
        self.geometry('300x50')

if __name__ == "__main__":
    app = App()
    main_frame = MainFrame(app)
    app.mainloop()