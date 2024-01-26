import sys
import random
import matplotlib.pyplot as plt
import copy



from code.classes.stations import Station
from code.classes.trajectory import Trajectory
from code.algorithms.baseline import Baseline
from code.classes.connection import Connection
from code.classes.schedule import Schedule

from code.algorithms.baseline import Baseline


class Hillclimber:
    """ this class......."""

    def __init__(self, max, region) -> None:
        self.baseline_instance = Baseline(max, region)
        self.stations = []
        self.connections = []
        self.network = []
        self.total_time = 0
        self.current_directory = []
        self.schedules = []
        
        # load station structures and connections 
        self.load_stations(f"data/Stations{region}.txt")
        self.load_connections(f"data/Connecties{region}.txt")
        
        self.total_connections = len(self.connections)
        
        #set maximum of trajectories
        self.max_trajectories = max
        self.random_network = []
        self.changed_network = []
        
        self.current_railmap = None

        #deepcopy
        # self.railmap = copy.deepcopy(railmap)
        # self.value = railmap.calculate_K()

    def load_stations(self, filename):
        """open file, read the lines and split into the three parts
        """
        with open(filename) as f:
            # skip first line
            next(f)
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",", 2)

                # set the different parts of the line to its variable
                name = parts[0]
                try:
                    y = parts[1]
                except(IndexError):
                    break
                x = parts[2].strip("\n")

                # create the station, add station to self.stations
                station = Station(name, y, x)
                self.stations.append(station)

                # read new line
                line = f.readline()

    def load_connections(self, filename):
        """open file, read the lines and split into the three parts
        """
        with open(filename) as f:
            # skip first line
            next(f)
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",", 2)

                # set the different parts of the line to its variable
                name = parts[0]
                try:
                    connection = parts[1]
                except(IndexError):
                    break
                if "Holland" in filename:
                    time = int(parts[2].strip("\n"))
                else:
                    time = int(parts[2].strip(".0\n"))

                # add connection to connection list in Station class,
                # and the list of all connections,
                # for both stations
                for station in self.stations:
                    if name == station.name:
                        station.add_connection(connection, time)
                    if connection == station.name:
                        station.add_connection(name, time)

                # add the connection and time to the list of all connections
                self.connections.append((name, connection))

                # read new line
                line = f.readline()

    def random_railmap(self):
        """Generate a random railmap using the Baseline class."""
        # Start with a random trajectory from the baseline
        random_network = self.baseline_instance.start_trajectory()
        # Continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline_instance.continue_trajectory(random_network)

            if result == "stop":
                self.network.append((random_network))
                break
            elif result == "new trajectory":
                self.network.append((random_network))
                random_network = self.baseline_instance.start_trajectory()


        # Calculate the quality of the generated railmap
        quality = self.baseline_instance.calculate_K()
        print(quality)
        
        return self.network
        
    def change_node(self):
        """Change a node/connection in the current trajectory."""
        #randomly select a trajectory from the railmap and remove it from network after creating a copy
        random_trajectory = random.choice(self.network)
        changed_trajectory = copy.deepcopy(random_trajectory)
        self.network.remove(random_trajectory)
        
        #decide if the first or the last connection will be replaced
        if random.random() < 0.9999:
            #select last connection from random trajectory 
            last_station = random_trajectory.stations[-2]
            print(last_station)
            
            # get available connections 
            connections = last_station.connections
            print(connections)
        
            #randomly choose new connection
            new_connection = random.choice(connections)
            print(new_connection)
            
            
            for station in self.stations:
                if new_connection == station.name:
                    new_station = station

            # remove the last connection from the current trajectory
            changed_trajectory.stations.pop()

            # add the new connection to the trajectory
            changed_trajectory.stations.append(new_station)
            
            #add new trajectory to network
            self.network.append(changed_trajectory)
            
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
            self.network.append(changed_trajectory)
        return self.network
            

    def compare_K_values(self, random_network, changed_network):
            """
            Compare the K values of the original and changed networks.
            """
            # Set the railmap for the current trajectory
            self.current_railmap = random_network

            # Calculate the K value for the original trajectory
            original_quality = self.baseline_instance.calculate_K()

            print(original_quality)

            # Set the railmap for the changed trajectory
            self.current_railmap = changed_network

            # Calculate the K value for the changed trajectory
            changed_quality = self.baseline_instance.calculate_K()

            print(changed_quality)

            # Compare the K values and determine if there is an improvement
            improvement = changed_quality > original_quality
            print("Improvement:", improvement)
            return improvement
    

    
        
            
        
        