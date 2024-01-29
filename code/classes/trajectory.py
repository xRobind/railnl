from typing import Optional

from code.classes.stations import Station

class Trajectory:
    """this class keeps track of a trajectory and it's eslapsed
    time and visited stations
    """    
    
    def __init__(self, start: Optional[Station] = None) -> None:
        if start != None:
            self.stations = [start]
        else:
            self.stations = []
        self.time = 0
        self.nr_connections = 0

    def add_first_time(self) -> None:
        self.time = self.stations[0].time
        
    def add_time(self, connection_time) -> None:
        self.time += connection_time

    def add_connection(self, connection) -> None:
        self.stations.append(connection)
        self.nr_connections += 1
        
    def add_connection_and_time(self, connection, max_time) -> bool:
        if self.time + connection.time > max_time:
            return False
        # if self.stations[-1].connection_id == connection.corresponding.connection_id:
            # if self.stations[-2].connection_id == connection.connection_id:
                # return False
        self.stations.append(connection)
        self.time += connection.time
        return True
        
        
        

