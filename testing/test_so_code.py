"""
from TheLizzard on Stackoverflow
"""


import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import time

class MainFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.buffs_list_frames = []

        self.button1 = ttk.Button(self, text="Simulate frame list appended True Strike",
                                  command=lambda: self.buffs_frame_list_is_appended("True Strike", 9))
        self.button1.grid(column=0, row=0)

        self.button2 = ttk.Button(self, text="Simulate frame list appended Bulls",
                                  command=lambda: self.buffs_frame_list_is_appended("Bulls", 1080))
        self.button2.grid(column=0, row=1)

        self.button0 = ttk.Button(self, text="Simulate frame list appended Endurance",
                                  command=lambda: self.buffs_frame_list_is_appended("Endurance", 1080))
        self.button0.grid(column=0, row=2)

        self.button4 = ttk.Button(self, text="START loops of time passing",
                                  command=self.buffs_loop_time_passing)
        self.button4.grid(column=0, row=3)

        self.test_label_frame = ttk.LabelFrame(self, text="Testing putting buffs into a frame with grid")
        self.test_label_frame.grid(column=1, row=0)

    def buffs_loop_time_passing(self):
        for x in self.buffs_list_frames:
            x.buff_timer.set(f"{x.buff_birthday - time.time():.1f}s")
            time_now = time.time()
            if x.buff_birthday < time_now + 6:
                x.config(bg="red")
            if x.buff_birthday < time_now:
                self.buffs_list_frames.remove(x)
                x.destroy()
        self.after(100, self.buffs_loop_time_passing)

    def buffs_frame_list_is_appended(self, added_buff, time_alive):
        """ makes the buff frame and adds to the list of frame widgets
        """ 
        buff_frame = tk.LabelFrame(self.test_label_frame, borderwidth=1,
                                   text=added_buff[:4], labelanchor="n") 

        # buff_frame.buff_image_reference = ImageTk.PhotoImage(Image.open(added_buff[2]), master=self)
        # buff_frame.buff_image_label = ttk.Label(buff_frame, image=buff_frame.buff_image_reference)
        # buff_frame.buff_image_label.image_keep = buff_frame.buff_image_reference
        # buff_frame.buff_image_label.grid(column=0, row=0)
        buff_frame.buff_birthday = time.time() + time_alive
        buff_frame.buff_timer = tk.StringVar(master=self)
        buff_frame.buff_timer.set(f"{buff_frame.buff_birthday - time.time():.1f}s")
        buff_frame.buff_label = ttk.Label(buff_frame,
                                          textvariable=buff_frame.buff_timer)
        buff_frame.buff_label.grid(column=0, row=1)
        buff_frame.pack(side="right", anchor="e")
        self.buffs_list_frames.append(buff_frame)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title("NWN Buff Watcher")
        # self.geometry("300x50")


if __name__ == "__main__":
    app = App()
    main_frame = MainFrame(app)
    main_frame.pack()
    app.mainloop()