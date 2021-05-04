"""

Program: tk_tester.py
Author: Mattamue
Last date modified: 02/27/2021
Test out TK functionality
Adding stuff
Giving it a timer
Removing it when the timer is up


""" 

import tkinter
import time
import os as os

def follow_test():
    buff.config(text="Does this work?")
    logfile = open("/Users/Matta/Documents/Neverwinter Nights/logs/nwclientLog1.txt","r")
    logfile.seek(0,2)
    while True:
        line = logfile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

def pick_dinner():
    buff.config(text="Worse than picking lunch!")

# Setting up the Main Application Window
root = tkinter.Tk()
root.title("Title of the window.")

buff = tkinter.Label(root, text="Buff")

buff.grid(row=4)

button1 = tkinter.Button(root, text='Start Log watcher', width=25, command=follow_test).grid(row=5)

# This is the main loop that keeps the window "running"


if __name__ == '__main__':


    root.mainloop()

    # logfile = open(getFilePath("nwclientLog1.txt"),"r")

    # logfile = open("/Users/Matta/Documents/Neverwinter Nights/logs/nwclientLog1.txt","r")
    # loglines = follow(logfile)
    # for line in loglines:
        # print(line)