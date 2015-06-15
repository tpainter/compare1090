from twisted.internet import reactor, protocol
from twisted.internet.defer import Deferred
import modesclient
from displayHistory import receiveData

class ModesClient(protocol.Protocol):
    """Send received message to be analyzed."""
    
    def dataReceived(self, data):
        d = modesclient.parseBeastMessage(self.factory.name, data)
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