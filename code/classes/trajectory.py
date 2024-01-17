class Trajectory:
    """this class keeps track of a trajectory and it's eslapsed
    time and visited stations
    """    
    
    def __init__(self, start) -> None:
        self.stations = [start]
        self.time = 0
        self.nr_connections = 0

    def add_time(self, connection_time):
        self.time += connection_time

    def add_connection(self, connection):
        self.stations.append(connection)
        self.nr_connections += 1
