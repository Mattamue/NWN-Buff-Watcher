from tkinter import *
import tkinter

top = Tk()

mb=  Menubutton ( top, text="condiments", relief=RAISED )
mb.grid()
mb.menu =  Menu ( mb, tearoff = 0 )
mb["menu"] =  mb.menu

mayoVar = IntVar()
ketchVar = IntVar()

mb.menu.add_separator()
mb.menu.add_command(label='Exit', command=top.destroy)


        # self.menu_button = ttk.Menubutton(self.buttons_frame, text="Settings")
        # self.menu_button.grid(column=0, row=1, sticky='ew')
        # self.file_menu = Menu(self.menu_button, tearoff=0)
        # self.file_menu.add_command(label='Name', command=lambda: main_frame.character_name())
        # self.file_menu.add_command(label='Open...', command=lambda: main_frame.open_file())
        # self.file_menu.add_separator()
        # self.file_menu.add_command(label='Exit', command=self.destroy)
        # self.menu_button["menu"] = Menu1

mb.pack()
top.mainloop()