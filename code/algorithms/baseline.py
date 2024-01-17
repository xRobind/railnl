from code.classes.stations import Station
from code.classes.trajectory import Trajectory

import random
import matplotlib.pyplot as plt


class Baseline:
    """This class reads data from csv files about train stations in Holland,
    saves them in classes and uses them to create imaginary trains that follow
    a trajectory through the saved train stations.
    This process continues until all saved connections between two specific
    stations are used. It then uses a known formula to calculate the quality
    of the lines. The goal is to implement its methods in such a way that the
    quality of the lines will end up the closest to the number 10000.
    """    

    def __init__(self, max, region) -> None:
        """initialise lists that contain stations as objects of the class,
        connections as a dict that links the connection to the time,
        and trajectories made and time spent
        """
        self.stations = []
        self.connections = []
        self.trajectories = []
        self.total_time = 0

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
                time = int(parts[2].strip("\n"))

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

    def start_trajectory(self):
        """initialize a trajectory with a starting station and amount of stops
        that it will make
        """
        # random starting station from our list of station objects
        starting_station = random.choice(self.stations)

        # create trajectory with starting station, add to the Trajectory class
        trajectory = Trajectory(starting_station)
        self.trajectories.append(trajectory)

        return trajectory
    
    def continue_trajectory(self, trajectory):
        """continue a trajectory by choosing between available connections
        of the current station and updating the current one to the next one,
        except if we've reached the end.

        Returns "continue" if continued, "new trajectory" if not because the
        2hrs are over,
        "all connections used" if not because all connections have been
        used and the goal has been reached.
        """
        # get available connections
        station = trajectory.stations[-1]
        connections = station.connections
        # choose a random connection
        chosen_connection = random.choice(connections)
        #calculate probability train stops
        if random.random() < ((1 / (len(connections)+1)) * (trajectory.time / 120)):
            if random.random() < ((1/7)**(7-len(self.trajectories))):
                return "stop"
            return "new trajectory"
            
        # get the travel time by finding the chosen connection
        # in the dict where it's time is mapped
        time = self.get_time(station, chosen_connection)

        # add travel time if it stays under 2hrs, otherwise stop
        # add to total time and start new trajectory
        if (trajectory.time + time) > 120:
            self.total_time += trajectory.time
            if random.random() < ((1/7)**(7-len(self.trajectories))):
                return "stop"
            return "new trajectory"
        else:
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

        if (chosen_connection, station.name) in self.connections:
            self.connections.remove((chosen_connection, station.name))

            if len(self.connections) == 0:
                return "stop"

        return "continue"
    
    def get_time(self, station, chosen_connection):
        """get the travel time by finding the chosen connection
        in the dict where it's time is mapped
        """        
        for connection in station.connection_time:
            if connection == chosen_connection:
                return station.connection_time[connection]


    def calculate_K(self):
        """calculate the quality of the lijnvoering
        """        
        T = len(self.trajectories)
        p = (self.total_connections - len(self.connections)) / self.total_connections
        return 10000 * p - (T * 100 + self.total_time)

    def histogram(self, max):
        """plot a histogram of the quality of all the solutions
        """        
        K_values = []
        x = 1000

        for i in range(x):
            rail = Baseline(max, "Holland")
            run = "new trajectory"
            
            while run == "new trajectory" and len(rail.trajectories) < 7:

                trajectory = rail.start_trajectory()
                run = rail.continue_trajectory(trajectory)
                while run == "continue":

                    run = rail.continue_trajectory(trajectory)
                    
            K = rail.calculate_K()
            K_values.append(K)

        plt.hist(K_values, 1000)
        plt.show()