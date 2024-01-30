import matplotlib.pyplot as plt
import matplotlib
import numpy as np

class Visualisation:

    def __init__(self, region, trajectories) -> None:
        # dictionaries with information about size (number of connections) of stations
        # and about their coordinates
        # the lists and dicts are all ordered the same way as the data files
        self.size_of_station = {}
        self.connections = []
        self.x_station = {}
        self.y_station = {}

        # a region (str) and the trajectories (list of objects from class Trajectory)
        self.region = region
        self.trajectories = trajectories

        matplotlib.use("TkAgg")

    def load_stations(self):
        with open(f"data/Stations{self.region}.txt") as f:
            # skip first line
            next(f)
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",")
                # set the different parts of the line to its variable
                station = str(parts[0])
                try:
                    y_coord = float(parts[1])
                except(IndexError):
                    break
                try:
                    x_coord = float(parts[2].strip("\n"))
                except(IndexError):
                    break

                # add station to the dictionary with a default size of 0 connections
                # and add station to the dictionaries with its coordinates
                self.size_of_station[station] = 0
                self.x_station[station] = x_coord
                self.y_station[station] = y_coord

                # next line
                line = f.readline()
        
        # make separate lists of all coordinates for plotting
        self.x_values = []
        self.y_values = []
        for station in self.x_station:
            self.x_values.append(self.x_station[station])
            self.y_values.append(self.y_station[station])

    def load_sizes(self):
        with open(f"data/Connecties{self.region}.txt") as f:
            # skip first line
            next(f)
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",")
                # set the different parts of the line to its variable
                try:
                    connection = str(parts[1])
                except(IndexError):
                    break
                station = str(parts[0])

                # add 1 connection to the size of the connected stations
                self.size_of_station[station] += 1
                self.size_of_station[connection] += 1

                # next line
                line = f.readline()

        # make separate list of all the different sizes for plotting
        self.sizes = []
        if self.region == "Holland":
            for station in self.size_of_station:
                self.sizes.append((self.size_of_station[station] + 1) ** 2)
        else:
            for station in self.size_of_station:
                self.sizes.append(self.size_of_station[station])

    def get_connections(self):
        # for each trajectory, create a list that saves the name of the
        # stations in the trajectory
        for trajectory in self.trajectories:
            stations = []

            for station in trajectory.stations:
                stations.append(station.name)

            # add each connection as a tuple to the list of connections
            for i in range(0, len(stations) - 1):
                self.connections.append((stations[i], stations [i + 1]))

    def draw(self):
        # determine size of the figure and remove axes
        plt.figure()
        img = plt.imread(f"code/visual/maps/{self.region}_empty.jpeg")
        plt.axis('off')
        # scatter the stations with their corresponding size, 
        # stations with the same size have the same color
        plt.scatter(self.x_values, self.y_values, s=self.sizes)
        if self.region == "Holland":
            plt.imshow(img, extent=[4.1, 5.25, 51.7, 53.18])
        else:
            plt.imshow(img, extent=[3.1, 7.5, 50.6, 53.7])


        # make lists of all connections and plot them
        for line in self.connections:
            station, connection = line
            self.x_values = [self.x_station[station], self.x_station[connection]]
            self.y_values = [self.y_station[station], self.y_station[connection]]
            plt.plot(self.x_values, self.y_values, '-', c="b", alpha=0.33)
            # draw the connections
            plt.draw()
            plt.pause(.1)

        # plt.savefig(f"railmap_{self.region}.png")
        plt.show()

    def histogram(self, K_values, iterations):
        """plot a histogram of the quality of all the solutions
        """
        plt.title(f"Histogram of K-values ({self.region})")
        if iterations > 400:
            plt.hist(K_values, int(iterations / 4))
        else:
            plt.hist(K_values, int(iterations))
        # plt.savefig(f"hist_{self.region}.png")
        plt.show()

    def boxplot(self, all_K_values):
        """plot the K's of all algorithms and their averages next to eachother
        for comparison reasons.
        """
        print(all_K_values)
        try:
            plt.title("K's of our algorithms")
            plt.boxplot(all_K_values, showfliers=True, labels=["baseline", "hill climber", "pool", "simulated annealing"])
            # plt.savefig(f"boxplot_compare_{self.region}")
            plt.show()
        except(ValueError):
            plt.title("K-values")
            plt.boxplot(all_K_values, showfliers=True)
            # plt.savefig(f"boxplot_{self.region}")
            plt.show()
        


