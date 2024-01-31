# this file contains functions that retrieves input from a user,
# and handles our different algorithms
import csv
import time
import copy

from code.algorithms.baseline import Baseline
from code.algorithms.hill_climber import Hillclimber
from code.algorithms.iterativedeepening import IDS
from code.algorithms.pool import Pool
from code.algorithms.simulated_annealing import Simulated_annealing

from code.visual.visual import Visualisation


class Main:

    def __init__(self) -> None:
        """Initiates a list to save all K's, a variable to save the highest K,
        variables to set how the experiment will be done, and a list 
        to store the trajectories made.
        """
        self.K_values = []
        self.all_K_values = []
        self.highest_K = 0
        self.iterations = 1000
        self.trajectories = None
        self.K_value_output = 0
        self.runtime = 0

    def user_input(self):
        """This method asks the user to fill in the algorithm, region,
        and the max trajectories to be used in a railmap
        """
        # retrieve existing algorithm
        self.algorithm = input("\nWhich algorithm?\n")

        # choose between all our algorithms
        while self.algorithm not in \
["baseline", "hill climber", "beam", "pool", "simulated annealing", "all"]:
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

        # Holland or Nederland
        while self.region != "Holland" and self.region != "Nederland":
            self.region = \
        input("\nChoose a region: Holland or Nederland (case-sensitive).\n")

        # get max trajectories
        self.max = int(input("\nWhat is the maximum of trajectories?\n"))

        if self.algorithm != "beam":
            self.runtime =\
                    int(input("\nFor how many seconds do you want to run?\n"))

        # must be between 1 and 7
        while self.max < 1 or self.max > 45:
            self.max = \
    int(input("\nMaximum number of trajectories must be between 1 and 45.\n"))

    def baseline(self):
        """This method carries out the baseline algorithm
        """
        # reset K's
        self.K_values = []
        # let the user know the algorithm is running
        print(f"\nUsing Baseline algorithm in {self.region} \
for {self.runtime} seconds...")
        
        # initialise baseline algorithm
        rail = Baseline(self.max, self.region)

        # use time to run the algorithm for a given time
        start = time.time()
        n_runs = 0

        # # csv file to store K's
        # filename = f"baseline_K_{self.runtime}s_{self.region}.csv"
        # # writing to csv file
        # with open(filename, 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)
        
        #     # write the field
        #     csvwriter.writerow(["K values"])

        while time.time() - start < self.runtime:
            n_runs += 1

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

                    # # write K to the data row
                    # with open(filename, 'a') as csvfile:
                    #     csvwriter = csv.writer(csvfile)
                    #     csvwriter.writerow([int(K_value)])

                    # save the rail with highest K
                    if self.highest_K < K_value:
                        self.highest_K = K_value
                        self.trajectories = rail.trajectories
                        self.K_value_output = self.highest_K

                    # stop if a stopping condition is met
                    if run == "stop":
                        break

        # add to the list of all K's and reset highest K
        self.all_K_values.append(self.K_values)
        self.highest_K = 0
    
    def hill_climber(self):
        """This method carries out the hill climber algorithm."""
        
        # reset K's
        self.K_values = []
        # let the user know the algorithm is running
        print(f"\nUsing Hill climber algorithm in {self.region} \
for {self.runtime} seconds..")
        
        # use time to run the algorithm for a given time
        start = time.time()
        n_runs = 0

        # # csv file to store K's
        # filename = f"hillclimber_K_{self.runtime}s_{self.region}.csv"
        # # writing to csv file
        # with open(filename, 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)
        #     # write the field
        #     csvwriter.writerow(["K values"])

        while time.time() - start < self.runtime:
            n_runs += 1

            # run the hill climber algorithm and add the found K
            hillclimber_instance = Hillclimber(self.max, self.region)
            hillclimber_instance.run(self.iterations)
            self.K_values.append(hillclimber_instance.original_quality)

            # # write K to the data row
            # with open(filename, 'a') as csvfile:
            #     csvwriter = csv.writer(csvfile)
            #     csvwriter.writerow([hillclimber_instance.original_quality])
    
        # add to the list of all K values
        self.all_K_values.append(self.K_values)
        
        # set variables for visualisation
        self.K_value_output = hillclimber_instance.original_quality
        self.trajectories = hillclimber_instance.original_trajectories


    def beam(self):
        """This mathod carries out the iterative deepening algorithm."""
        # reset K's
        self.K_values = []
        # let the user know the algorithm is running
        print(f"\nUsing Iterative Deepening algorithm in {self.region}..")

        # initialise and run algorithm
        test = IDS(self.max, self.region)
        test.start_trajectory()
        schedule, k = test.continue_trajectory()

        # apart from running, keep track of trajectories for visualisation
        for i in range(len(schedule.trajectories)):
            stations1 = []
            for j in range(len(schedule.trajectories[i].stations)):
                if j == 0:
                    stations1.append\
                        (schedule.trajectories[i].stations[j].station)
                stations1.append\
                    (schedule.trajectories[i].stations[j].connection)
            schedule.trajectories[i].stations = stations1
        
        # for visualisation
        self.trajectories = schedule.trajectories
        print(k)
        self.K_values.append(k)
        self.all_K_values.append(k)

    def pool(self):
        """This method carries out the pool algorithm."""
        # reset K's
        self.K_values = []

        amount = \
    int(input("\nFor Pool algorithm:\n\
              How many random trajectories do you want to create?\n"))
        
        changes = \
    int(input("\nAnd how many times do you want to recreate the railmap?\n"))
        
        # let the user know the algorithm is running
        print\
    (f"\nUsing Pool algorithm in {self.region} for {self.runtime} seconds..")

        # use time to run the algorithm for a given time
        start = time.time()
        n_runs = 0

        # # csv file to store K's
        # filename = f"pool_K_{self.runtime}s_{self.region}.csv"
        # # writing to csv file
        # with open(filename, 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)
        
        #     # write the field
        #     csvwriter.writerow(["K values"])

        while time.time() - start < self.runtime:
            n_runs += 1

            for i in range(0, self.iterations):
                # initiate the algorithm
                rail = Pool(self.max, self.region, amount)

                # run the algorithm
                for i in range(0, changes):
                    rail.change_network()

                self.K_values.append(rail.K)

                # # write K to the data row
                # with open(filename, 'a') as csvfile:
                #     csvwriter = csv.writer(csvfile)
                #     csvwriter.writerow([rail.K])

        # for checking K calculation
        self.trajectories = rail.network
        self.K_value_output = rail.K

        # extend the list of all K's and reset highest K
        self.all_K_values.append(self.K_values)
        self.highest_K = 0
    
    def simulated_annealing(self):
        """This method carries out the simulated annealing algorithm."""
        # reset K's
        self.K_values = []

        # let the user know the algorithm is running
        print(f"\nUsing Simulated annealing algorithm in {self.region} \
for {self.runtime} seconds..")

        # use time to run the algorithm for a given time
        start = time.time()
        n_runs = 0

        # # csv file to store K's
        # filename = f"SimAn_K_{self.runtime}s_{self.region}.csv"
        # # writing to csv file
        # with open(filename, 'w') as csvfile:
        #     # creating a csv writer object
        #     csvwriter = csv.writer(csvfile)

        #     # write the field
        #     csvwriter.writerow(["K values"])

        while time.time() - start < self.runtime:
            n_runs += 1

            # initiate and run the algorithm
            simulated_annealing_instance =\
                Simulated_annealing(self.max, self.region)
            simulated_annealing_instance.run()
            self.K_values.append\
                (simulated_annealing_instance.original_quality)

            # # write K to the data row
            # with open(filename, 'a') as csvfile:
            #     csvwriter = csv.writer(csvfile)
            #     csvwriter.writerow\
            # ([simulated_annealing_instance.original_quality])

        # for visualisation and checking K calculation
        self.K_value_output = simulated_annealing_instance.K_values[-1]
        self.trajectories = simulated_annealing_instance.original_trajectories
        self.all_K_values.append(simulated_annealing_instance.K_values)

    def visualisation(self, t=None):
        """This method carries out the visualisation.
        """
        assert self.trajectories is not None,\
            "\n\nYou need to set the trajectories made to self.trajectories.\
            Check the end of baseline method in class Main for example.\n"
        # plot rails of best_rail
        v = Visualisation(self.region, self.trajectories)

        # stop visualising when we only want boxplots
        # if v.boxplot(self.all_K_values) == True:
        #     return
        
        v.load_stations()
        v.load_sizes()
        v.get_connections()

        # plot map of the best lijnvoering
        v.draw()
        # plot histogram of all K's from a single algorithm
        # v.histogram(self.K_values, self.iterations)
        # plot all K's next to eachother from all algorithms
        # v.boxplot(self.all_K_values, t=None)

        return

    def output(self, algorithm):
        """This method is used to check if the K's are calculated correctly,
        by using check50 on the output file.
        """
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
            


        
