class Schedule:

    def __init__(self, trajectory, all_connections) -> None:
        self.trajectories = [trajectory]
        self.connections_used = []
        self.all_connections = all_connections
        self.time = 0
        self.T = 0
        self.p = 0
        
    def calculate_K(self):
        for trajectory in self.trajectories:
            self.time += trajectory.time
        self.T = len(self.trajectories)
        for i in range(len(trajectory.stations)):
            self.connections_used.append(trajectory.stations[i])
            self.time += trajectory.stations[i].time
        sef.p = 2 * len(self.connections_used) / len(self.all_connections)
        return 10000 * self.p - (self.T * 100 + self.time)