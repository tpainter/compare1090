import socket
import base64
import binascii
import binhex

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('192.168.0.92', 30005))
#clientsocket.connect(('192.168.0.92', 10001))

while True:
    #Keep the parts of a message that haven't been used yet
    msgString = str()
    buf = clientsocket.recv(2048)
    if len(buf) > 0:
        msgString += buf
        #For reference: http://wiki.modesbeast.com/Mode-S_Beast:Data_Output_Formats
        #Make sure that we find the escape character (begining of message)
        if chr(0x1a) in msgString:
            #Make sure that we start at the start of the message
            start = msgString.find(chr(0x1a))
        
        
        if 0x1a in bytearray(msgString):
            print "begin msg"
            start = 0
            for i in bytearray(msgString):
                if i == 0x1a:
                    break
                else:
                    start += 1
            
            print start
            #print(chr(bytearray(msgString)[start+1]))
        