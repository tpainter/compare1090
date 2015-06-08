import socket
import binascii
import math

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.92', 30005))
#clientsocket.connect(('192.168.0.92', 10001))

while True:
    #Keep the parts of a message that haven't been used yet
    msgString = str()
    buf = clientsocket.recv(2048)
    if len(buf) > 0:
        msgString += buf
        
        #For reference: http://wiki.modesbeast.com/Mode-S_Beast:Data_Output_Formats :
        #<esc> "1" : 6 byte MLAT, 1 byte signal level, 2 byte Mode-AC
        #<esc> "2" : 6 byte MLAT, 1 byte signal level, 7 byte Mode-S short frame
        #<esc> "3" : 6 byte MLAT, 1 byte signal level, 14 byte Mode-S long frame
        #<esc><esc>: true 0x1a
        #<esc> is 0x1a, and "1", "2" and "3" are 0x31, 0x32 and 0x33
        
        #Structure based on: https://github.com/mutability/dump1090/blob/master/net_io.c
        
        #Make sure that we find the escape character (begining of message)
        if chr(0x1a) in msgString:
            #Make sure that we start at the start of the message
            start = msgString.find(chr(0x1a))
        else:
            #Not a full message
            continue
        
        if msgString[start+1] == chr(0x1a):
            #This is just an escaped "escape"
            continue
           

        msgString = msgString[start+1:]
        
        #msgString = ["1","a","b","c","d","e","f","g","9"]
        msgType = msgString[0]
        msgMLAT = msgString[1:8]
        #msgSignal = binascii.hexlify(msgString[8])
        msgSignal = ord(msgString[8])
        msgSignal = msgSignal / 256.0
        msgSignal = msgSignal * msgSignal + 1e-5
        msgSignal = 10 * math.log(msgSignal, 10)
        
        #Address is supposed to be the last 24 bits of the message
        #Except for #11
        msgAddress = msgString[:6]
        msgAddress = bytearray(msgAddress)
        msgAddress = binascii.crc(msgAddress) & 0xffffffff
        
        if msgType == 1:
            pass
        elif msgType == 2:
            pass
        elif msgType == 3:
            pass
        else:
            pass
            
        
            
        print "Type: %s Address: %s Signal: %s" % (msgType, hex(msgAddress), msgSignal)
        
            
            
        