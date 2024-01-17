from main import RailNL
import matplotlib.pyplot as plt

K_values = []
x = 1000

for i in range(x):
    rail = RailNL(7)
    run = "new trajectory"
    
    while run == "new trajectory" and len(rail.trajectories) < 7:

        trajectory = rail.start_trajectory()
        run = rail.continue_trajectory(trajectory)
        while run == "continue":

            run = rail.continue_trajectory(trajectory)
            
    K = rail.calculate_K()
    K_values.append(K)

plt.hist(K_values, 1000)

plt.show()
