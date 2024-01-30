# this file contains functions that retrieves input from a user,
# and handles our different algorithms
import csv

from code.algorithms.baseline import Baseline
from code.algorithms.hill_climber import Hillclimber
from code.algorithms.iterativedeepening import IDS
from code.algorithms.pool import Pool
from code.algorithms.simulated_annealing import Simulated_annealing

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

        self.K_value_output = 0

    def user_input(self):
        """This method asks the user to fill in the algorithm, region,
        and the max trajectories to be used in a railmap
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")
        # self.algorithm = "simulated annealing"



        # choose between all our algorithms
        while self.algorithm not in \
                    ["baseline", "hill climber", "beam", "pool","simulated annealing", "all"]:
            self.algorithm = \
            input("Please provide an algortihm in the command line.\n\
        Options:\n\
        baseline\n\
        hill climber\n\
        beam\n\
        pool\n\
        simulated annealing\n\
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
        # self.max = 20

        # must be between 1 and 7
        while self.max < 1 or self.max > 45:
            self.max = \
        int(input("\nMaximum number of trajectories must be between 1 and 45.\n"))

    def baseline(self):
        # reset K's
        self.K_values = []
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
                    self.K_value_output = self.highest_K


                # stop if a stopping condition is met
                if run == "stop":
                    break

        # extend the list of all K's and reset highest K
        self.all_K_values.append(self.K_values)
        self.highest_K = 0

    def hill_climber_2(self):
        # reset K's
        self.K_values = []
        # let the user know the algorithm is running
        print(f"\nUsing Hill Climber algorithm in {self.region}")

        hillclimber_instance = Hillclimber(self.max, self.region)
        iterations = 20
        quality_threshold = 7500
        hillclimber_instance.random_railmap()
        self.K_values.append(hillclimber_instance.original_quality)
        hillclimber_instance.choose_random_trajectory()

        for iteration in range(iterations):
            hillclimber_instance.change_node_last()
            quality = hillclimber_instance.compare_K_values()
            self.K_values.append(quality)
            
        # Check for the quality threshold and break if met
            if hillclimber_instance.original_quality >= quality_threshold:
                print(f"Quality threshold reached.")
                break

        # set the best railmap to self.trajectories for visualisation
        self.trajectories = hillclimber_instance.trajectories

        # extend the list of all K's and reset highest K
        self.all_K_values.append(self.K_values)
        self.highest_K = 0
    
    def hill_climber(self):
        # reset K's
        self.K_values = 0

        hillclimber_instance = Hillclimber(self.max, self.region)
        hillclimber_instance.run()
        
        # set variables for visualisation
        self.trajectories = hillclimber_instance.trajectories
        self.K_value_output = hillclimber_instance.K_values[-1]
        self.K_values = hillclimber_instance.K_values
        self.all_K_values.append(hillclimber_instance.K_values)

    def beam(self):
        # reset K's
        self.K_values = []
        # let the user know the algorithm is running
        print(f"\nUsing Iterative Deepening algorithm in {self.region}")

        test = IDS(self.max, self.region)
        test.start_trajectory()
        schedule, k = test.continue_trajectory()
    
        for i in range(len(schedule.trajectories)):
            stations1 = []
            for j in range(len(schedule.trajectories[i].stations)):
                if j == 0:
                    stations1.append(schedule.trajectories[i].stations[j].station)
                stations1.append(schedule.trajectories[i].stations[j].connection)
            schedule.trajectories[i].stations = stations1
        
        self.trajectories = schedule.trajectories
        print(k)
        self.K_values.append(k)
        self.all_K_values.append(k)
        
        
        
        #set variables for visualisation

    def pool(self):
        # reset K's
        self.K_values = []

        amount = \
    int(input("\nFor Pool algorithm:\n\
              How many random trajectories do you want to create?\n"))
        
        changes = \
    int(input("\nAnd how many times do you want to recreate the railmap?\n"))
        
        # let the user know the algorithm is running
        print\
        (f"\nUsing Random algorithm in {self.region} {self.iterations} times...")
        
        for i in range(0, self.iterations):
            # initiate the algorithm
            rail = Pool(self.max, self.region, amount)

            # run the algorithm
            for i in range(0, changes):
                rail.change_network()

            self.K_values.append(rail.K)

            if rail.K > self.highest_K:
                self.trajectories = rail.network
                self.highest_K = rail.K
                self.K_value_output = self.highest_K

        # extend the list of all K's and reset highest K
        self.all_K_values.append(self.K_values)
        self.highest_K = 0
    
    def simulated_annealing(self):
        # reset K's
        self.K_values = []

        simulated_annealing_instance = Simulated_annealing(self.max, self.region)
        simulated_annealing_instance.run()

        # for visualisation
        self.K_value_output = simulated_annealing_instance.K_values[-1]
        self.trajectories = simulated_annealing_instance.trajectories
        self.K_values = simulated_annealing_instance.K_values
        self.all_K_values.append(simulated_annealing_instance.K_values)
        

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

    def output(self, algorithm):
        # set column names
        fields = ["train", "stations"]

        # lists to store stations in
        all_stations = []

        # loop through every trajectory and add every station
        for trajectory in self.trajectories:
            stations = []
            for station in trajectory.stations:
                stations.append(station.name)
            all_stations.append(stations)

        rows = []

        for i in range(0, len(all_stations)):
            row = f"train_{i + 1}", "[" + ", ".join(all_stations[i]) + "]"
            rows.append(row)

        filename = "output.csv"

        # writing to csv file
        with open(filename, 'w') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)
        
            # writing the fields
            csvwriter.writerow(fields)
        
            # writing the data rows
            csvwriter.writerows(rows)

            last_row = ["score", f"{self.K_value_output}"]
            # write score
            csvwriter.writerow(last_row)


        
