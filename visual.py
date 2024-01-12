from matplotlib import pyplot as plt

x_values = []
y_values = []

with open(f"data/StationsHolland.txt") as f:
    # skip first line
    next(f)
    line = f.readline()
    while line != "\n":
        # remove newline character and split into different parts
        parts = line.split(",")
        # set the different parts of the line to its variable
        try:
            x_coord = float(parts[1])
        except(IndexError):
            break
        try:
            y_coord = float(parts[2].strip("\n"))
        except(IndexError):
            break
        x_values.append(x_coord)
        y_values.append(y_coord)
        line = f.readline()

plt.scatter(x_values, y_values)
plt.show()