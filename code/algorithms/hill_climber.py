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


class Hillclimber:
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

    def random_railmap(self):
        """Generate a random railmap using the Baseline class."""
        # Start with a random trajectory from the baseline
        try:
            random_network = self.baseline_instance.start_trajectory() 
        except(AttributeError):
            return

            
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
        self.original_trajectory = random_network

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

            if result == "stop":
                self.trajectories.append(self.new_traj)
                break

        S = Schedule(self.trajectories, self.baseline_instance.total_connections)
        self.new_quality = S.calculate_K_simple()
        self.K_values.append(self.new_quality)
    
    def compare(self):
        improvement = self.new_quality > self.original_quality

        if improvement: 
            self.original_trajectory = self.trajectories
            self.original_quality = self.new_quality
            
    def run(self, iterations):
        self.random_railmap()
        
        for i in range(100):
            self.choose_random_trajectory()
            self.new_trajectory()
            self.compare()
            
            
            
    
    
    
 
        
        