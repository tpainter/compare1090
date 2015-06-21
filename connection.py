from twisted.internet import reactor, protocol
import modesclient

class ModesClient(protocol.Protocol):
    """Send received message to be analyzed."""
        
    def dataReceived(self, data):
        modesclient.parseBeastMessage(self.factory.name, data)

class ModesFactory(protocol.ReconnectingClientFactory):
    protocol = ModesClient
    
    def __init__(self, name):
        """Uses the passed name to help sort results later."""
        self.name = name
        print("Connected to antenna: %s" % self.name)

    def clientConnectionFailed(self, connector, reason):
        print("Connection lost. Reconnecting...")
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)
    
    def clientConnectionLost(self, connector, reason):
        print("Connection lost. Reconnecting...")
        protocol.ReconnectingClientFactory.clientConnectionLost(self, connector, reason)