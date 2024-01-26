import random as r


from code.algorithms.baseline import Baseline

from code.classes.schedule import Schedule


class Pool:
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
            # empty lists and start again
            self.B.trajectories = []
            self.B.connections = []
            trajectory = self.B.start_trajectory()
            
            # continue a trajectory until a stopping condition is met
            # and add the completed trajectory to the list
            while True:
                result = self.B.continue_trajectory(trajectory)

                if result == "stop" or result == "new trajectory":
                    self.all_trajectories.append(trajectory)
                    break
        
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
        # create a new train table and calculate it's K
        self.create_train_table()
        k = self.calculate_K()

        # update if it is better or the same, 
        # otherwise revert back to old train table
        if k >= self.K:
            self.K = k
            self.best_train_table = self.train_table

    def calculate_K(self):
        """calculate the quality of the train table using Schedule class.
        """        
        S = Schedule(self.train_table, self.B.connections)
        return S.calculate_K()