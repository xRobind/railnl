from stations import Station

class RailNL:

    def __init__(self) -> None:
        # initialise lists that contain stations as objects of the class,
        # and connections as a dict that links the connection to the time
        self.stations = []
        self.connections = {}

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

x = RailNL()