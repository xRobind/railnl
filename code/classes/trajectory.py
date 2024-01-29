class Trajectory:
    """this class keeps track of a trajectory and it's eslapsed
    time and visited stations
    """    
    
    def __init__(self, start= None) -> None:
        if start != None:
            self.stations = [start]
        else:
            self.stations = []
        self.time = start.time
        self.nr_connections = 0

    def add_time(self, connection_time):
        self.time += connection_time

    def add_connection(self, connection):
        self.stations.append(connection)
        self.nr_connections += 1
        
    def add_connection_and_time(self, connection, max_time):
        if self.time + connection.time > max_time:
            return False
        # if self.stations[-1].connection_id == connection.corresponding.connection_id:
            # if self.stations[-2].connection_id == connection.connection_id:
                # return False
        self.stations.append(connection)
        self.time += connection.time
        return True
        
        
        

