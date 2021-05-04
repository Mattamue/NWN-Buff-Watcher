import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


class MainFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # this goes into all of the ".pack(**options)" fields
        options = {'padx': 15, 'pady': 15}

        # label
        self.label = ttk.Label(self, text='Hello, Tkinter!')
        self.label.pack(**options)
        """
        This uses **options because it unpacks the dictionary into arguments,
        essentially the same as 'self.label.pack(padx=15, pady=15)' which
        would be the basic way to enter one just one pack.
        *options works with lists
        **options works with dictionaries
        https://docs.python.org/3.7/tutorial/controlflow.html#unpacking-argument-lists
        """

        # button
        self.button = ttk.Button(self, text='Click Me')
        self.button['command'] = self.button_clicked
        self.button.pack(**options)

        # show the frame on the container
        self.pack()

        # making another frame inside the frame... with a label
        self.frame1 = ttk.LabelFrame(self, text="Frame within the \"frame\"")
        self.frame1.pack(**options)
        self.button_frame = ttk.Label(self.frame1, text="I'm a label.")
        self.button_frame.pack(**options)

    def button_clicked(self):
        showinfo(title='Information',
                message='Hello, Tkinter!')


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # configure the root window
        self.title('My Awesome App')
        self.geometry('300x50')
        self.attributes("-topmost", True)


if __name__ == "__main__":
    app = App()
    frame = MainFrame(app)
    app.mainloop()