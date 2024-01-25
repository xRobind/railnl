class Schedule:

    def __init__(self) -> None:
        self.trajectories = []
        self.connections_used = []
        self.all_connections = []
        self.time = 0
        
    def calculate_K(self):
        for trajectory in self.trajectories:
            self.time += trajectory.time
        T = len(self.trajectories)
        p = len(self.connections_used)) / len(self.all_connections)
        return 10000 * p - (T * 100 + self.time)