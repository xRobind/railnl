class Trajectory:
    
    def _init_(self) -> None:
        self.connections = []
        self.time = 0
        self.nr_connections = 0

    def add_time(self, connection_time):
        self.time += connection_time

    def add_connection(self, connection_name):
        self.connections.append(connection_name)
        self.nr_connections += 1