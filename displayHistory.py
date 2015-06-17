import time
from twisted.internet import reactor



    
def updateDisplay():
    #Sort the history by the time received
    sorted(_signalHistory, key = lambda x: x[1])
    
    