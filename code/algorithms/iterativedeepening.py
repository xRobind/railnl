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
from code.classes.schedule import Schedule

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
                connection_id = 0
                for station in self.stations:
                    if name == station.name:
                        for station2 in self.stations:
                            if station2.name == connection:
                                connection_object = Connection(station, station2, time)
                                station.add_connection(connection_object)
                                self.connections.append(connection_object)
                                connection_object2 = Connection(station2, station, time)
                                station2.add_connection(connection_object2)
                                self.connections.append(connection_object2)
                                connection_object.add_corresponding_connection(connection_object2)
                                connection_object2.add_corresponding_connection(connection_object)
                                
                    # if connection == station.name:
                        # for station1 in self.stations:
                            # if station1.name == name:
                                # connection_object = Connection(station, station1, time)
                                # station.add_connection(connection_object)
                                # self.connections.append(connection_object)
                                
        # for connection in self.connections:
            # for connection2 in self.connections:
                # if connection.connection == connection2.station and connection.station == connection2.connection:
                    # print("het lukt")
                    # connection.add_corresponding_connection(connection2)

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
                    new.add_connection_and_time(second_connection, 120)
                    new = [new]
                    ## add trajectory to schedule
                    self.stack.push(Schedule(new, self.connections))
        # for item in self.stack.items:
            # print(item.calculate_K())
            # print(item.trajectories[-1].time, item.time)

    def continue_trajectory(self):
        # depth 2
        depth = 16
        number_trajectories = 3
        yeh = False
        while(yeh == False):
            current = self.stack.pop()
            for next_connection in current.trajectories[-1].stations[-1].connection.connections:
                new = copy.deepcopy(current)
                if new.trajectories[-1].add_connection_and_time(next_connection, 120):
                    if len(new.trajectories[-1].stations) < depth:
                        print(len(new.trajectories[-1].stations))
                        self.stack.push(new)
                        # print(new.trajectories[-1].time)
                        print(new.calculate_K())
                elif len(new.trajectories) <  number_trajectories:
                    for connection in new.connections_over:
                        trajectory = Trajectory(connection)
                        new2 = copy.deepcopy(new)
                        new2.add_trajectory(trajectory)
                        self.stack.push(new2)
                if new.calculate_K() > 6500:
                    for i in range(len(new.trajectories[-1].stations)):
                        print(new.trajectories[-1].stations[i].station.name, new.trajectories[-1].stations[i].connection.name)
                    for i in range(len(new.trajectories[-2].stations)):
                        print(new.trajectories[0].stations[i].station.name, new.trajectories[0].stations[i].connection.name)
                    print(len(new.connections_used))
                    yeh = True

