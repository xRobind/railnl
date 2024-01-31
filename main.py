from code.main_helpers import Main

if __name__ == "__main__":
    main = Main()
    # retrieve input from user
    main.user_input()

    # execution of all algorithms, with visualisation and csv output file
    if main.algorithm == "baseline":
        main.baseline()
        main.visualisation()
        main.output("baseline")
    
    elif main.algorithm == "hill climber":
        main.hill_climber()
        main.visualisation()
        main.output("hill climber")

    elif main.algorithm == "beam":
        main.beam()
        main.visualisation()
        main.output("beam")

    elif main.algorithm == "pool":
        main.pool()
        main.visualisation()
        main.output("pool")
        
    elif main.algorithm == "simulated annealing":
        main.simulated_annealing()
        main.visualisation(500)
        main.output("simulated annealing")

    elif main.algorithm == "all":
        # all except beam, because that one only yields one K value
        main.baseline()
        main.hill_climber()
        main.pool()
        main.simulated_annealing()
        main.visualisation()
    

    

    

    




