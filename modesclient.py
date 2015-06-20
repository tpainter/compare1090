from twisted.internet import reactor
from history import receiveData
import math

#TODO Need to properly run through all of received data for multiple messages.

def parseBeastMessage(name, msg):    
    
    #For reference: http://wiki.modesbeast.com/Mode-S_Beast:Data_Output_Formats :
    #<esc> "1" : 6 byte MLAT, 1 byte signal level, 2 byte Mode-AC
    #<esc> "2" : 6 byte MLAT, 1 byte signal level, 7 byte Mode-S short frame
    #<esc> "3" : 6 byte MLAT, 1 byte signal level, 14 byte Mode-S long frame
    #<esc><esc>: true 0x1a
    #<esc> is 0x1a, and "1", "2" and "3" are 0x31, 0x32 and 0x33
    
    
    beastMsgString = msg
    #Make sure that we find the escape character (begining of message)
    while chr(0x1a) in beastMsgString:
        #Some structure based on: https://github.com/mutability/dump1090/blob/master/net_io.c
        
        start = beastMsgString.find(chr(0x1a))            
        
        if beastMsgString[start+1] == chr(0x1a):
            #This is just an escaped "escape", return the rest of the string
            beastMsgString = beastMsgString[start+2:]
            continue           

        beastMsgString = beastMsgString[start+1:]
        
        msgType = ord(beastMsgString[0])
        #Check that we have a full message
        if msgType == 0x31:
            #Type 1
            #Mode AC, ignore these messages
            beastMsgString = beastMsgString[start+2:]
            continue
        elif msgType == 0x32:
            #Type 2
            #Mode-S Short is 1+6+1+7=15 bytes
            if len(beastMsgString) >= 15:
                totalMsgLength = 15
            else:
                #Not enough length for a full message
                break
        elif msgType == 0x33:
            #Type 3
            #Mode-S Long is 1+6+1+14=22 bytes
            if len(beastMsgString) >= 22:
                totalMsgLength = 22
            else:
                #Not enough length for a full message
                break
        else:
            #This doesn't make sense.
            beastMsgString = beastMsgString[start+1:]
            continue
        
        
        msgMLAT = beastMsgString[1:8]
        
        #Reported signal strength is dbfs.
        msgSignal = ord(beastMsgString[8])
        msgSignal = msgSignal / 256.0
        msgSignal = msgSignal * msgSignal + 1e-5
        rssi = 10 * math.log(msgSignal, 10)
        
        #Get the original message information. Assume that dump1090 has corrected any errors
        # and done minimal validation. i.e. Don't check here.
        msgPlane = beastMsgString[9:]        
        modesType = ord(msgPlane[0]) >> 3        
        
        #Address is always the last 24 bits of the message used as crc parity.
        #Except for #11, which had the raw address.
        if modesType == 11:
            addr = ord(msgPlane[1]) << 16 | ord(msgPlane[2]) << 8 | ord(msgPlane[3])
            reactor.callLater(0, receiveData, name, addr, rssi)
        
        #Remove message from received data
        beastMsgString = beastMsgString[start+totalMsgLength:]





    
