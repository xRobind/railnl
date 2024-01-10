class Trajectory:
    
    def _init_(self, start) -> None:
        self.start = start
        self.stations = [start]
        self.time = 0
        self.nr_connections = 0

    def add_time(self, connection_time):
        self.time += connection_time

    def add_connection(self, connection):
        self.stations.append(connection)
        self.nr_connections += 1