import time
from twisted.internet import reactor


#Storage format is [time], [name], [icaoAddr], [rssi]
_signalHistory = []

#Store the names of the antennas
antennas = []

def init():
    """
    Initialization tasks for storage.
    """
    
    pass

def receiveData(name, icaoAddr, rssi):
    """
    Receives data address and signal strength data from clients. 
    """
    _signalHistory.append((time.time(), name, icaoAddr, rssi))
    
    print "Name: %s Address: %x Signal: %.1f" % (name, icaoAddr, rssi)
    
def updateDisplay():
    #Sort the history by the time received
    sorted(_signalHistory, key = lambda x: x[1])
    
    