"""

Program: buff_watcher.py
Author: Mattamue
Last date modified: 03/25/2021
The purpose of this program is to watch
the chat log for buff actions and spells
then create a python window that floats over
everything and tracks when buffs expire

# https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file
# follow.py
# Follow a file like tail -f.

""" 

import time
from tkinter import *

def follow(thefile): # follows the file, returns (yields) each new line
    thefile.seek(0,2) # goes to the last line of the file, column 0, IE line 12355
    while True: # keeps looping until it yeilds
        line = thefile.readline()
        '''
        reads the 12355 line, should always be blank the first pass
        through?, when the line is eventually filled with
        data then we don't sleep and continue, and instead
        yeild'''
        if not line: # if line is blank (null?) then we're at EOF
            time.sleep(0.1) # sleep for 0.1 seconds
            continue # this wraps back up and reads the 12355 line again
        yield line
        '''
        This is a "generator" that returns the line, but after
        the line is returned the program COMES BACK TO THE FUNCTION
        and keeps running at the "while True" line, it doesn't
        go up to the seek function...

        I think this means it was always work its way through the
        newlines but I don't undestand how its moving the "reader"
        part up in the file, if the seeker started at line 12355
        and we come back to the top of the "while True" what is
        moving the readline down to 12356 and so forth? Is that
        also because yield is turning it into a "generator?" and
        is keeping track somehow? I think so... when testing I
        added a print above the while True and it was only called
        once. So I know it doesn't reach back up outside of the
        white True loop, but I still don't understand how the
        reader on the file moves to the next line.
        
        When testing I also tried to add a .skeek into the while
        True loop and that broke something, like even though I
        wasn't setting the .seek to anything I think it was
        just moving the "reader" to the end of the file, even
        if I was just trying to print its status.
        https://www.guru99.com/python-yield-return-generator.html
        '''



""" can't call this in a loop because it just keeps re-creating the window...
def buff_drawer(buff): 
    root = Tk()
    my_buff = Label(root, text = buff)
    my_buff.pack()
    root.mainloop() """

""" my first attempt
if __name__ == '__main__':
    logfile = open("/Users/Matta/Documents/Neverwinter Nights/logs/nwclientLog1.txt","r")
    loglines = follow(logfile)
    for line in loglines:
        if 'uses Potion of Bull\'s Strength' in line:
            buff_drawer("Bulls") 
        continue """


# prior working main, this just prints each line

if __name__ == '__main__':
    logfile = open("/Users/Matta/Documents/Neverwinter Nights/logs/nwclientLog1.txt","r")
    loglines = follow(logfile)
    for line in loglines:
        print(line)