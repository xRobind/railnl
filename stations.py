class Station:
    """This class creates stations with its coordinates and connections
    """

    def __init__(self, name: str, y: str, x: str) -> None:
        self.name: str = name
        self.y: str = y
        self.x: str = x

        # make a dict that maps connections to their travel time
        # and a list that just has the connections
        self.connection_time: dict[str: int] = {}
        self.connections: list[str] = []

    def add_connection(self, connection: str, time: int):
        self.connection_time[connection] = time
        self.connections.append(connection)
        
        