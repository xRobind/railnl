import matplotlib.pyplot as plt

# dictionaries with information about size (number of connections) of stations
# and about their coordinates
size_of_station = {}
connections = []
x_station = {}
y_station = {}


with open(f"data/StationsHolland.txt") as f:
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
        size_of_station[station] = 0
        x_station[station] = x_coord
        y_station[station] = y_coord

        # next line
        line = f.readline()

with open(f"data/ConnectiesHolland.txt") as f:
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
        size_of_station[station] += 1
        size_of_station[connection] += 1
        connections.append((station, connection))

        # next line
        line = f.readline()

# make a list of all the different sizes
sizes = []
for station in size_of_station:
    sizes.append((size_of_station[station] + 1) ** 4)

# make lists of all coordinates
x_values = []
y_values = []
for station in x_station:
    x_values.append(x_station[station])
    y_values.append(y_station[station])

# size of the figure
plt.figure(figsize=(12,20))
# scatter the stations with their corresponding size, 
# stations with the same size have the same color
plt.scatter(x_values, y_values, s=sizes, c=sizes)

# make lists of all connections and plot them
for line in connections:
    station, connection = line
    x_values = [x_station[station], x_station[connection]]
    y_values = [y_station[station], y_station[connection]]
    plt.plot(x_values, y_values, '-', color='blue', alpha=0.33)

plt.axis('off')
plt.savefig("visual_representation.png")
plt.show()