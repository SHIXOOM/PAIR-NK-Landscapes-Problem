from abc import ABC, abstractmethod
from typing import List, Tuple
import numpy as np

class QAPProblem:
    """
    Represents a Quadratic Assignment Problem instance.
    """
    def __init__(self, distance_matrix: np.ndarray, flow_matrix: np.ndarray, name: str = ""):
        """
        Initialize QAP problem instance.
        
        Args:
            distance_matrix: n x n matrix of distances between locations
            flow_matrix: n x n matrix of flows between facilities
            name: optional problem name
        """
        self.distance_matrix = distance_matrix
        self.flow_matrix = flow_matrix
        self.n = len(distance_matrix)
        self.name = name
        
        # Validate matrices
        if distance_matrix.shape != (self.n, self.n):
            raise ValueError("Distance matrix must be square")
        if flow_matrix.shape != (self.n, self.n):
            raise ValueError("Flow matrix must be square")
        if distance_matrix.shape != flow_matrix.shape:
            raise ValueError("Distance and flow matrices must have same dimensions")
    
    def calculate_cost(self, assignment: List[int]) -> int:
        """
        Calculate the total cost of an assignment.
        
        Args:
            assignment: List where assignment[i] is the location assigned to facility i
                       (0-based indexing)
        
        Returns:
            Total cost of the assignment
        """
        if len(assignment) != self.n:
            raise ValueError(f"Assignment must have length {self.n}")
        
        total_cost = 0
        for i in range(self.n):
            for j in range(self.n):
                total_cost += self.flow_matrix[i][j] * self.distance_matrix[assignment[i]][assignment[j]]
        
        return total_cost


class QAPPopulationInitializer(ABC):
    """
    Abstract class for QAP problem population initialization for Genetic
    Algorithm solutions.
    """

    @abstractmethod
    def initialize(self, population_size: int, problem: QAPProblem) -> List[Tuple[List[int], int]]:
        """
        Initialize a population for the QAP.
        
        Args:
            population_size: Number of individuals in the population
            problem: QAP problem instance
            
        Returns:
            List of tuples where each tuple contains:
            - assignment: List of integers representing facility-to-location assignment (0-based)
            - cost: Total cost of the assignment
        """
        pass