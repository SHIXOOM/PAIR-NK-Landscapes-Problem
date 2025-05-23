import QAPSAPopulationInitializer , QAPLibLoader, QAPProblem

if __name__ == "__main__":
    # Run examples
    
    #call and get problem details
    problem , assignment , cost =QAPLibLoader.load_problem_example()
    print("\n" + "="*50 + "\n")

    #Run Simulated Annealing on problem set
    sa = QAPSAPopulationInitializer.QAPSAPopulationInitializer()
    sa.initialize(population_size=4, problem=problem)
    answer = sa._simulated_annealing()
    print(answer)

    """
    # To run a specific example:

    loader = QAPLibLoader.QAPLIBLoader()
    problem , assignment , cost = loader.load_from_url("bur26a")
    print("Initialized assginment: ", assignment)
    print("Initialized cost: ", cost)

    """

    