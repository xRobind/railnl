from code.algorithms.baseline import Baseline
import random as r


class Random_change:
    """This class contains an algorithm that takes 10000 randomly-created
    trajectories and combines them in a train-table over and over again,
    while keeping track of which combination returns the highest K-value.
    """

    def __init__(self, max, region, amount) -> None:
        """Initialises a baseline instance for creating trajectories,
        a list to save the trajectories in, and a variable to save the
        highest K.
        """
        self.B = Baseline(max, region)
        self.all_trajectories = []
        self.K = -10000

        self.create_trajectories(amount)
        self.create_train_table()

    def create_trajectories(self, amount):
        """Create a number trajectories.
        """
        for i in range(0, amount):
            # empty list of trajectories and start again
            self.B.trajectories = []
            trajectory = self.B.start_trajectory()
            
            # continue a trajectory until a stopping condition is met
            # and add the completed trajectory to the list
            while True:
                result = self.B.continue_trajectory(trajectory)

                if result == "stop" or result == "new trajectory":
                    self.all_trajectories.append(trajectory)
                    break

    def count_connections(self):
        """Count all unique connections in a train table
        """
        # list to store all connections
        connections = []

        # loop through the trajectories
        for trajectory in self.train_table:
            # loop through all connections in a trajectory and add to the list
            for i in range(0, len(trajectory.stations) - 1):
                station = trajectory.stations[i]
                connection = trajectory.stations[i + 1]
                connections.append((station, connection))

        # make sure there are no doubles
        self.connections = set(connections)

    def count_time(self):
        """Count the total time in a train table.
        """
        # variable to store the time
        self.total_time = 0

        # loop through the trajectories
        for trajectory in self.train_table:
            self.total_time += trajectory.time
    
    def calculate_K(self):
        """calculate the quality of the train table
        """        
        T = len(self.train_table)
        p = (self.B.total_connections - len(self.connections)) / self.B.total_connections
        return 10000 * p - (T * 100 + self.total_time)
        
    def create_train_table(self):
        """Create a train table with the maximum amount of trajectories.
        """        
        self.train_table = []

        # randomly choose a trajectory to add to the train table
        for i in range(0, self.B.max_trajectories):
            self.train_table.append(r.choice(self.all_trajectories))

    def change_trajectory(self):
        """Randomly change one of the trajectories in the train table,
        and calculate the K after. If it is better: keep the change,
        otherwise discard it.
        """
        # create a new train table
        self.create_train_table()

        # calculate K
        self.count_connections()
        self.count_time()
        k = self.calculate_K()

        # update if it is better or the same, 
        # otherwise revert back to old train table
        if k >= self.K:
            self.K = k
            self.best_train_table = self.train_table

        print(self.K, self.best_train_table)
