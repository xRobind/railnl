import copy

from code.classes.stations import Station
from code.classes.trajectory import Trajectory
from code.classes.stack import Stack
from code.classes.connection import Connection
from code.classes.schedule import Schedule


class IDS:

    def __init__(self, max, region) -> None:
        """initialise lists that contain stations as objects of the class,
        connections as a dict that links the connection to the time,
        and trajectories made and time spent
        """
        
        ##initialise empty lists, dicts and stacks 
        self.stations = []
        self.connections = []
        self.connection_dict = {}
        self.stack = Stack()
        self.stack2 = Stack()
        self.list_all = []
        
        ##set parameters
        self.depth = 3
        self.breadth = 3
        self.connection_breadth = 3
        
        ##set maximum time and goal depending on case
        if region == "Holland":
            self.time = 120
            self.goal = 8800
        else:
            self.time = 180
            self.goal = 6300

        # load station structures and connections 
        self.load_stations(f"data/Stations{region}.txt")
        self.load_connections(f"data/Connecties{region}.txt")
        
        self.total_connections = len(self.connections)
        
        #set maximum of trajectories
        self.max_trajectories = max


    def load_stations(self, filename):
        """open file, read the lines and split into the three parts
        """
        with open(filename) as f:
            # skip first line
            next(f)
            line = f.readline()
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",", 2)

                # set the different parts of the line to its variable
                name = parts[0]
                try:
                    y = parts[1]
                except(IndexError):
                    break
                x = parts[2].strip("\n")

                # create the station, add station to self.stations
                station = Station(name, y, x)
                self.stations.append(station)

                # read new line
                line = f.readline()
                   

    def load_connections(self, filename):
        """open file, read the lines and split into the three parts
        """
        connection_id = 1
        with open(filename) as f:
        
            # skip first line
            next(f)
            line = f.readline()
            
            while line != "\n":
                # remove newline character and split into different parts
                parts = line.split(",", 2)

                # set the different parts of the line to its variable
                name = parts[0]
                try:
                    connection = parts[1]
                except(IndexError):
                    break
                if "Holland" in filename:
                    time = int(parts[2].strip("\n"))
                else:
                    time = float(parts[2].strip("\n"))

                
                for station in self.stations:
                    if name == station.name:
                        for station2 in self.stations:
                            if station2.name == connection:
                                # make connection
                                connection_object = Connection(station, station2, time, connection_id)
                                #add connection to station object
                                station.add_connection(connection_object)
                                
                                #add connection to dict and list to store
                                self.connections.append(connection_object)
                                self.connection_dict[connection_id] = connection_object
                                
                                #increase connection_id for new connection
                                connection_id += 1
                                
                                #make corresponding connection
                                connection_object2 = Connection(station2, station, time, connection_id)
                                #add connection to station object
                                station2.add_connection(connection_object2)
                                
                                #add connection to dict and list to store
                                self.connections.append(connection_object2)
                                self.connection_dict[connection_id] = connection_object2
                                #increase connection_id for new connection
                                connection_id += 1
                                
                                #add corresponding connection to connection object
                                connection_object.add_corresponding_connection(connection_object2)
                                connection_object2.add_corresponding_connection(connection_object)
                

                # read new line
                line = f.readline()
        
        ##add number of connections to all station objects
        for station in self.stations:
            station.nmbr()    


    def start_trajectory(self):
        """initialize a trajectory with a starting station and amount of stops
        that it will make
        """
        
        # pick every starting trajectory once
        for connection in self.connections:
                current_trajectory = Trajectory(connection)
                current_trajectory.add_first_time()
                
                for second_connection in current_trajectory.stations[-1].connection.connections:
                    #copy current schedule and make all possible new connections
                    trajectory_copy = copy.deepcopy(current_trajectory)
                    trajectory_copy.add_connection_and_time(second_connection, self.time)
                    
                    #make a list of the first trajectorie to add to a schedule
                    trajectory_copy = [trajectory_copy]
                    
                    ## add trajectory to schedule and put in the stack
                    self.stack.push(Schedule(trajectory_copy, self.connection_dict))


    def continue_trajectory(self):
        nr_connections_added = 0
        while(True):
            ##if no schedules left, return the best one present
            try:
                current_schedule = self.stack.pop()
            except AssertionError:         
                return self.list_all[-1], self.list_all[-1].calculate_K2()
                
            ##look at possible next connection    
            for next_connection in current_schedule.trajectories[-1].stations[-1].connection.connections:
                if current_schedule.trajectories[-1].stations[-1].corresponding.connection_id != next_connection.connection_id: 
                    new = copy.deepcopy(current_schedule)
                    
                    ##add connection if possible
                    if new.trajectories[-1].add_connection_and_time(next_connection, self.time):
                        ## save schedule if depth is reached
                        if len(new.trajectories[-1].stations) == self.depth:
                            nr_connections_added += 1
                            new.calculate_K2()
                            self.list_all.append(new)
                        ##if depth not reached, put in stack to work out further
                        else:
                            self.stack.push(new)

                        
                    ##check if stack is empty
                    if len(self.stack.items) == 1:
                        self.best_schedules()
                        
                        ##make new trajectories when no connections can be added
                        if nr_connections_added == 0:
                            self.make_trajectories()

                        ##reset the number of connections added and increase depth
                        nr_connections_added = 0
                        self.depth += 2


    def best_schedules(self):
        ##sort all schedules on score
        self.list_all.sort(key=lambda x: x.score)
                        
        ##if best schedule reached goal, return best schedule
        new = self.list_all[-1]
        if(new.calculate_K2() > self.goal):
            return new, new.calculate_K2()

        ##work further with best schedules
        for i in range(self.breadth, 1, -1):
            self.stack.push(self.list_all[-i])

 
    def make_trajectories(self):
        self.list_all = []
                            
        while len(self.stack.items) > 1:
            current_schedule2 = self.stack.pop()
                                
            ##if maximum number of trajectories reached, return best schedule
            if(self.max_trajectories == len(current_schedule2.trajectories)):
                return self.list_all[-1], self.list_all[-1].calculate_K2()
                                
            ##sort connections over on number of connections the starting station has
            current_schedule2.connections_over.sort(key = lambda x: self.connection_dict[x].station.nmbr_connections)
                                
            for connection_id in current_schedule2.connections_over[:self.connection_breadth]:
                trajectory = Trajectory(self.connection_dict[connection_id])
                trajectory.add_first_time()
                copy_current_schedule2 = copy.deepcopy(current_schedule2)
                                    
                ##add trajectorie to schedule and put in list with all schedules
                copy_current_schedule2.add_trajectory(trajectory)
                copy_current_schedule2.calculate_K2()
                self.list_all.append(copy_current_schedule2)
                                    
            del current_schedule2

        ##sort schedules on score and go on with best schedules
        self.list_all.sort(key=lambda x: x.score)
        for i in range(self.breadth, 1, -1):
            self.stack.push(self.list_all[-i]) 
                                
        ##reset the depth
        self.depth = 0