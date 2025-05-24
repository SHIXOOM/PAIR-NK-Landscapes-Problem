from abc import ABC, abstractmethod
from src.QAPLoader.QAPProblem import QAPProblem

class PopulationInitializer(ABC):
    """ 
    Abstract class for TSP problem population initialization for Genetic
    alogirthms solutions.
    """

    @abstractmethod
    def initialize(self, population_size: int, problem: QAPProblem) -> list[tuple[list,int]]:
        """ returns a list of tuples. each tuple contains a 1-based tsp trace and its length """
        pass