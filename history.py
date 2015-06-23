
import json
import time
from twisted.internet import reactor

#Store the names of the antennas to be able to sort the histories.
histories = {}

def receiveData(name, icaoAddr, rssi):
    """
    Receives data address and signal strength data from clients. 
    """
    histories[name].addResult(time.time(), icaoAddr, rssi)
    
    #print "Name: %s Address: %x Signal: %.1f" % (name, icaoAddr, rssi)
    



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
        self.msgReceivedTot = 0
        self.msgCount = 0
        #Number of minutes between printing number of messages received
        self.resultsPeriod = 5
        
        
        f = connection.ModesFactory(self.name)
        self.connection = reactor.connectTCP("192.168.0.92", 30005, f)
        
        reactor.callLater(5*60, self._cullResults)
        reactor.callLater(self.resultsPeriod*60, self._periodicResults, self.resultsPeriod)
        reactor.callLater(5*60, self._checkReceiving)
        
    def addResult(self, time, addr, rssi):
        """
        Adds signal strength and time to history.
        """
        
        if addr in self.signalHistory:
            self.signalHistory[addr].append((time, rssi))
        else:
            self.signalHistory[addr] = [(time,rssi)]
            
        self.msgReceivedTot += 1
        self.msgCount += 1
            
    def _cullResults(self, limit = 5*60):
        """
        Removes message history older than "limit" seconds.
        """
        
        count = 0
        
        for k,v in self.signalHistory.iteritems():
            for i in v:
                if i[0] < time.time() - limit:
                    self.signalHistory[k].remove(i)
                    count += 1
                    
        #print("Culled: %d" % count)
                    
        reactor.callLater(5*60, self._cullResults)
        
    def _periodicResults(self, period):
        """
        Print number of messages received in last "period" minutes.
        """
        
        print("%s: %d messages received in last %d minutes." % (self.name, self.msgCount, period))       
        self.msgCount = 0        
        reactor.callLater(self.resultsPeriod*60, self._periodicResults, self.resultsPeriod)
        
    def _checkReceiving(self, lastTot = 0):
        """
        Checks that message are being received. If not, restarts connection.
        """
        
        if self.msgReceivedTot == lastTot:
            #Have not received any new messages since last check
            pass
        
        reactor.callLater(5*60, self._checkReceiving, self.msgReceivedTot)
        
    def returnHistoryJson(self):
        """
        Returns as json all history.
        """
        
        return json.dumps({self.name: self.signalHistory}, separators=(',',':'))
    
    def returnHistoryGoogle(self):
        """
        Returns as all history as array to use with Google Charts.
        """
        
        #Google charts need full lines, dictionaries won't work.
        #Columns are [antenna name], [plane address], [time], [rssi]
        temp_array = []
        
        for k, v in self.signalHistory.iteritems():
            #k is address, v is [(time, rssi)]
            for i in v:
                temp_array.append([self.name, "%x" % k, i[0], i[1] ])
        
        return json.dumps(temp_array, separators=(',',':'))