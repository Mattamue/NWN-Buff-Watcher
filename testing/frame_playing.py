import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        options = {'padx': 5, 'pady': 5}

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.pack(**options)

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack(**options)

        self.buffs_list = {"key1": ["Bulls", "duration", "birthday", "(b+d)-n", "icon"]}

        # show the frame on the container
        self.pack(**options)

    def button_clicked(self):
        print(self.buffs_list)
        accumulator = 0
        self.buffs_list["key2"] = ["Bears", "duration", "birthday", "(b+d)-n", "icon"]
        for key, value in self.buffs_list.items():
            key = tk.Frame(self)
            
            key.pack()
            print(key)
            print(value)






class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('My Awesome App')
        self.geometry('300x100')


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    app.mainloop()