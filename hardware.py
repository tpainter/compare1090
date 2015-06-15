


class Antenna():
    """
    Holds information about the antenna being used.
    """
    
    
    
    def __init__(self, name, ip, port):
        from twisted.internet import reactor
        import connection
        
        self.name = name
        self.ip = ip
        self.port = port
        
        f = connection.ModesFactory(self.name)
        self.connection = reactor.connectTCP("192.168.0.92", 30005, f)

