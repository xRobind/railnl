# railnl: Delay

## The Problem
We want to develop a program that provides the best possible solution for connecting a number of given train stations through their connections. This program creates a route through (a part of) the Netherlands, consisting of one or more segments. The quality of the route is calculated using a function that yields a K-value, and the goal is to maximize the value of that optimization function. We have developed several algorithms aimed at maximizing this K value. The K value depends on the total travel time, the number of critical connections traversed, and the number of segments used.

## Our Algorithms
- Baseline/Random


For the Random algorithm we started a trajectory on a random stations, and than we started adding random stations to the trajectory. After each connection we added a probability that the trajectory would not continue. If the time was up and the trajectory had not stopped yet, we stopped the trajectory. After the trajectory stopped, we start a new trajectory but we also added a probability that the network is finished after the previous trajectory. 

- Hill Climber


For the hill climber algorithm we first randomly generate a network using the baseline algorithm. We than randomly select a trajectory in the network. After this we generate a new trajectory, and replace the selected trajectory by the new one. We than compare the quality of the old network to the quality of the new network. If the new quality is higher than the old one, we replave the old network by the new one and than we start again from the beginning by choosing a random trajectory. If the quality of the old network is higher we do not replace the old network, and than we start again. 

- Pool
- Simulated Annealing

The simulated annealing algorithm almost works he same as the hill climber algorithm. The only difference is that with the simulated annealing algorithm declines in quality can sometimes still lead te a raplacement of the old network. The probabilty that this happens depends on the number of iterations, the temparature and the old and new quality's. 

- Iterative Deepening
  
The iterative deepening algorithm creates multiple schedules. It then adds a certain number of connections, depending on the depth set in the code. After the depth is reached, the algrotihm takes the best number of schedules, how many depends on the breadth set in the code. This process repeats itself, untill it reaches the goal or cannot go further.

## Usage
When entering "python3 main.py" in the terminal, you will be asked a couple of things like which algorithm you want to use on which region etc. After filling this in, the programme will be run. Csv files with K-values will be saved and plots for visualisation will be shown.

### Autors
Robin Duson
Jet van Ommeren
Thomas Spreen
