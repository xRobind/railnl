from stations import Station

import random


class RailNL:

    def __init__(self) -> None:
        # initialise lists/dicts that contain stations as objects of the class,
        # connections as a dict that links the connection to the time,
        # and trajectories made
        self.stations = []
        self.connections = {}
        self.trajectories

        # load station structures and connections 
        self.load_stations(f"data/StationsHolland.txt")
        self.load_connections(f"data/ConnectiesHolland.txt")

    def load_stations(self, filename):
        # open file, read the lines and split into the three parts
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
                self.connections[f"{name} -> {connection}"] = time
                
                # read new line
                line = f.readline()

    def start_trajectory(self):
        """initialize a trajectory with a starting station and amount of stops
        that it will make
        """
        # random starting station from our list of station objects
        starting_station = random.choice(self.stations)
        # random number of stops between 4 and 7
        number_of_connections = random.randrange(4, 8)

        # add the starting station as a key and the number of stops as value
        # to all trajectories
        self.trajectories[starting_station] = number_of_connections
    
    def continue_trajectory(self, trajectory):
        pass

x = RailNL()