import random

from code.algorithms.baseline import Baseline
from code.classes.schedule import Schedule
from code.classes.load import Load
from code.algorithms.baseline import Baseline


class Simulated_annealing:
    """This class takes a random network, and makes
    random changes to it. If the chages resutls in a higher score,
    the original network will be replaced. If not, the original
    network will be replaced with a probability that depends on
    the temperature, the quality of the old and new network and the number
    of iterations.
    """

    def __init__(self, max, region) -> None:
        self.max = max
        self.region = region
        self.baseline_instance = Baseline(max, region)
        self.trajectories = []

        # load station structures and connections
        load = Load(region)
        self.stations = load.stations()
        self.connections = load.connections()
        self.total_connections = len(self.connections)

        # save K's for plotting
        self.K_values = []

        #set iteration to 1
        self.iteration = 1

    def random_railmap(self) -> None:
        """Generate a random railmap using the Baseline class.
        """
        # Start with a random trajectory from the baseline
        random_network = self.baseline_instance.start_trajectory()

        # Continue the trajectory until a stopping condition is met
        while True:
            result =\
                self.baseline_instance.continue_trajectory(random_network)
            if result == "stop":
                self.trajectories.append(random_network)
                break
            elif result == "new trajectory":
                self.trajectories.append(random_network)
                random_network = self.baseline_instance.start_trajectory()

        # Calculate and save the quality of the generated railmap
        S = Schedule\
            (self.trajectories, self.baseline_instance.total_connections)
        self.original_quality = S.calculate_K_simple()

        # save K for plotting
        self.K_values.append(self.original_quality)

        #keep track of original trajectory
        self.original_trajectories = random_network

    def choose_random_trajectory(self) -> None:
        """Randomly chooses a trajectory from network,
        and deletes it from the network.
        """
        # randomly select a trajectory from the railmap and
        # remove it from network after creating a copy
        self.random_trajectory = random.choice(self.trajectories)
        self.trajectories.remove(self.random_trajectory)


    def new_trajectory(self) -> None:
        """Makes a random trajectory, adds it to the previous
        network and calculates the quality of this new network.
        """
        self.baseline = Baseline(self.max, self.region)
        self.new_traj = self.baseline.start_trajectory()

        # continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline.continue_trajectory(self.new_traj)

            if result == "stop" or result == "new trajectory":
                self.trajectories.append(self.new_traj)
                break

        S = Schedule(self.trajectories, self.baseline.total_connections)
        self.new_quality = S.calculate_K_simple()
        self.K_values.append(self.new_quality)
    
    def calculate_temperature(self) -> None:
        """Calculates the temparature and the rejection probability.
        """
        #set t start and define temperature
        t_start = 500
        temperature = t_start - (t_start/self.iterations)*self.iteration
        try:
            self.reject_prob =\
                2**(( self.new_quality - self.original_quality)/temperature)
        except(ZeroDivisionError,OverflowError):
            self.reject_prob = 1

    def compare_values(self) -> None:
        """If the original quality is smaller than the new one,
        replace the original network with the old one. If not,
        the new network will be accepted with the probability calculated in
        calculate_temparature.
        """
        # Define an improvement
        improvement = self.original_quality < self.new_quality

        # Define when a decline in quality should still lead to a replacement
        replace = self.reject_prob < random.random()
        if improvement:
            # If the new network is an improvement,
            # replace the original with the new one
            self.original_trajectories = self.trajectories
            self.original_quality = self.new_quality

        elif replace:
            # If the new network is not better,
            # but accepted based on probability, replace the original
            self.calculate_temperature()
            self.original_trajectories = self.trajectories
            self.original_quality = self.new_quality

    def run(self) -> None:
        self.random_railmap()
        self.iterations = 1000

        for i in range(self.iterations):
            self.choose_random_trajectory()
            self.new_trajectory()
            self.calculate_temperature()
            self.compare_values()
            self.iteration += 1
