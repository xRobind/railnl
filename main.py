from code.algorithms.baseline import Baseline

if __name__ == "__main__":
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
        region = input
        ("Choose a region: Holland or Nederland (case-sensitive).")

    # execution of baseline algorithm
    if algorithm == "baseline":
        # get max trajectories
        max = input("What is the maximum of trajectories?\n")
        print
        ("Using Baseline algorithm a number of times and plotting Histogram..")

        # initialise and run baseline algorithm
        rail = Baseline(max, region)
        run = "new trajectory"
        
        # continue trajectories until it doesn't create a new
        while run == "new trajectory" and len(rail.trajectories) < 7:

            trajectory = rail.start_trajectory()
            run = rail.continue_trajectory(trajectory)
            while run == "continue":

                run = rail.continue_trajectory(trajectory)
        
        # plot a histogram of all K's
        rail.histogram()

    

    

    

    




