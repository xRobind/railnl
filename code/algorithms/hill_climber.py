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
        self.baseline_instance = Baseline(max, region)
        self.trajectories = []
        
        # load station structures and connections
        load = Load(region)
        self.stations = load.stations()
        self.connections = load.connections()
        self.total_connections = len(self.connections)

        #deepcopy
        # self.railmap = copy.deepcopy(railmap)
        # self.value = railmap.calculate_K()

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
        S = Schedule(self.trajectories, self.connections)
        self.original_quality = S.calculate_K()
        print(self.original_quality)
        
        #keep track of original trajectory
        self.original_trajectory = random_network
        
        
    def change_node(self):
        """Change a node/connection in the current trajectory."""
        #randomly select a trajectory from the railmap and remove it from network after creating a copy
        random_trajectory = random.choice(self.trajectories)
        changed_trajectory = copy.deepcopy(random_trajectory)
        self.trajectories.remove(random_trajectory)
        
        #decide if the first or the last connection will be replaced
        if random.random() < 0.5:
            #select last connection from random trajectory 
            last_station = random_trajectory.stations[-2]
            
            # get available connections 
            connections = last_station.connections
        
            #randomly choose new connection
            new_connection = random.choice(connections)
            
            for station in self.stations:
                if new_connection == station.name:
                    new_station = station

            # remove the last connection from the current trajectory
            changed_trajectory.stations.pop()

            # add the new connection to the trajectory
            changed_trajectory.stations.append(new_station)
            
            #add new trajectory to network
            self.trajectories.append(changed_trajectory)
            
            quality = self.baseline_instance.calculate_K()

        
        else:
            #select first connection from random trajectory
            first_station = random_trajectory.stations[1]
            
            #get available connections 
            connections = first_station.connections
            
            #randomly choose new connection
            new_connection = random.choice(connections)
            
            for station in self.stations:
                if new_connection == station.name:
                    new_station = station
            
            # create a copy of the current trajectory to make changes
            changed_trajectory = copy.deepcopy(random_trajectory)

            # remove the first connection from the current trajectory
            changed_trajectory.stations.pop(0)

            # add the new connection to the beginning of the trajectory
            changed_trajectory.stations.insert(0,new_connection)
            
            #add new trajectory to network
            self.trajectories.append(changed_trajectory)
        
        return    
        
    def undo_change_node(self, random_trajectory, changed_trajectory):
          """
          Undo the changes made to the network during the change_node function.
          """
          self.trajectories.remove(changed_trajectory)
          self.trajectories.append(random_trajectory)

    def compare_K_values(self):
        """
        Compare the K values of the original and changed networks.
        """
        # Calculate the K value with the changed trajectory
        S = Schedule(self.trajectories, self.connections)
        changed_quality = S.calculate_K()
        print(changed_quality)

        # Compare the K values and determine if there is an improvement
        improvement = changed_quality > self.original_quality
        print("Improvement:", improvement)
        if not improvement:
            #undo the change 
            self.trajectories.pop()
            self.trajectories.append(self.original_trajectory)
        else:
            self.original_quality = changed_quality

        return changed_quality


