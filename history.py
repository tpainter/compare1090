
import json
import time
import datetime
from twisted.internet import reactor

#Store the names of the antennas to be able to sort the histories.
histories = {}

def receiveData(name, icaoAddr, rssi):
    """
    Receives data address and signal strength data from clients. 
    """
    histories[name].addResult(time.time(), icaoAddr, rssi)
    
def allHistory():
    """
    Returns the history from all antennas as one big array.
    """
    
    #Name of file to write history
    historyfile = "resultsHistory.js"
    
    # Google charts needs data in following format:
    # [x-axis],[Address],[Series1] ... [SeriesN]
    # [time],[Address],[Antenna1] ... [AntennaN]
    
    temp_array = []
    numAntennas = len(histories)
    
    #add headers to array
    headers = ["Time", "Address"]
    #headers = []
    #columnType = {}
    #columnType['label'] = 'Time'
    #columnType['id'] = 'Time'
    #columnType['type'] = 'datetime'
    #headers.append(columnType)
    #headers.append("Address")
    
    for name in histories:
        headers.append(name)
        
    temp_array.append(headers)
    
    i = 0
    for name, hist in histories.iteritems():
        a = hist.returnHistoryGoogle()
        for b in a:
            temp_list = []
            
            #add time and address
            temp_list.append(b[0])
            temp_list.append(b[1])
            
            #Pad columns to put rssi in proper location
            for n in range(i):
                temp_list.append(None)
            temp_list.append(b[2])
            
            #Pad after the rssi to make all rows the same length
            for j in range(numAntennas - i - 1):
                temp_list.append(None)
            
            #Add row to array
            temp_array.append(temp_list)
        
        i += 1
        
    with open(historyfile, 'w') as the_file:
        the_file.write(json.dumps(temp_array, separators=(',',':')))
        
    print("History written to file: %s" % historyfile)
    
    #Every 10 minutes write a new file with results.
    reactor.callLater(10*60, allHistory)
    

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
        self.connection = reactor.connectTCP(self.ip, self.port, f)
        
        #Every hour remove results older than 4 hours
        reactor.callLater(60*60, self._cullResults, 4*60*60)
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
            
    def _cullResults(self, limit = 24*60*60):
        """
        Removes message history older than "limit" seconds. Default 24 hours.
        """
        
        count = 0
        
        for k,v in self.signalHistory.iteritems():
            for i in v:
                if i[0] < time.time() - limit:
                    self.signalHistory[k].remove(i)
                    count += 1
        
        print("$s removed %d old results." % (self.name, count))
        reactor.callLater(60*60, self._cullResults, limit)
        
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
                #temp_array.append([datetime.datetime.utcfromtimestamp(i[0]).isoformat(),"%x" % k, round(i[1], 2) ])
                temp_array.append([i[0],"%x" % k, round(i[1], 2) ])
        
        return temp_array