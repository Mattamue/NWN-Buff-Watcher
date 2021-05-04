import tkinter
import time

window = tkinter.Tk()

window.title('NWN Buff Watcher')

logfile = open("/Users/Matta/Documents/Neverwinter Nights/logs/nwclientLog1.txt","r")

buffs_list = []
rest_wipe = False
buffs_stringvar = tkinter.StringVar()
char_name = '"Paladin"'

def go_to_end_first(): # this goes to the end of the file
    global logfile
    logfile.seek(0, 2)
    window.after(100, test_button)

def buffs_rest(): # this goes to the end of the file
    global rest_wipe
    rest_wipe = True

def test_button():
    global logfile
    global buffs_list
    global buffs_display
    global rest_wipe
    global buffs_stringvar
    global char_name
    buffs = logfile.readlines()

    # print(f"list: {buffs}") # for testing
    # print(str(f"string: {buffs}")) # testing
    # print(f" buffs list: {buffs_list}")

    if char_name + " uses Potion of Endurance" in str(buffs):
        # print("Bear fired.")
        buffs_list.append(["Endurance", time.time() + 1080])
    elif char_name + " uses Potion of Cat\\'s Grace" in str(buffs):
        # print("Cat fired.")
        buffs_list.append(["Cat", time.time() + 1080])
    elif char_name + " uses Potion of Bull\\'s Strength" in str(buffs):
        # print("Bull fired.")
        buffs_list.append(["Bull", time.time() + 1080])
    elif char_name + " uses Potion of Owl\\'s Wisdom" in str(buffs):
        # print("Owl fired.")
        buffs_list.append(["Owl", time.time() + 1080])
    elif char_name + " uses Potion of Fox\\'s Cunning" in str(buffs):
        # print("Fox fired.")
        buffs_list.append(["Fox", time.time() + 1080])
    elif char_name + " uses Potion of Clarity" in str(buffs):
        # print("Clarity fired.")
        buffs_list.append(["*CLARITY*", time.time() + 48])
        buffs_list.append(["Clarity Cooldown", time.time() + 72])
    elif char_name + " uses Potion of Eagle\\'s Splendor" in str(buffs): # not firing, because of \'s?
        # print("Eagle fired.")
        buffs_list.append(["Eagle", time.time() + 1080])
    elif char_name + " uses Potion of Barkskin" in str(buffs):
        # print("Bark fired.")
        buffs_list.append(["Barkskin", time.time() + 1080])
    elif char_name + " uses Potion of True Strike" in str(buffs):
        # print("TS fired.")
        buffs_list.append(["*TRUE STRIKE*", time.time() + 9])
    elif char_name + " uses Potion of Freedom" in str(buffs):
        # print("Freedom fired.")
        buffs_list.append(["Freedom", time.time() + 2520])
    elif char_name + " uses Potion of Speed" in str(buffs):
        # print("Haste fired.")
        buffs_list.append(["*HASTE*", time.time() + 30])
    elif char_name + " uses Shield" in str(buffs):
        # print("Shield fired.")
        buffs_list.append(["Shield", time.time() + 300])
    
    buffs_list = sorted(buffs_list)
    
    buffs_display = ""
    
    for x in buffs_list:
        if x[1] - time.time() < 0:
            rem = x
            buffs_list.remove(rem)
    
    for x in buffs_list:
        padding_buff = 22 - len(x[0])
        padding_time = 7 - len(str(f"{x[1] - time.time():,.1f}"))
        buffs_display = buffs_display + f"{x[0]}{padding_buff * ' '}:: {padding_time * ' '}{x[1] - time.time():,.1f}s\n"
    
    buffs_stringvar.set(buffs_display)
    
    # print(f"buffs_display: {buffs_display}")
    
    label1 = tkinter.Label(window, justify='left', font=("Courier", 8), textvariable=buffs_stringvar)
    label1.grid(sticky="NW", row=0, column=1)
    # label1.config(text=buffs_display)
    
    if rest_wipe == True:
        rest_wipe = False
        buffs_display = " "
        buffs_list = []
        buffs_stringvar.set(buffs_display)
    
    window.after(1000, test_button)


button1 = tkinter.Button(window, text="Start", command=go_to_end_first).grid(sticky="NW", row=0, column=0)
button2 = tkinter.Button(window, text="Rest", command=buffs_rest).grid(sticky="NW", row=1, column=0)

window.attributes("-topmost", True)
window.mainloop()