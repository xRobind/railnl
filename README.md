# railnl: Delay

## The Problem
We want to develop a program that provides the best possible solution for connecting a number of given train stations through their connections. This program creates a route through (a part of) the Netherlands, consisting of one or more segments. The quality of the route is calculated using a function that yields a K-value, and the goal is to maximize the value of that optimization function. We have developed several algorithms aimed at maximizing this K value. The K value depends on the total travel time, the number of critical connections traversed, and the number of segments used.

## Our Algorithms
- Baseline/Random
- Hill Climber
- Pool
- Simulated Annealing
- Iterative Deepening
  
The iterative deepening algorithm creates multiple schedules. It then adds a certain number of connections, depending on the depth set in the code. After the depth is reached, the algrotihm takes the best number of schedules, how many depends on the breadth set in the code. This process repeats itself, untill it reaches the goal or cannot go further.

## Usage
When entering "python3 main.py" in the terminal, you will be asked a couple of things like which algorithm you want to use on which region etc. After filling this in, the programme will be run. Csv files with K-values will be saved and plots for visualisation will be shown.

### Autors
Robin Duson
Jet van Ommeren
Thomas Spreen
