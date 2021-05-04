""" Doesn't do what I want, only makes topmost for a second to take focus...
"""


#lift/lower/raise and topmost test
#variation of tkinter test set up
#____________________________
from tkinter import *
root = Tk()
root.wm_attributes('-fullscreen', True) #create a clean visual test environment
root.configure(background='linen')
scrW = root.winfo_screenwidth() # use commands to get screenwidth and height
scrH = root.winfo_screenheight()  #oddly - not always = fullscreen
wholescreen = str(900) + "x" + str(500)
top1 = Toplevel(root, bg="light blue")
top1.geometry(wholescreen +"+100"+"+100")
top1.title("Top 1 Window")
b1=Button(top1, text="end it all", command=root.destroy)
b1.grid(row=0,column=0,ipadx=10, ipady=10, pady=5, padx=5, sticky = W+N)
#____________________________remember root.mainloop()
#toplevels purposefully offset for demonstration
 
top2= Toplevel(root, bg="ivory")
top2.geometry(wholescreen)
top2.title("Top 2 Window")
 
b2=Button(top2, text="egress", command=root.destroy)
b2.grid(row=0,column=0,ipadx=10, ipady=10, pady=5, padx=5)
 
# in this case using lambda is clearer code than a function
b3=Button(top1,text="1. lift top2", command= lambda: top2.lift(aboveThis=None))
b3.grid(row=1,column=1, ipadx=10, ipady=10, pady=5, padx=5)
 
b4=Button(top2,text="2. lift top1", command= lambda: top1.lift(aboveThis=None))
b4.grid(row=1,column=1, ipadx=10, ipady=10, pady=5, padx=5)
 
root.update() # position in process for this update is CRITICAL
 
top1.wm_attributes("-topmost", 1)  # make sure top1 is on top to start
top1.wm_attributes("-topmost", 0)  # but is not stuck on top all the time
 
root.mainloop()