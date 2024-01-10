from stations import Station
from trajectory import Trajectory

import random


class RailNL:

    def __init__(self) -> None:
        # initialise lists/dicts that contain stations as objects of the class,
        # connections as a dict that links the connection to the time,
        # and trajectories made
        self.stations = []
        self.connections = {}
        self.trajectories = []

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

        # create trajectory with starting station, add to the Trajectory class
        trajectory = Trajectory(starting_station)
        self.trajectories.append(trajectory)

        return trajectory
    
    def continue_trajectory(self, trajectory):
        """continue a trajectory by choosing between available connections
        of the current station and updating the current one to the next one,
        except if we've reached the end.
        Returns True if continued, False if not because the 2hrs are over.

        accepts a trajectory from self.trajectories
        """
        # get available connections
        station = trajectory.stations[-1]
        connections = station.connections
        # choose a random connection
        chosen_connection = random.choice(connections)

        # get the travel time by finding the chosen connection
        # in the dict where it's time is mapped
        for connection in station.connection_time:
            if connection == chosen_connection:
                time = station.connection_time[connection]

        # add travel time if it stays under 2hrs
        if (trajectory.time + time) > 120:
            return False
        else:
            trajectory.add_time(time)

            # add connected station as an object by searching for it by name
            for item in self.stations:
                if item.name == chosen_connection:
                    trajectory.add_connection(item)

        return True

if __name__ == "__main__":
    rail = RailNL()
    trajectory = rail.start_trajectory()
    
    run = rail.continue_trajectory(trajectory)
    while run is True:
        run = rail.continue_trajectory(trajectory)



