###Main GUI Program Version###

from tkinter import *

PARALLEL_MODE = False
#Button Callbacks
def addFilter():
    print("Hello,world!")

def changeMode():
    #They should select the mode before 
    global PARALLEL_MODE
    if(PARALLEL_MODE):
        mode.config(text="Serial")
        PARALLEL_MODE = False
    else:
        mode.config(text="Parallel")
        PARALLEL_MODE = True

#BASE ROOT WINDOW
root = Tk()
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(700, 150))
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

#BUTTONS
add = Button(root,text="Add",command=addFilter, width=25)
add.place(relx=0.65,rely=0.1)
edit = Button(root,text="Edit",command=addFilter, width=25)
edit.place(relx=0.65,rely=0.3)
delete = Button(root,text="Delete",command=addFilter, width=25)
delete.place(relx=0.65,rely=0.5)
mode = Button(root,text="Serial",command=changeMode, width=25, state=DISABLED)
mode.place(relx=0.65,rely=0.7)

#SERIAL DESIGN
filterOne = Label(root,text="First Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg="green")
filterOne.place(relx=0.2,rely=0.4)
filterTwo = Label(root,text="Second Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg="green")
filterTwo.place(relx=0.4,rely=0.4)
lineInput = Label(root,borderwidth=0,text="IN --------->",relief="solid",padx=0,pady=1)
lineInput.place(relx=0.085,rely=0.43)
mainloop()

