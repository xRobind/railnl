# this file contains functions that retrieves input from a user,
# and handles our different algorithms

from code.algorithms.baseline import Baseline
from code.algorithms.hill_climber import Hillclimber
from code.algorithms.iterativedeepening import IDS
from code.algorithms.pool import Pool

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
        self.iterations = 1000
        self.trajectories = None

    def user_input(self):
        """This method asks the user to fill in the algorithm, region,
        and the max trajectories to be used in a railmap
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")
        # self.algorithm = "hill climber"

        # choose between all our algorithms
        while self.algorithm not in \
                    ["baseline", "hill climber", "beam", "pool", "all"]:
            self.algorithm = \
            input("Please provide an algortihm in the command line.\n\
        Options:\n\
        baseline\n\
        hill climber\n\
        beam\n\
        pool\n\
        all\n\n")
            
        # retrieve region
        self.region = input("\nWhich region?\n")
        # self.region = "Holland"

        # Holland or Nederland
        while self.region != "Holland" and self.region != "Nederland":
            self.region = \
        input("\nChoose a region: Holland or Nederland (case-sensitive).\n")

        # get max trajectories
        self.max = int(input("\nWhat is the maximum of trajectories?\n"))
        # self.max = 7

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
        
        # initialise baseline algorithm
        rail = Baseline(self.max, self.region)

        # repeat a specified number of times
        for i in range(0, self.iterations):
            # empty railmap info
            rail.trajectories = []
            rail.total_time = 0

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

                # calculate K and add it to list of all K's
                K_value = rail.calculate_K()
                self.K_values.append(K_value)

                # save the rail with highest K
                if self.highest_K < K_value:
                    self.highest_K = K_value
                    self.trajectories = rail.trajectories

                # stop if a stopping condition is met
                if run == "stop":
                    break
    
        self.all_K_values.extend(self.K_values)

    def hill_climber(self):
        # let the user know the algorithm is running
        print(f"\nUsing Hill Climber algorithm in {self.region}")

        hillclimber_instance = Hillclimber(self.max, self.region)
        iterations = 2
        quality_threshold = 7500
        hillclimber_instance.random_railmap()
        self.K_values.append(hillclimber_instance.original_quality)
        hillclimber_instance.choose_random_trajectory()

        for iteration in range(iterations):
            hillclimber_instance.change_node()
            quality = hillclimber_instance.compare_K_values()
            self.K_values.append(quality)
            
        # Check for the quality threshold and break if met
            if hillclimber_instance.original_quality >= quality_threshold:
                print(f"Quality threshold reached.")
                break

        self.trajectories = hillclimber_instance.trajectories
        self.all_K_values.extend(self.K_values)

    def beam(self):
        # let the user know the algorithm is running
        print(f"\nUsing Iterative Deepening algorithm in {self.region}")

        test = IDS(self.max, self.region)
        test.start_trajectory()
        test.continue_trajectory()

    def pool(self):
        amount = \
    int(input("\nHow many random trajectories do you want to create?\n"))
        
        changes = \
    int(input("\nHow many times do you want to update the train table?\n"))
        
        # let the user know the algorithm is running
        print(f"\nUsing Random algorithm in {self.region} {changes} times...")
        
        # initiate the algorithm
        rail = Pool(self.max, self.region, amount)

        for i in range(0, changes):
            rail.change_trajectory(self.random_trajectory, self.changed_trajectory)

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



        
