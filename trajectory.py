class Trajectory:
    def _init_(self) -> None:
        self.connections = []
        self.time = 0
        self.nr_connections = 0
        for connection in self.connections:
        			self.time += connection.time
        			self.nr_connections += 1;