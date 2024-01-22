from code.classes.stations import Station
from code.classes.trajectory import Trajectory

import random
import matplotlib.pyplot as plt

class Hillclimber:
    """ this class......."""

    def __init__(self, max, region) -> None:
        self.baseline_instance = Baseline(max, region)
    

    def random_railmap(self):
        """Generate a random railmap using the Baseline class."""
        # Start with a random trajectory from the baseline
        current_trajectory = self.baseline_instance.start_trajectory()

        # Continue the trajectory until a stopping condition is met
        while True:
            result = self.baseline_instance.continue_trajectory(current_trajectory)

            if result == "stop":
                break
            elif result == "new trajectory":
                current_trajectory = self.baseline_instance.start_trajectory()

        # Calculate the quality of the generated railmap
        quality = self.baseline_instance.calculate_K()
        print(quality)
        return quality
        
    def change_node(self):
        
        