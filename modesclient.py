from twisted.internet import reactor
from history import receiveData

#TODO Need to properly run through all of received data for multiple messages.

def parseBeastMessage(name, msg):
    import math
    #Keep the parts of a message that haven't been used yet
    beastMsgString = str()
    if len(msg) > 0:
        beastMsgString += msg
        
        #For reference: http://wiki.modesbeast.com/Mode-S_Beast:Data_Output_Formats :
        #<esc> "1" : 6 byte MLAT, 1 byte signal level, 2 byte Mode-AC
        #<esc> "2" : 6 byte MLAT, 1 byte signal level, 7 byte Mode-S short frame
        #<esc> "3" : 6 byte MLAT, 1 byte signal level, 14 byte Mode-S long frame
        #<esc><esc>: true 0x1a
        #<esc> is 0x1a, and "1", "2" and "3" are 0x31, 0x32 and 0x33
        
        #Structure based on: https://github.com/mutability/dump1090/blob/master/net_io.c
        
        #Make sure that we find the escape character (begining of message)
        if chr(0x1a) in beastMsgString:
            #Make sure that we start at the start of the message
            start = beastMsgString.find(chr(0x1a))
        else:
            #No message start found
            return None
        
        if beastMsgString[start+1] == chr(0x1a):
            #This is just an escaped "escape", return the rest of the string
            return None
           

        beastMsgString = beastMsgString[start+1:]
        
        msgType = beastMsgString[0]
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
            
            return (name, addr, rssi)





    
