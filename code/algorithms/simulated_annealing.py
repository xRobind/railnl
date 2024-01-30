import sys
import random
import matplotlib.pyplot as plt
import copy


from code.classes.stations import Station
from code.classes.trajectory import Trajectory
from code.algorithms.baseline import Baseline
from code.classes.connection import Connection
from code.classes.schedule import Schedule
from code.classes.load import Load

from code.algorithms.baseline import Baseline


class Simulated_annealing:
    """ this class......."""

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
    
        self.iteration = 1 
        

    def random_railmap(self):
        """Generate a random railmap using the Baseline class."""
        # Start with a random trajectory from the baseline
        random_network = self.baseline_instance.start_trajectory()
        # Continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline_instance.continue_trajectory(random_network)

            if result == "stop":
                self.trajectories.append(random_network)
                break
            elif result == "new trajectory":
                self.trajectories.append(random_network)
                random_network = self.baseline_instance.start_trajectory()


        # Calculate the quality of the generated railmap
        S = Schedule(self.trajectories, self.baseline_instance.total_connections)
        self.original_quality = S.calculate_K_simple()
        # save K for plotting
        self.K_values.append(self.original_quality)
        
        #keep track of original trajectory
        self.original_trajectories = random_network

    def choose_random_trajectory(self):
        #randomly select a trajectory from the railmap and remove it from network after creating a copy
        self.random_trajectory = random.choice(self.trajectories)
        self.trajectories.remove(self.random_trajectory)
        
    
    def new_trajectory(self):
        baseline = Baseline(self.max, self.region)
        self.new_traj = baseline.start_trajectory()

        # Continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline_instance.continue_trajectory(self.new_traj)

            if result == "stop" or result == "new trajectory":
                self.trajectories.append(self.new_traj)
                break

        S = Schedule(self.trajectories, self.baseline_instance.total_connections)
        self.new_quality = S.calculate_K_simple()
        self.K_values.append(self.new_quality)
    
    def calculate_temperature(self):
        t_start = 500
        temperature = t_start - (t_start/self.iterations)*self.iteration
        try:
            self.reject_prob = 2**(( self.new_quality - self.original_quality)/temperature)
        except(ZeroDivisionError,OverflowError):
            self.reject_prob = 1

    def compare_values(self):
        improvement = self.original_quality < self.new_quality
        replace = self.reject_prob < random.random()
        if improvement:
            self.original_trajectories = self.trajectories
            self.original_quality = self.new_quality
            
        elif replace: 
            self.calculate_temperature()
            self.original_trajectories = self.trajectories
            self.original_quality = self.new_quality
            
    def run(self):
        self.random_railmap()
        self.iterations = 1000
        
        for i in range(self.iterations):

            self.choose_random_trajectory()
            self.new_trajectory()
            self.calculate_temperature()
            self.compare_values()
            self.iteration += 1
            