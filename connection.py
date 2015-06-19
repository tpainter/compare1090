from twisted.internet import reactor, protocol
import modesclient
from history import receiveData

class ModesClient(protocol.Protocol):
    """Send received message to be analyzed."""
        
    def dataReceived(self, data):
        d = modesclient.parseBeastMessage(self.factory.name, data)
        #self.partialMsg = remain
        if d is not None:
            receiveData(d[0], d[1], d[2])

class ModesFactory(protocol.ClientFactory):
    protocol = ModesClient
    
    def __init__(self, name):
        """Uses the passed name to help sort results later."""
        self.name = name

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        reactor.stop()