###Main GUI Program Version###

from tkinter import *
import string
import serial 
global PARALLEL_MODE 
PARALLEL_MODE = True
FILTER_NAMES = ["Low Pass","High Pass","Echo","Noise Gate","Distortion","Compression"]
FILTER_ONE_SET = False
FILTER_TWO_SET = False
MIX_SET = False
FILTER_ONE = []
FILTER_TWO = []
MIX_SETUP = []

#FILTER PARAMS
LOW_HIGH_PASS = ['Cutoff Frequency','Roll Off']
ECHO = ['Room Size','Echo Gain','Decay']
NOISE_GATE = ['Threshold']
DISTORTION = ['Min Boundary','Max Boundarys','Threshold']
COMPRESSION = ['Threshold','Ratio']

##############################################################
##############################################################
############ COMMUNICATION METHODS/ SERIAL STUFF #############
##############################################################
##############################################################

def sendDataStream(msg):
    #Send data via stream
    ser = serial.Serial('/dev/ttyACM0', 9600)
    ser.write(msg)
    while(True):
        data_raw = ser.read(1)
        print(data_raw)
def sendMode():
    global PARALLEL_MODE
    if(PARALLEL_MODE):
        sendDataStream("MP")
    else:
        sendDataStream("MS")
def sendFilter(filter_id):
    msg = "F" #Add/Edit the filter
    msg+= str(filter_id) + "X"
    if(filter_id == 1):

        for param in FILTER_ONE:
            msg += str(param) + "X"
    else:
        for param in FILTER_TWO:
            msg += str(param) + "X"
    print(msg)
    sendDataStream(msg)
def sendDelete(filter_id):
    msg = "D" + str(filter_id) #Delete the filter
    sendDataStream(msg)
def updateMix():
    pass

##############################################################
##############################################################
############ GUI/ BUTTON CALLBACK/ MAIN PRG. STUFF ###########
##############################################################
##############################################################

def addFilter(filter_id):
    filterPop = Toplevel()
    filterPop.geometry('{}x{}'.format(215, 300))
    filterList = Listbox(filterPop)
    filterList.place(relx=0.12,rely=0.1)

    for fil in FILTER_NAMES:
        filterList.insert(END, fil)
    editOne = Button(filterPop,text="Add Filter",command= lambda: placeFilter(filter_id,filterPop,filterList.get(filterList.curselection())
),width=15)
    editOne.place(relx=0.12,rely=0.8)
    

def placeFilter(filter_id,filterPop,selectedFilter):
    filterPop.destroy()
    if(filter_id == 1):
         global FILTER_ONE_SET
         FILTER_ONE_SET = True
         filterOne.configure(bg="green",text=selectedFilter)
         FILTER_ONE.append(FILTER_NAMES.index(selectedFilter))
    else:
        global FILTER_TWO_SET
        FILTER_TWO_SET = True
        filterTwo.configure(bg="green",text=selectedFilter)
        FILTER_TWO.append(FILTER_NAMES.index(selectedFilter))
    print(selectedFilter)
     
def changeMode():
    #They should select the mode before 
    global PARALLEL_MODE
    if(PARALLEL_MODE):
        mode.config(text="Serial")
        PARALLEL_MODE = False
    else:
        mode.config(text="Parallel")
        PARALLEL_MODE = True

def filterTwoClick(event=None):
    if(FILTER_ONE_SET):
        
        if(not(FILTER_TWO_SET)):
            #let them add the filter
            addFilter(2)
        else:
            #show the filter parameters
            editFilter(2)

def filterOneClick(event=None):
    if(not(FILTER_ONE_SET)):
        addFilter(1)
    else:
        #show the filter parameters
        editFilter(1)

def mixClick(event=None):
    if(MIX_SET):
        #edit the mix settings
        editMix()
    else:
        #add a mix setting
        print("create mix settings")
        
def editFilter(filter_id):

  #Give them the edit window, allow them to update the parameters
    filterParams = Toplevel()
    filterParams.geometry('{}x{}'.format(215, 300))
    param_entry = list()
    label_entry = list()
    
    if(filter_id == 1):
        print(FILTER_ONE)
        params = filterParam(FILTER_ONE[0])
        index_filter = FILTER_ONE[0]
    else:
        print(FILTER_TWO)
        params = filterParam(FILTER_TWO[0])
        index_filter = FILTER_TWO[0]

    for i in range(0,len(params)):
        label_entry.append(Label(filterParams,text=params[i]))
        label_entry[i].pack()
        param_entry.append(Entry(filterParams))
        param_entry[i].pack()
        if((filter_id == 1) and (len(FILTER_ONE) > 1)):
            param_entry[i].insert(0,FILTER_ONE[i+1])
        elif((filter_id == 2) and (len(FILTER_TWO) > 1)):
            param_entry[i].insert(0,FILTER_TWO[i+1])
    

    updateButton = Button(filterParams,text="Set", command = lambda: updateFilter(filter_id,param_entry,filterParams))
    updateButton.pack()

    deleteButton = Button(filterParams,text="Delete",command = lambda: deleteFilter(filter_id,filterParams))
    deleteButton.pack()
 

def updateFilter(filter_id,param_entry,filterParams):
    #set the new settings for the filter
    global FILTER_ONE
    global FILTER_TWO
    if((len(FILTER_ONE) > 1) and (filter_id == 1)):
        tmp = FILTER_ONE[0]
        FILTER_ONE = list()
        FILTER_ONE.append(tmp)
    elif((len(FILTER_TWO) > 1)and (filter_id == 2)):
        tmp = FILTER_TWO[0]
        FILTER_TWO = list()
        FILTER_TWO.append(tmp)
    for i in range(0,len(param_entry)):
        #print(param_entry[i].get())
        if(len(FILTER_ONE) == 0):
            #it must be filter 2
            FILTER_TWO.append(str(param_entry[i].get()).strip(string.ascii_letters))
        elif(len(FILTER_TWO) == 0):
            #it must be filter 1
            FILTER_ONE.append(str(param_entry[i].get()).strip(string.ascii_letters))
        elif(filter_id == 1):
            FILTER_ONE.append(str(param_entry[i].get()).strip(string.ascii_letters))
        elif(filter_id == 2):
            FILTER_TWO.append(str(param_entry[i].get()).strip(string.ascii_letters))
    filterParams.destroy()
    sendFilter(filter_id)
    
def deleteFilter(filter_id,filterParams):
    
    global FILTER_ONE
    global FILTER_TWO
    global FILTER_ONE_SET
    global FILTER_TWO_SET
    if((filter_id == 1) and (FILTER_TWO_SET)):#ensure we don't delete filter 1 before filter 2
        pass
    else: 
        if(filter_id== 1):
            FILTER_ONE = list()
            FILTER_ONE_SET = False
            filterOne.configure(bg="red",text="Filter One")
        else:
            FILTER_TWO = list()
            FILTER_TWO_SET = False
            filterTwo.configure(bg="red",text="Filter Two")
            
        filterParams.destroy()
def editMix():
    pass

def filterParam(filterID):
    
    if((filterID == 0) or (filterID == 1)):
        return LOW_HIGH_PASS
    elif(filterID == 2):
        return ECHO
    elif(filterID == 3):
        return NOISE_GATE
    elif(filterID == 4):
        return DISTORTION
    elif(filterID == 5):
        return COMPRESSION

#BASE ROOT WINDOW
root = Tk()
root.title("Filter Settings")
root.resizable(width=False, height=False)
root.geometry('{}x{}'.format(700, 150))
root.eval('tk::PlaceWindow %s center' % root.winfo_pathname(root.winfo_id()))

#ASK IF THEY WANT TO DO PARALLEL OR SERIAL

not_chosen = True
while(not_chosen):

    print("Choose Parallel (P) or Serial (S) mode.")
    mode_choice = str(raw_input())
    global PAE
    if((mode_choice == "S") or (mode_choice == "s")):
        PARALLEL_MODE = False
        break
    elif((mode_choice == "P") or (mode_choice == "p")):
        PARALLEL_MODE = True
        break
sendMode()
if(PARALLEL_MODE == False):
    #SERIAL DESIGN
    lineInput = Label(root,borderwidth=0,text="IN --------->",relief="solid",padx=0,pady=1)
    lineInput.place(relx=0.085,rely=0.43)
    lineSeq = Label(root,borderwidth=0,text="-----------------------------------------------> OUT",relief="solid",padx=0,pady=1)
    lineSeq.place(relx=0.25,rely=0.43)
    filterOne = Label(root,text="First Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg=("green"if(FILTER_ONE_SET) else"red"))
    filterOne.place(relx=0.2,rely=0.4)
    filterOne.bind("<Button-1>",filterOneClick)
    filterTwo = Label(root,text="Second Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg=("green"if(FILTER_TWO_SET)else"red"))
    filterTwo.place(relx=0.4,rely=0.4)
    filterTwo.bind("<Button-1>",filterTwoClick)
else:

    #PARALLEL DESIGN
    lineInput = Label(root,borderwidth=0,text="IN ---------",relief="solid",padx=0,pady=1)
    lineInput.place(relx=0.085,rely=0.43)
    lineUp = Label(root,wraplength=1,borderwidth=0,text="||||",relief="solid",padx=0,pady=0)
    lineUp.place(relx=0.19,rely=0.28)
    lineSeq = Label(root,borderwidth=0,text="--------------------------------------------------> OUT",relief="solid",padx=0,pady=1)
    lineSeq.place(relx=0.4,rely=0.43)
    lineDown = Label(root,wraplength=1,borderwidth=0,text="||||",relief="solid",padx=0,pady=0)
    lineDown.place(relx=0.38,rely=0.27)
    lineTop = Label(root,borderwidth=0,text="---------------------",relief="solid",padx=0,pady=1)
    lineTop.place(relx=0.2,rely=0.24)
    lineBottom = Label(root,borderwidth=0,text="---------------------",relief="solid",padx=0,pady=1)
    lineBottom.place(relx=0.2,rely=0.64)
    filterOne = Label(root,text="First Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg="red")
    filterOne.place(relx=0.2,rely=0.2)
    filterOne.bind("<Button-1>",filterOneClick)
    filterTwo = Label(root,text="Second Filter",borderwidth=2,relief="solid",padx=4,pady=4,bg="red")
    filterTwo.place(relx=0.2,rely=0.6)
    filterTwo.bind("<Button-1>",filterTwoClick)
    mixFilter = Label(root,text="Mix",borderwidth=2,relief="solid",padx=4,pady=4,bg="green")
    mixFilter.place(relx=0.37,rely=0.41)
    mixFilter.bind("<Button-1>",mixClick)
    
currentMode = Label(root,text="Mode: "+("Parallel"if(PARALLEL_MODE) else"Serial"))
currentMode.place(relx=0,rely=0)
mainloop()

