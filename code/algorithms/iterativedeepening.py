import random
import sys
import matplotlib.pyplot as plt
import copy

sys.path.append('../classes')
sys.path.append('code/classes')
sys.path.append('../..')

from code.classes.stations import Station
from code.classes.trajectory import Trajectory
from code.classes.stack import Stack
from code.classes.connection import Connection

class IDS:

    def __init__(self, max, region) -> None:
        """initialise lists that contain stations as objects of the class,
        connections as a dict that links the connection to the time,
        and trajectories made and time spent
        """
        self.stations = []
        self.connections = []
        self.stack = Stack()

        # load station structures and connections 
        self.load_stations(f"data/Stations{region}.txt")
        self.load_connections(f"data/Connecties{region}.txt")
        
        self.total_connections = len(self.connections)
        
        #set maximum of trajectories
        self.max_trajectories = max

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
                        for station2 in self.stations:
                            if station2.name == connection:
                                connection_object = Connection(station, station2, time)
                                station.add_connection(connection_object)
                                self.connections.append(connection_object)
                    if connection == station.name:
                        for station1 in self.stations:
                            if station1.name == name:
                                connection_object = Connection(station, station1, time)
                                station.add_connection(connection_object)
                                self.connections.append(connection_object)
                print(len(self.connections))

                # read new line
                line = f.readline()
                
    def start_trajectory(self):
        """initialize a trajectory with a starting station and amount of stops
        that it will make
        """
        # depth 1
        # pick every starting trajectory once
        for connection in self.connections:
                current = Trajectory(connection)
                for second_connection in current.stations[-1].connection.connections:
                    new = copy.deepcopy(current)
                    new.add_connection(second_connection)
                    ## add trajectory to schedule
                    self.stack.push(new)
        return len(self.stack.items)

    def continue_trajectory(self):
        # depth 2
        i = 0
        while( i != 10):
            current = self.stack.pop()
            for next_connection in current.stations[-1].connection.connections:
                new = copy.deepcopy(current)
                new.add_connection(next_connection)
            self.stack.push(new)
            i += 1
        return len(self.stack.items)