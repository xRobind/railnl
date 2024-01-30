from main_helpers import Main

if __name__ == "__main__":
    main = Main()
    # retrieve input from user
    main.user_input()

    # execution of baseline algorithm
    if main.algorithm == "baseline":
        # initialise and run baseline algorithm
        main.baseline()
        main.visualisation()
    
    # execution of hill climber algorrithm
    elif main.algorithm == "hill climber":
        #initialise and run hill climber algorithm 
        main.hill_climber()
        main.visualisation()

    elif main.algorithm == "beam":
        #testen
        main.beam()

    elif main.algorithm == "pool":
        main.pool()
        main.visualisation()
        
    elif main.algorithm == "simulated annealing":
        main.simulated_annealing()
        # main.visualisation()

    elif main.algorithm == "all":
        main.baseline()
        main.hill_climber()
        # main.beam()
        main.pool()
        main.visualisation()
    

    

    

    




