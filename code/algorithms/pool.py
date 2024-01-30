import random as r

from code.algorithms.baseline import Baseline
from code.classes.trajectory import Trajectory
from code.classes.schedule import Schedule


class Pool:
    """This class contains an algorithm that takes 10000 randomly-created
    trajectories and combines them in a train-table over and over again,
    while keeping track of which combination returns the highest K-value.
    """

    def __init__(self, max: int, region: str, amount: int) -> None:
        """Initialises a baseline instance for creating trajectories,
        a list to save the trajectories in, and a variable to save the
        highest K.
        """
        self.B = Baseline(max, region)
        self.all_trajectories: list[Trajectory] = []
        self.K = -10000

        self.create_trajectories(amount)
        self.create_network()

    def create_trajectories(self, amount):
        """Create a number trajectories.
        """
        for i in range(0, amount):
            # empty list and start again
            self.B.trajectories = []
            trajectory = self.B.start_trajectory()
            
            # continue a trajectory until a stopping condition is met
            # and add the completed trajectory to the list
            while True:
                result = self.B.continue_trajectory(trajectory)

                if result == "stop" or result == "new trajectory":
                    self.all_trajectories.append(trajectory)
                    break

    def create_network(self):
        """Create a train table with the maximum amount of trajectories.
        """        
        self.network = []

        # randomly choose a trajectory to add to the train table
        for i in range(0, self.B.max_trajectories):
            self.network.append(r.choice(self.all_trajectories))

    def change_network(self):
        """Randomly change the network by picking 7 random trajectories,
        and calculate the K after. If it is better: keep the change,
        otherwise discard it.
        """
        # create a new train table and calculate it's K
        self.create_network()
        S = Schedule(self.network, self.B.total_connections)
        self.K = S.calculate_K_simple()

    def calculate_K(self):
        """calculate the quality of the train table using Schedule class.
        """
        S = Schedule(self.network, self.B.total_connections)
        return S.calculate_K_simple()