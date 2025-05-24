import random

from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.QAPLoader.QAPProblem import QAPProblem


class RandomInitializer(PopulationInitializer):
    def __init__(self):
        self.problem = None

    def initialize(
        self, population_size: int, problem: QAPProblem
    ) -> list[tuple[list, int]]:
        """returns a list of tuples. each tuple contains a 1-based tsp trace and its length"""
        self.problem: QAPProblem = problem

        node_count = problem.n
        population = []
        for i in range(population_size * 6):
            tour: list[int] = [point for point in range(1, node_count + 1)]
            random.shuffle(tour)
            trace_fitness: int = problem.calculate_cost(tour)
            population.append((tour, trace_fitness))

        population.sort(key=lambda x: x[1], reverse=True)
        population = population[-population_size:]      # This is necessairy, it takes the smallest "population_size" solutions.
        return population


# problem = tsplib95.load('/Users/shadyali/Downloads/clu_25_10.tsp')
# ri = RandomInitializer(problem)
# print(ri.initialize(16, problem))
