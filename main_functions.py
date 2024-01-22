# this file contains functions that retrieves input from a user,
# and handles our different algorithms

from code.algorithms.baseline import Baseline
from code.visual.visual import Visualisation
from code.algorithms.iterativedeepening import IDS


class Main:

    def __init__(self) -> None:
        """Initiates a list to save all K's, a variable to save the highest K,
        and a variable to set how many iterations there will be done.
        """        
        self.K_values = []
        self.highest_K = 0
        self.iterations = 1000

    def algorithm_and_region(self):
        """This method asks the user to fill in the algorithm and region
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")

        # tot nu toe alleen nog maar baseline
        while self.algorithm not in ["baseline", "hill climber", "beam"]:
            self.algorithm = \
            input("Please provide an algortihm in the command line.\n\
        Options:\n\
        baseline\n\
        hill climber\n\
        beam\n\n")
            
        # retrieve region
        self.region = input("\nWhich region?\n")

        # Holland of Nederland
        while self.region != "Holland" and self.region != "Nederland":
            self.region = \
            input("\nChoose a region: Holland or Nederland (case-sensitive).\n")

        # get max trajectories
        self.max = int(input("\nWhat is the maximum of trajectories?\n"))

        # must be between 1 and 7
        while self.max < 1 or self.max > 7:
            self.max = \
        int(input("\nMaximum number of trajectories must be between 1 and 7.\n"))

        print(f"\nUsing {self.algorithm} algorithm in {self.region} \
        {self.iterations} times...")

    def beam(self):
        test = IDS(self.max, self.region)
        print(test.start_trajectory())
        
    def baseline(self):
        """this method carries out the baseline algorithm
        """
        for i in range(0, self.iterations):
            # initialise and run baseline algorithm
            rail = Baseline(self.max, self.region)
            run = "new trajectory"
            
            # continue trajectories until it doesn't create a new
            while run == "new trajectory" and len(rail.trajectories) < self.max:

                # create new trajectory and continue it
                trajectory = rail.start_trajectory()
                run = rail.continue_trajectory(trajectory)

                while run == "continue":
                    run = rail.continue_trajectory(trajectory)

                # calculate K and add it to list of all K's
                K_value = rail.calculate_K()
                self.K_values.append(K_value)

                # save the rail with highest K
                if self.highest_K < K_value:
                    self.highest_K = K_value
                    self.best_rail = rail
    
    def hill_climber(self):
        for i in range(0, self.iterations):

    def visualisation(self):
        """This method carries out the visualisation.
        """
        # plot rails of best_rail
        x = Visualisation(self.region, self.best_rail.trajectories)
        x.load_stations()
        x.load_sizes()
        x.get_connections()

        # plot map of the best lijnvoering
        x.draw()
        # plot histogram of all K's
        x.histogram(self.K_values, self.iterations)


        
