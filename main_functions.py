# this file contains functions that retrieves input from a user,
# and handles our different algorithms

from code.algorithms.baseline import Baseline


def algorithm_and_region():
    # retrieve existing algorithm
    algorithm = input("Which algorithm?\n")
    # tot nu toe alleen nog maar baseline
    while algorithm != "baseline":
        algorithm = input("Please provide an algortihm in the command line.\n\
    Options:\n\
    baseline\n\n")
        
    # retrieve region
    region = input("Which region?\n")
    # Holland of Nederland
    while region != "Holland" and region != "Nederland":
        region = input("Choose a region: \
Holland or Nederland (case-sensitive).\n")
        
    return algorithm, region

def baseline(region):
    # get max trajectories
    max = int(input("What is the maximum of trajectories?\n"))

    K_values = []
    iterations = 1000

    print(f"Using Baseline algorithm {iterations} times and plotting Histogram..")

    for i in range(0, iterations):
        # initialise and run baseline algorithm
        rail = Baseline(max, region)
        run = "new trajectory"
        
        # continue trajectories until it doesn't create a new
        while run == "new trajectory" and len(rail.trajectories) < max:

            trajectory = rail.start_trajectory()
            run = rail.continue_trajectory(trajectory)
            while run == "continue":

                run = rail.continue_trajectory(trajectory)

            K_value = rail.calculate_K()
            K_values.append(K_value)

    rail.histogram(K_values, 1000)