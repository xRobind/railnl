from stations import Station

class RailNL:

    def __init__(self) -> None:
        self.stations = []
            
    def load_stations(self, filename):
        # open file, read the lines and split into the three parts
        with open(filename) as f:
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",", 2)

                name = parts[0]
                connection = parts[1]
                time = int(parts[2].strip("\n"))

                # create the room, add room to self.rooms
                station = Station(name, connection, time)
                self.stations.append(station)

                # read new line
                line = f.readline()