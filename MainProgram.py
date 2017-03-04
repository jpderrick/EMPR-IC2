##### MODE #####
#represented as a 1 for parallel and 0 for serial

def getMode():
    # Request the Current mode setup from the mbed board
    raw_req = sendDataStream(1)
    pass

def getMix():
    #Get the mixing values
    pass

def getFilters():
    #get all of the filters in the fx chain
    

    #some test data, returns a list of filter ids
    return [1,2,3,4,5]

def getFilterParams(filterID):
    #get the parameters of a certain filter
    return 1

def setFilterParams(filterID,params):
    #send an updated set of paramters for a filter
    pass

def initialSetupGatherData():
    #gather all the data we need
    mode = getMode()
    filters = getFilters()
    filter_params = list()
    
    for i in range(0,len(filters)):
        filter_params.append(getFilterParams(filters[i]))
        #print(filter_params)

    
    
def sendDataStream(code,data=""):
    #Send something via serial usb
    #####ENUMS#####
        #1 = get mode
        #2 = get filters
        #3 = get filter params (by id)
        #4 = update parameters
        #5 = update mode
        #6 =

    msg = ""
    ret = False
 
    if(data == ""):
        #we're expecting a return
         msg = "X"+str(code)+"X"
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
    #print(data_raw)
    return data_raw

    

#######
#main program loop
#######

print("Initial")
initialSetupGatherData()
print("Current config: ... ")
