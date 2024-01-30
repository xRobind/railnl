class Station:
    """This class creates stations with its coordinates and connections
    """

    def __init__(self, name: str, y: str, x: str) -> None:
        # name and coordinates of the station
        self.name: str = name
        self.y: str = y
        self.x: str = x
        self.nmbr_connections = 0

        # make a dict that maps connections to their travel time
        # and a list that just has the connections
        self.connection_time: dict[str, int] = {}
        self.connections: list[str] = []

    def add_connection(self, connection: str, time: int = 0) -> None:
        # add the connection to the dict and list
        self.connection_time[connection] = time
        self.connections.append(connection)
        
    # def __str__(self):
    #     return self.name
        
    def nmbr(self):
        self.nmbr_connections = len(self.connections)
        
    
        