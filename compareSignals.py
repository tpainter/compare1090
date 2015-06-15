if __name__ == "__main__":
    from twisted.internet import reactor
    from hardware import Antenna
    import displayHistory
    
    
    #TODO get connection information from file
    #Lines of the file are: [Name] [IP] [PORT] 
    
    connections = [["Main", "192.168.0.92", 30005, ],
                   ["Main2", "192.168.0.92", 30005, ],
                                                        ]
    
    for i in connections:
        Antenna(i[0], i[1], i[2])
        displayHistory.antennas.append(i[0])
    
    
    reactor.callWhenRunning(displayHistory.init)
    reactor.run()