# this file contains functions that retrieves input from a user,
# and handles our different algorithms

from code.algorithms.baseline import Baseline
from code.algorithms.hill_climber import Hillclimber
from code.algorithms.iterativedeepening import IDS
from code.algorithms.random_change import Random_change

from code.visual.visual import Visualisation


class Main:

    def __init__(self) -> None:
        """Initiates a list to save all K's, a variable to save the highest K,
        a variable to set how many iterations there will be done, and a list 
        to store the trajectories made.
        """        
        self.K_values = []
        self.all_K_values = []
        self.highest_K = 0
        self.iterations = 100
        self.trajectories = None

    def user_input(self):
        """This method asks the user to fill in the algorithm, region,
        and the max trajectories to be used in a railmap
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")

        # choose between all our algorithms
        while self.algorithm not in \
                    ["baseline", "hill climber", "beam", "random", "all"]:
            self.algorithm = \
            input("Please provide an algortihm in the command line.\n\
        Options:\n\
        baseline\n\
        hill climber\n\
        beam\n\
        random\n\
        all\n\n")
            
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

    def baseline(self):
        """This method carries out the baseline algorithm
        """
        # let the user know the algorithm is running
        print(f"\nUsing Baseline algorithm in {self.region} \
{self.iterations} times...")
        
        # repeat a specified number of times
        for i in range(0, self.iterations):
            # initialise and run baseline algorithm
            rail = Baseline(self.max, self.region)

            # continue trajectories until it doesn't create a new
            while True:

                # create new trajectory
                trajectory = rail.start_trajectory()

                # check for maximum of trajectories
                if trajectory == "stop":
                    break

                # continue a trajectory
                run = rail.continue_trajectory(trajectory)
                while run == "continue":
                    run = rail.continue_trajectory(trajectory)
                
                # stop if a stopping condition is met
                if run == "stop":
                    break

                # calculate K and add it to list of all K's
                K_value = rail.calculate_K()
                self.K_values.append(K_value)

                # save the rail with highest K
                if self.highest_K < K_value:
                    self.highest_K = K_value
                    self.trajectories = rail.trajectories
    
        self.all_K_values.extend(self.K_values)

    def hill_climber(self):
        # let the user know the algorithm is running
        print(f"\nUsing Hill Climber algorithm in {self.region}")

        rail = Hillclimber(self.max, self.region)
        solution = rail.random_railmap()
        node = rail.change_node()

    def beam(self):
        # let the user know the algorithm is running
        print(f"\nUsing Iterative Deepening algorithm in {self.region}")

        test = IDS(self.max, self.region)
        print(test.start_trajectory())
        print(test.continue_trajectory())

    def random_change(self):
        amount = \
    int(input("\nHow many random trajectories do you want to create?\n"))
        
        changes = \
    int(input("\nHow many times do you want to update the train table?\n"))
        
        # let the user know the algorithm is running
        print(f"\nUsing Random algorithm in {self.region} {amount} times...")
        
        # initiate the algorithm
        rail = Random_change(self.max, self.region, amount)

        for i in range(0, changes):
            rail.change_trajectory()

        self.trajectories = rail.train_table
        self.K_values = rail.K
        self.all_K_values.extend([rail.K])

    def visualisation(self):
        """This method carries out the visualisation.
        """
        assert self.trajectories is not None,\
            "\n\nYou need to set the trajectories made to self.trajectories.\
            Check the end of baseline method in class Main for example.\n"
            
        # plot rails of best_rail
        v = Visualisation(self.region, self.trajectories)
        v.load_stations()
        v.load_sizes()
        v.get_connections()

        # plot map of the best lijnvoering
        v.draw()
        # plot histogram of all K's from a single algorithm
        v.histogram(self.K_values, self.iterations)
        # plot all K's next to eachother from all algorithms
        v.boxplot(self.all_K_values)



        
