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
    """ this class takes a random network, and than makes random 
    changed to the network. If the change results into a better 
    quality the original network is replaced.If not, another
    random change is made."""

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


    def random_railmap(self) -> None:
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

        # Calculate and save the quality of the generated railmap
        S = Schedule(self.trajectories, self.baseline_instance.total_connections)
        self.original_quality = S.calculate_K_simple()
        
        # save K for plotting
        self.K_values.append(self.original_quality)
        
        #keep track of original trajectory
        self.original_trajectories = random_network


    def choose_random_trajectory(self) -> None:
        """Randomly chooses a trajectory from network,
         and deletes it from the network."""
        #randomly select a trajectory from the railmap and remove it from network after creating a copy
        self.random_trajectory = random.choice(self.trajectories)
        self.trajectories.remove(self.random_trajectory)
        
    
    def new_trajectory(self):
        """Randomly create a new trajectory and add it to the network"""
        self.baseline = Baseline(self.max, self.region)
        self.new_traj = self.baseline.start_trajectory()

        # Continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline.continue_trajectory(self.new_traj)

            if result == "stop" or result == "new trajectory":
                self.trajectories.append(self.new_traj)
                break

        S = Schedule(self.trajectories, self.baseline.total_connections)
        self.new_quality = S.calculate_K_simple()
        self.K_values.append(self.new_quality)
    
    
    def compare(self) -> None:
        """Checks if new network is an improvement, 
        and replaces it if this is the case."""
        #define improvement 
        improvement = self.new_quality > self.original_quality

        if improvement: 
            # If the new network is an improvement, replace the original with the new one
            self.original_trajectories = copy.deepcopy(self.trajectories)
            self.original_quality = self.new_quality
            
            
    def run(self, iterations) -> None:
        self.random_railmap()
        
        for i in range(100):
            self.choose_random_trajectory()
            self.new_trajectory()
            self.compare()
            
            
            
    
    
    
 
        
        