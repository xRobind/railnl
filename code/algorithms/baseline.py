import random
import sys
import matplotlib.pyplot as plt
from typing import Any

from code.classes.stations import Station
from code.classes.trajectory import Trajectory
from code.classes.load import Load
from code.classes.schedule import Schedule

class Baseline:
    """This class reads data from csv files about train stations in Holland,
    saves them in classes and uses them to create imaginary trains that follow
    a trajectory through the saved train stations.
    This process continues until all saved connections between two specific
    stations are used. It then uses a known formula to calculate the quality
    of the lines. The goal is to implement its methods in such a way that the
    quality of the lines will end up the closest to the number 10000.
    """    

    def __init__(self, max: int, region: str) -> None:
        """initialise lists that contain stations as objects of the class,
        connections as a dict that links the connection to the time,
        and trajectories made and time spent
        """
        self.trajectories: list[Trajectory] = []
        self.total_time = 0
        self.region = region

        # load station structures and connections
        load = Load(region)
        self.stations = load.stations()
        self.connections = load.connections()
        self.total_connections = len(self.connections)
        
        #set maximum of trajectories
        self.max_trajectories = max

    def start_trajectory(self) -> Any:
        """initialize a trajectory with a starting station and amount of stops
        that it will make
        """
        # stop if the maximum of trajectories
        if len(self.trajectories) == self.max_trajectories:
            return "stop"
        
        # random starting station from our list of station objects
        starting_station = random.choice(self.stations)

        # create trajectory with starting station, add to the Trajectory class
        trajectory = Trajectory(starting_station)
        self.trajectories.append(trajectory)

        return trajectory
    
    def continue_trajectory(self, trajectory: Trajectory) -> str:
        """continue a trajectory by choosing between available connections
        of the current station and updating the current one to the next one,
        except if we've reached the end.

        Returns "continue" if continued, "new trajectory" if not continued
        because the 2hrs are over,
        "stop" if not continued because all connections have been
        used and the goal has been reached.
        """
        # get available connections
        print(trajectory)
        station: Station = trajectory.stations[-1]
        connections = station.connections
        # choose a random connection
        chosen_connection = random.choice(connections)

        # probability that the trajectory stops, add to the total time if yes
        # different amount of time and trajectories for Holland and Nederland
        if self.region == "Holland":
            if random.random() < ((1 / (len(connections)+1)) * (trajectory.time / 120)):
                self.total_time += trajectory.time

                # probability that the whole train table stops
                if random.random() < ((1/7)**(7-len(self.trajectories))):
                    return "stop"
                
                # start a new trajectory
                return "new trajectory"
        else:
            if random.random() < ((1 / (len(connections)+1)) * (trajectory.time / 180)):
                self.total_time += trajectory.time

                # probability that the whole train table stops
                if random.random() < ((1/20)**(20-len(self.trajectories))):
                    return "stop"
                
                # start a new trajectory
                return "new trajectory"
            
        # find the chosen connection in the dict where it's time is mapped
        time = self.get_time(station, chosen_connection)

        # add travel time if it stays under 2hrs, otherwise stop
        # add to total time if t stops
        # different for the regions
        if self.region == "Holland":
            if (trajectory.time + time) > 120:
                self.total_time += trajectory.time
                
                # probability that the whole train table stops
                if random.random() < ((1/7)**(7-len(self.trajectories))):
                    return "stop"
                
                # start a new trajectory
                return "new trajectory"
            else:
                # add the travel time to the time of the trajectory
                trajectory.add_time(time)

                # add connected station as an object by searching for it by name
                for item in self.stations:
                    if item.name == chosen_connection:
                        trajectory.add_connection(item)
        else:
            if (trajectory.time + time) > 180:
                self.total_time += trajectory.time
                
                # probability that the whole train table stops
                if random.random() < ((1/20)**(20-len(self.trajectories))):
                    return "stop"
                
                # start a new trajectory
                return "new trajectory"
            else:
                # add the travel time to the time of the trajectory
                trajectory.add_time(time)

                # add connected station as an object by searching for it by name
                for item in self.stations:
                    if item.name == chosen_connection:
                        trajectory.add_connection(item)

        # remove connection from connections that have to be used
        # and check if they have all been used
        if (station.name, chosen_connection) in self.connections:
            self.connections.remove((station.name, chosen_connection))

            if len(self.connections) == 0:
                return "stop"

        elif (chosen_connection, station.name) in self.connections:
            self.connections.remove((chosen_connection, station.name))

            if len(self.connections) == 0:
                return "stop"

        return "continue"
    
    def get_time(self, station: Station, chosen_connection: str) -> int:
        """Get the travel time by finding the chosen connection
        in the dict where it's time is mapped.
        """        
        for connection in station.connection_time:
            if connection == chosen_connection:
                return station.connection_time[connection]
        
        return 0

    def calculate_K(self) -> float:
        """Calculate the quality of the railmap using Schedule class.
        """        
        S = Schedule(self.trajectories, self.total_connections)
        return S.calculate_K_simple()