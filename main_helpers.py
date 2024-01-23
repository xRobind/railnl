# this file contains functions that retrieves input from a user,
# and handles our different algorithms

from code.algorithms.baseline import Baseline
from code.algorithms.hill_climber import Hillclimber
from code.visual.visual import Visualisation
from code.algorithms.iterativedeepening import IDS


class Main:

    def __init__(self) -> None:
        """Initiates a list to save all K's, a variable to save the highest K,
        and a variable to set how many iterations there will be done.
        """        
        self.K_values = []
        self.all_K_values = []
        self.highest_K = 0
        self.iterations = 100

    def user_input(self):
        """This method asks the user to fill in the algorithm, region,
        and the max trajectories to be used in a railmap
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")

        # choose between all our algorithms
        while self.algorithm not in \
                                ["baseline", "hill climber", "beam", "all"]:
            self.algorithm = \
            input("Please provide an algortihm in the command line.\n\
        Options:\n\
        baseline\n\
        hill climber\n\
        beam\n\
        all/n\n")
            
        # retrieve region
        self.region = input("\nWhich region?\n")

        # Holland or Nederland
        while self.region != "Holland" and self.region != "Nederland":
            self.region = \
        input("\nChoose a region: Holland or Nederland (case-sensitive).\n")

        # get max trajectories
        self.max = int(input("\nWhat is the maximum of trajectories?\n"))

        # must be between 1 and 7
        while self.max < 1 or self.max > 45:
            self.max = \
        int(input("\nMaximum number of trajectories must be between 1 and 45.\n"))

        # let the user know the algorithm is running
        print(f"\nUsing {self.algorithm} algorithm in {self.region} \
{self.iterations} times...")

    def beam(self):
        test = IDS(self.max, self.region)
        print(test.start_trajectory())
        print(test.continue_trajectory())
        
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
    
        self.all_K_values.extend(self.K_values)

    # def hill_climber(self):
    #     for i in range(0, self.iterations):
    
    def hill_climber(self):
        
        rail = Hillclimber(max, self.region)
        solution = rail.random_railmap()
        node = rail.change_node()
        
        
        


    def visualisation(self):
        """This method carries out the visualisation.
        """
        # plot rails of best_rail
        v = Visualisation(self.region, self.best_rail.trajectories)
        v.load_stations()
        v.load_sizes()
        v.get_connections()

        # plot map of the best lijnvoering
        v.draw()
        # plot histogram of all K's from a single algorithm
        v.histogram(self.K_values, self.iterations)
        # plot all K's next to eachother from all algorithms
        if len(self.all_K_values) == 3:
            v.boxplot(self.all_K_values)



        
