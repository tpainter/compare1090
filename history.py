

import time
from twisted.internet import reactor

#Store the names of the antennas to be able to sort the histories.
histories = {}

def receiveData(name, icaoAddr, rssi):
    """
    Receives data address and signal strength data from clients. 
    """
    histories[name].addResult(time.time(), icaoAddr, rssi)
    
    print "Name: %s Address: %x Signal: %.1f" % (name, icaoAddr, rssi)
    



class History():
    """
    Holds history and connection information.
    """    
    
    def __init__(self, name, ip, port):
        
        import connection
        
        self.name = name
        self.ip = ip
        self.port = port
        
        #Check to make sure that there isn't a duplicate name
        if name in histories:
            print("Error: Duplicate Name Found!")
            reactor.stop()
        else:
            histories[name] = self
        
        self.signalHistory = {}
        
        f = connection.ModesFactory(self.name)
        self.connection = reactor.connectTCP("192.168.0.92", 30005, f)
        
        reactor.callLater(5*60, self._cullResults)
        
    def addResult(self, time, addr, rssi):
        """
        Adds signal strength and time to history.
        """
        
        if addr in self.signalHistory:
            self.signalHistory[addr].append((time, rssi))
        else:
            self.signalHistory[addr] = [(time,rssi)]
            
    def _cullResults(self, limit = 10*60):
        """
        Removes message history older than "limit" seconds.
        """
        #print "cull"
        #print self.signalHistory
        
        for k,v in self.signalHistory.iteritems():
            for i in v:
                if i[0] < time.time() - limit:
                    self.signalHistory[k].remove(i)
                    
        reactor.callLater(5*60, self._cullResults)
        
    def returnHistory(self, limit = 10*60):
        """
        Returns all history more recent than limit seconds.
        """
        
        pass