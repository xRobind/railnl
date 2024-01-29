import copy
from typing import Any

from code.classes.trajectory import Trajectory

class Schedule:

    def __init__(self, trajectories: list[Trajectory], all_connections: Any) -> None:
        self.trajectories = trajectories
        self.connections_used: list = []
        self.all_connections = all_connections
        self.connections_over: list = []
        try:
            for i in range(len(self.all_connections)):
                self.connections_over.append(i + 1)
        except(TypeError):
            pass
        self.score: float = 0
        self.time = 0
        self.T = 0
        self.p: float = 0
        
    def calculate_K2(self) -> float:
        for trajectory in self.trajectories:
            self.time += trajectory.time
            for connection in trajectory.stations:
                if connection.connection_id in self.connections_over:
                    self.connections_used.append(connection.connection_id)
                    self.connections_used.append(connection.corresponding.connection_id)
                    self.connections_over.remove(connection.connection_id)
                    self.connections_over.remove(connection.corresponding.connection_id)
                        
        self.T = len(self.trajectories)
        self.p = len(self.connections_used) / len(self.all_connections)
        self.score = 10000 * self.p - (self.T * 100 + self.time)
        self.time = 0
        self.T = 0
        self.p = 0
        
        return self.score

    def calculate_K_simple(self) -> float:
        connections = []

        for trajectory in self.trajectories:
            self.time += trajectory.time

            for i in range(0, len(trajectory.stations) - 1):
                if (trajectory.stations[i + 1], trajectory.stations[i])\
                not in connections:
                    connections.append((trajectory.stations[i],
                                    trajectory.stations[i + 1]))
        
        connections = set(connections)

        p = len(connections) / self.all_connections
        print("\nberekening K:")
        print("P = ", p)
        print("aantal trajectories:", len(self.trajectories))
        print("tijd:", self.time)

        return p * 10000 - (len(self.trajectories) * 100 + self.time)        

    def add_trajectory(self, trajectory) -> None:
        self.trajectories.append(trajectory)
    
