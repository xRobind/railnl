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
        self.connection_dict = {}
        self.stack = Stack()
        self.stack2 = Stack()
        self.list_all = []

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
        connection_id = 1
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
                                connection_object = Connection(station, station2, time, connection_id)
                                station.add_connection(connection_object)
                                self.connections.append(connection_object)
                                self.connection_dict[connection_id] = connection_object
                                connection_id += 1
                                connection_object2 = Connection(station2, station, time, connection_id)
                                station2.add_connection(connection_object2)
                                self.connections.append(connection_object2)
                                self.connection_dict[connection_id] = connection_object2
                                connection_id += 1
                                connection_object.add_corresponding_connection(connection_object2)
                                connection_object2.add_corresponding_connection(connection_object)
                

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
                current.add_first_time()
                for second_connection in current.stations[-1].connection.connections:
                    new = copy.deepcopy(current)
                    new.add_connection_and_time(second_connection, 120)
                    new = [new]
                    ## add trajectory to schedule
                    self.stack.push(Schedule(new, self.connection_dict))
        # for item in self.stack.items:
            # print(item.calculate_K2())
            # print(item.trajectories[-1].time, item.time)

    def continue_trajectory(self):
        # depth 2
        number_trajectories = 2
        depth = 4
        yeh = False
        
        for number_trajectories in range(3):
            depth = 4
            while(yeh == False):
                current = self.stack.pop()
   
                ##get all new connections
                for next_connection in current.trajectories[-1].stations[-1].connection.connections:
                    if current.trajectories[-1].stations[-1].corresponding.connection_id != next_connection.connection_id:            
                        new = copy.deepcopy(current)
                        if new.trajectories[-1].add_connection_and_time(next_connection, 120):
                            if len(new.trajectories[-1].stations) == depth:
                                new.calculate_K2()
                                self.list_all.append(new)
                            else:
                                self.stack.push(new)

                # if len(new.trajectories[-1].stations) == depth:
                    # self.list_all.append(new.calculate_K2())
                        
                        
                            # add new trajectory to schedule
                        if len(new.trajectories) <  number_trajectories and new_trajectory == True:
                            new.calculate_K2()
                            for connection_id in new.connections_over:
                                print("hij maakt nieuwe trajectorie")
                            # print(len(new.connections_over), len(new.connections_used), len(new.all_connections))
                                trajectory = Trajectory(self.connection_dict[connection_id])
                                trajectory.add_first_time()
                                new2 = copy.deepcopy(new)
                                new2.add_trajectory(trajectory)
                                self.stack.push(new2)
                        
                        # self.list_all.append(new.calculate_K2())
                        if len(self.stack.items) == 1:
                            self.list_all.sort(key=lambda x: x.score)
                            new = self.list_all[-100]
                            print(new.trajectories[-1].time, len(new.connections_used), len(new.all_connections), len(new.connections_over))
                            for i in range(len(new.trajectories)):
                                print("nieuwe")
                                for j in range(len(new.trajectories[i].stations)):
                                    print(new.trajectories[i].stations[j].station.name, new.trajectories[i].stations[j].connection.name)                           
                            for i in range(200, 1, -1):
                                self.stack.push(self.list_all[-i])
                            print(len(self.stack.items))
                            depth += 4
                        if depth > 15:
                            yeh = True
                        
                            ##found good result
                        # if new.calculate_K2() > 4000:
                            # print(new.trajectories[-1].time, len(new.connections_used), len(new.all_connections), len(new.connections_over))
                            # for i in range(len(new.trajectories)):
                                # print("nieuwe")
                                # for j in range(len(new.trajectories[i].stations)):
                                    # print(new.trajectories[i].stations[j].station.name, new.trajectories[i].stations[j].connection.name)
                            # self.stack2.push(new)
                            # if len(self.stack2.items) == 100:
                                # self.stack.items.clear()
                                # for i in range(len(self.stack2.items)):
                                    # self.stack.push(self.stack2.pop)
                                    # yeh = True

