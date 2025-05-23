from QAPProblem import QAPProblem, QAPPopulationInitializer
from typing import List, Tuple
import random
import numpy as np


class QAPSAPopulationInitializer(QAPPopulationInitializer):
    """
    Population initializer using Simulated Annealing for QAP problems.
    Each individual is generated using SA with different cooling rates.
    """
    
    def __init__(self):
        self.problem = None

    def initialize(self, population_size: int, problem: QAPProblem) -> List[Tuple[List[int], int]]:
        """
        Initialize population using Simulated Annealing with variable cooling rates.
        
        Args:
            population_size: Number of individuals in the population
            problem: QAP problem instance
            
        Returns:
            List of tuples (assignment, cost)
        """
        self.problem = problem
        
        # Range of cooling rates to use for diversity
        cooling_rate_range = (0.90, 0.99)
        population = []

        for _ in range(population_size):
            cooling_rate = random.uniform(*cooling_rate_range)
            assignment, cost = self._simulated_annealing(cooling_rate=cooling_rate)
            population.append((assignment, cost))

        return population

    def _calculate_cost(self, assignment: List[int]) -> int:
        """Calculate the total cost of a QAP assignment."""
        return self.problem.calculate_cost(assignment)

    def _swap_facilities(self, assignment: List[int]) -> List[int]:
        """Generate a neighboring solution by swapping two facility assignments."""
        new_assignment = assignment.copy()
        i, j = random.sample(range(len(assignment)), 2)
        new_assignment[i], new_assignment[j] = new_assignment[j], new_assignment[i]
        return new_assignment

    def _insert_move(self, assignment: List[int]) -> List[int]:
        """Generate a neighboring solution using insert move."""
        new_assignment = assignment.copy()
        i = random.randint(0, len(assignment) - 1)
        j = random.randint(0, len(assignment) - 1)
        
        if i != j:
            # Remove facility at position i and insert at position j
            facility = new_assignment.pop(i)
            new_assignment.insert(j, facility)
        
        return new_assignment

    def _get_neighbor(self, assignment: List[int]) -> List[int]:
        """Get a random neighbor using either swap or insert move."""
        if random.random() < 0.7:  # 70% chance for swap, 30% for insert
            return self._swap_facilities(assignment)
        else:
            return self._insert_move(assignment)

    def _simulated_annealing(self, cooling_rate: float = 0.95, 
                           initial_temperature: float = 1000, 
                           max_iterations: int = 1000) -> Tuple[List[int], int]:
        """
        Perform Simulated Annealing to find a good initial solution.
        
        Args:
            cooling_rate: Rate at which temperature decreases
            initial_temperature: Starting temperature
            max_iterations: Maximum number of iterations
            
        Returns:
            Tuple of (best_assignment, best_cost)
        """

        n = self.problem.n
        
        # Start with random assignment
        current_assignment = list(range(n))
        random.shuffle(current_assignment)
        current_cost = self._calculate_cost(current_assignment)

        # Track best solution found
        best_assignment = current_assignment.copy()
        best_cost = current_cost
        temperature = initial_temperature

        for iteration in range(max_iterations):
            # Generate neighbor
            new_assignment = self._get_neighbor(current_assignment)
            new_cost = self._calculate_cost(new_assignment)

            # Accept or reject the new solution
            if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
                current_assignment = new_assignment
                current_cost = new_cost

                # Update best solution if necessary
                if new_cost < best_cost:
                    best_assignment = new_assignment.copy()
                    best_cost = new_cost

            # Cool down
            temperature *= cooling_rate
            
            # Optional: Early termination if temperature is very low
            if temperature < 1e-8:
                break

        return best_assignment, best_cost
    