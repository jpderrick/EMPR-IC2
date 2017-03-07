import serial
##### MODE #####
#represented as a 1 for parallel and 0 for serial

#we're going to assume 2 filters in use at most, whether that be in parallel or in series

#CURRENT SETUP VARIABLES
PARALLEL_MODE = True
FILTERS = list()
MIXER = list()
FILTER_PARAMS = list()
FILTER_NAMES = list()
LIST_OF_FILTERS = [['id','name','param T/F','param T/F', '....']]

def getMode():
    # Request the Current mode setup from the mbed board
    # Mode =  1 => PARALLEL MODE
    raw_req = sendDataStream(1)
    if(raw_req == 1):
        PARALLEL_MODE = True


def getMix():
    #Get the mixing values
    #raw_req = sendDataStream(6)
    #MIXER.append(raw_req[1])
    #MIXER.append(raw_req[2])
    pass

def getFilters():
    #get all of the filters in the fx chain
    raw_req = sendDataStream(2)
    #print(raw_req)
    FILTERS[:] = []
    for i in range(1,len(raw_req)-2):
        #print(raw_req[i])
        FILTERS.append(raw_req[i])
        #print(FILTERS)
        
    #print(FILTERS)
    #some test data, returns a list of filter ids
    

def getFilterParams():
    #get the parameters of all filters
    FILTER_PARAMS[:] = []
    for i in range(0,len(FILTERS)):
        raw_req = sendDataStream(3,FILTERS[i])
        FILTER_PARAMS.append([])
        for x in range(1,len(raw_req)):
            FILTER_PARAMS[i].append(raw_req[x])

def setFilterParams(filterID,params):
    #send an updated set of paramters for a filter
    pass

def initialSetupGatherData():
    #gather all the data we need
    getMode()
    getFilters()
    getFilterParams()
    listFilters()
    if(PARALLEL_MODE):
        getMix()
    
def sendDataStream(code,data=""):
    #Send something via serial usb
    #####ENUMS#####
        #1 = get mode
        #2 = get filters
        #3 = get filter params (by id)
        #4 = update parameters
        #5 = update mode
        #6 = get mix values

    msg = ""
    ret = False
 
    if(data == ""):
        #we're expecting a return
         msg = "X"+str(code)
         ret = True
         ret_msg = ""
    else:
        #just sending data to update
        msg = "X"+str(code)+str(data)+"X"
    
    #send the data via pyserial
    
     #wait for a return
    if(ret):
        ret_msg = receiveDataStream();
        return ret_msg

    

def receiveDataStream():
    
    #receive something via serial usb
    #msgs need to end with an EOL
    ser = serial.Serial('/dev/ttyACM0', 2000000, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
    ser.flushInput()
    ser.flushOutput()
    data_raw = ser.readline()
    while(data_raw == ""):
        print("Waiting on Return")
        data_raw = ser.readline()
    print("From MBED, raw data is: "+data_raw)
    return data_raw


#### METHODS TO TEXT #####

def listFilters():

    FILTER_NAMES[:] = [];
    for i in range(0,len(FILTERS)):
        FILTER_NAMES.append(filterIdToString(int(FILTERS[i])))
        

def filterIdToString(filterID):
    filterID = int(filterID)
    #print(filterID)
    if(filterID == 1):
        return "Hi"
    elif(filterID == 2):
        return "Lo"
    else:
        return "Foo"

def printList(array):

    for i in range(0,len(array)):
        print(array[i])

def filterWholeStringBuilder():
    #loop through all the filters
    for i in range(0,len(FILTERS)):
        output = ""
        output = str(i+1) + ")" + FILTER_NAMES[i].upper() + " has parameters "
        for x in range(0,len(FILTER_PARAMS)):
            if(int(FILTER_PARAMS[i][x]) != 0):
                output = output + filterParamString(x) + str(FILTER_PARAMS[i][x]) + " "
        print(output)
        

def filterParamString(filterIndex):
    #Each position in the array denotes a specific param type
    if(filterIndex == 0):
        return "Echo: "
    elif(filterIndex == 1):
        return "Reverb: "
    elif(filterIndex == 2):
        return "Sustain: "

def startUp():
    initialSetupGatherData()
    print("Current Mode : "+ ("Parallel"if(PARALLEL_MODE) else"Serial"))
    print("Current Filters : ")
    filterWholeStringBuilder();
    if(PARALLEL_MODE & len(MIXER) > 0):
       #output
        print("Current Mix : "+ MIXER[0] + "-" +MIXER[1])
        pass
def displayMainMenu():
    print("--------------------------------------------------")
    print("MENU")
    print("--------------------------------------------------")
    print("1) Current Effects Chain")
    print("2) Add Filter")
    print("3) Edit Effects Chain")
    print("--------------------------------------------------")

#######
#main program loop
#####
##startUp()
##displayMainMenu()
##while(1):
##    menu_choice = input()
##    if(int(menu_choice) == 1):
##        startUp()
##    elif(int(menu_choice) == 2):
##        #add a filter, if number of filters is 2, ignore
##        if(len(FILTERS) == 2):
##            print("Already reached limit of filters")
##        else:
##            if(len(FILTERS) == 1):
##                #they've already selected serial mode
##                #show all the filters
##                for i in range(0,len(LIST_OF_FILTERS)):
##                    print()
##            pass

getFilters()
