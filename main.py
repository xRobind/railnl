from main_helpers import Main

if __name__ == "__main__":
    main = Main()
    # retrieve input from user
    main.user_input()

    # execution of all algorithms, with visualisation and csv outut file
    if main.algorithm == "baseline":
        main.baseline()
        main.visualisation()
        main.output("baseline")
        main.visualisation()
    
    elif main.algorithm == "hill climber":
        main.hill_climber()
        main.visualisation()
        main.output("hill_climber")

    elif main.algorithm == "beam":
        #testen
        main.beam()

    elif main.algorithm == "pool":
        main.pool()
        main.visualisation()
        main.output("pool")
        
    elif main.algorithm == "simulated annealing":
        main.simulated_annealing()
        main.visualisation(500)
        main.output("simulated_annealing")

    elif main.algorithm == "all":
        main.baseline()
        main.hill_climber()
        # main.beam()
        main.pool()
        main.simulated_annealing()
        main.visualisation()
    

    

    

    




