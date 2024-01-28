class Schedule:

    def __init__(self, trajectories, all_connections) -> None:
        self.trajectories = trajectories
        self.connections_used = []
        self.all_connections = all_connections
        self.connections_over = all_connections
        self.time = 0
        self.T = 0
        self.p = 0
        
    # def calculate_K(self):
    #     for trajectory in self.trajectories:
    #         self.time += trajectory.time
    #         for connection in trajectory.stations:
    #             if connection not in self.connections_used:
    #                 self.connections_used.append(connection)
    #                 self.connections_used.append(connection.corresponding)
    #                 if connection in self.connections_over:
    #                     self.connections_over.remove(connection)
    #                     self.connections_over.remove(connection.corresponding)
    def calculate_K(self):
        for trajectory in self.trajectories:
            self.time += trajectory.time
        self.T = len(self.trajectories)
        for i in range(len(trajectory.stations)):
            self.connections_used.append(trajectory.stations[i])
            try:
                self.time += trajectory.stations[i].time
            except(AttributeError):
                pass
        
        try:
            self.p = 2 * len(self.connections_used) / len(self.all_connections)
        except(TypeError):
            self.p = 2 * len(self.connections_used) / self.all_connections

        return 10000 * self.p - (self.T * 100 + self.time)
            
            
        self.T = len(self.trajectories)
        
        # for i in range(len(trajectory.stations)):
            # self.connections_used.append(trajectory.stations[i])
            # try:
                # self.time += trajectory.stations[i].time
            # except(AttributeError):
                # pass
        
        # sometimes self.all_connections is already an integer of the number
        # of connections
        try:
            self.p = len(self.connections_used) / len(self.all_connections)
        except(TypeError):
            self.p = len(self.connections_used) / self.all_connections
        
        score = 10000 * self.p - (self.T * 100 + self.time)
        self.time = 0
        self.T = 0
        self.p = 0
        
        return score
        
    def add_trajectory(self, trajectory):
        self.trajectories.append(trajectory)
    
