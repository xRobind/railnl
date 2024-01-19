from main_functions import Main

if __name__ == "__main__":
    main = Main()
    # retrieve input from user
    main.algorithm_and_region()

    # execution of baseline algorithm
    if main.algorithm == "baseline":
        # initialise and run baseline algorithm
        main.baseline()
        main.visualisation()

    

    

    

    




