import random
import sys
import matplotlib.pyplot as plt
import copy
import gc

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
        if region == "Holland":
            self.time = 120
            self.goal = 8800
        else:
            self.time = 180
            self.goal = 5000

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
                
        for station in self.stations:
            station.nmbr()    
            
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
                    new.add_connection_and_time(second_connection, self.time)
                    new = [new]
                    ## add trajectory to schedule
                    self.stack.push(Schedule(new, self.connection_dict))
        # for item in self.stack.items:
            # print(item.calculate_K2())
            # print(item.trajectories[-1].time, item.time)

    def continue_trajectory(self):
        # depth 2
        number_trajectories = max
        depth = 4
        yeh = False
        nr_con = 0
        add_trajectory = False

        while(yeh == False):
            try:
                current = self.stack.pop()
            except AssertionError:         
                return self.list_all[-1], self.list_all[-1].calculate_K2()
                
                
            for next_connection in current.trajectories[-1].stations[-1].connection.connections:
                len(current.trajectories[-1].stations[-1].connection.connections)
                if current.trajectories[-1].stations[-1].corresponding.connection_id != next_connection.connection_id: 
                    new = copy.deepcopy(current)
                    if new.trajectories[-1].add_connection_and_time(next_connection, self.time):
                        if len(new.trajectories[-1].stations) == depth:
                            nr_con += 1
                            new.calculate_K2()
                            self.list_all.append(new)
                        else:
                            self.stack.push(new)

                        
                    if len(self.stack.items) == 1:
                        self.list_all.sort(key=lambda x: x.score)
                        new = self.list_all[-1]
                        print(new.calculate_K2())
                        if(new.calculate_K2() > self.goal):
                            return new, new.calculate_K2()
                            
                        print(new.trajectories[-1].time, len(new.connections_used), len(new.all_connections), len(new.connections_over))
                        for i in range(len(new.trajectories)):
                            print("nieuwe")
                            for j in range(len(new.trajectories[i].stations)):
                                print(new.trajectories[i].stations[j].station.name, new.trajectories[i].stations[j].connection.name)                           
                        for i in range(60, 1, -1):
                            self.stack.push(self.list_all[-i])
                            
                        if nr_con == 0:
                            print(len(self.list_all))
                            self.list_all.clear()
                            
                            while len(self.stack.items) > 1:
                                n = self.stack.pop()
                                if(self.max_trajectories == len(n.trajectories)):
                                    return self.list_all[-1], self.list_all[-1].calculate_K2()
                                
                                n.connections_over.sort(key = lambda x: self.connection_dict[x].station.nmbr_connections)
                                
                                for connection_id in n.connections_over[:30]:
                                    trajectory = Trajectory(self.connection_dict[connection_id])
                                    trajectory.add_first_time()
                                    new2 = copy.deepcopy(n)
                                    new2.add_trajectory(trajectory)
                                    new2.calculate_K2()
                                    self.list_all.append(new2) 
                            self.list_all.sort(key=lambda x: x.score)
                            for i in range(60, 1, -1):
                                self.stack.push(self.list_all[-i])
                            print(len(self.stack.items), len(self.stack.items[-1].trajectories))                              
                            depth = 0
                        nr_con = 0
                        depth += 2
                           
                        