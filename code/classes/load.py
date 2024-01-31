from code.classes.stations import Station

class Load:
    """This class loads data from csv files about stations and their
    connections and saves them in lists.
    """

    def __init__(self, region: str) -> None:
        """Initialises the needed lists and variables.
        """
        self.stations_list: list[Station] = []
        self.connections_list: list[tuple[str, str]] = []
        self.region = region

    def stations(self) -> list[Station]:
        """Open file, read the lines and split into the three parts and save.
        """
        with open(f"data/Stations{self.region}.txt") as f:
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
                self.stations_list.append(station)

                # read new line
                line = f.readline()

        return self.stations_list
    
    def connections(self) -> list[tuple[str, str]]:
        """Open file, read the lines and split into the three parts and save.
        """
        with open(f"data/Connecties{self.region}.txt") as f:
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
                if self.region == "Holland":
                    time = int(parts[2].strip("\n"))
                else:
                    time = float(parts[2].strip("\n"))

                # add connection to connection list in Station class,
                # and the list of all connections,
                # for both stations
                for station in self.stations_list:
                    if name == station.name:
                        station.add_connection(connection, time)
                    if connection == station.name:
                        station.add_connection(name, time)

                # add the connection and time to the list of all connections
                self.connections_list.append((name, connection))

                # read new line
                line = f.readline()

        return self.connections_list