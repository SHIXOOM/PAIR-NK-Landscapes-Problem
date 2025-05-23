import numpy as np
import requests
import io
from typing import Optional, Dict, List
from QAPProblem import QAPProblem

class QAPLIBLoader:
    """
    Loader for QAPLIB problem instances from the online repository.
    """
    
    BASE_URL_DAT = "https://coral.ise.lehigh.edu/wp-content/uploads/2014/07/data.d"
    BASE_URL_SLN = "https://coral.ise.lehigh.edu/wp-content/uploads/2014/07/soln.d"
    
    # Some popular QAPLIB instances
    POPULAR_INSTANCES = {
        'bur26a': 'bur26a.dat',
        'bur26b': 'bur26b.dat',
        'bur26c': 'bur26c.dat',
        'bur26d': 'bur26d.dat',
        'bur26e': 'bur26e.dat',
        'bur26f': 'bur26f.dat',
        'bur26g': 'bur26g.dat',
        'bur26h': 'bur26h.dat',
        'chr12a': 'chr12a.dat',
        'chr12b': 'chr12b.dat',
        'chr12c': 'chr12c.dat',
        'chr15a': 'chr15a.dat',
        'chr15b': 'chr15b.dat',
        'chr15c': 'chr15c.dat',
        'chr18a': 'chr18a.dat',
        'chr18b': 'chr18b.dat',
        'chr20a': 'chr20a.dat',
        'chr20b': 'chr20b.dat',
        'chr20c': 'chr20c.dat',
        'chr22a': 'chr22a.dat',
        'chr22b': 'chr22b.dat',
        'chr25a': 'chr25a.dat',
        'els19': 'els19.dat',
        'esc16a': 'esc16a.dat',
        'esc16b': 'esc16b.dat',
        'esc16c': 'esc16c.dat',
        'esc16d': 'esc16d.dat',
        'esc16e': 'esc16e.dat',
        'esc16f': 'esc16f.dat',
        'esc16g': 'esc16g.dat',
        'esc16h': 'esc16h.dat',
        'esc16i': 'esc16i.dat',
        'esc16j': 'esc16j.dat',
        'had12': 'had12.dat',
        'had14': 'had14.dat',
        'had16': 'had16.dat',
        'had18': 'had18.dat',
        'had20': 'had20.dat',
        'kra30a': 'kra30a.dat',
        'kra30b': 'kra30b.dat',
        'kra32': 'kra32.dat',
        'lipa20a': 'lipa20a.dat',
        'lipa20b': 'lipa20b.dat',
        'lipa30a': 'lipa30a.dat',
        'lipa30b': 'lipa30b.dat',
        'lipa40a': 'lipa40a.dat',
        'lipa40b': 'lipa40b.dat',
        'lipa50a': 'lipa50a.dat',
        'lipa50b': 'lipa50b.dat',
        'lipa60a': 'lipa60a.dat',
        'lipa60b': 'lipa60b.dat',
        'lipa70a': 'lipa70a.dat',
        'lipa70b': 'lipa70b.dat',
        'lipa80a': 'lipa80a.dat',
        'lipa80b': 'lipa80b.dat',
        'lipa90a': 'lipa90a.dat',
        'lipa90b': 'lipa90b.dat',
        'nug12': 'nug12.dat',
        'nug14': 'nug14.dat',
        'nug15': 'nug15.dat',
        'nug16a': 'nug16a.dat',
        'nug16b': 'nug16b.dat',
        'nug17': 'nug17.dat',
        'nug18': 'nug18.dat',
        'nug20': 'nug20.dat',
        'nug21': 'nug21.dat',
        'nug22': 'nug22.dat',
        'nug24': 'nug24.dat',
        'nug25': 'nug25.dat',
        'nug27': 'nug27.dat',
        'nug28': 'nug28.dat',
        'nug30': 'nug30.dat',
        'rou12': 'rou12.dat',
        'rou15': 'rou15.dat',
        'rou20': 'rou20.dat',
        'scr12': 'scr12.dat',
        'scr15': 'scr15.dat',
        'scr20': 'scr20.dat',
        'sko42': 'sko42.dat',
        'sko49': 'sko49.dat',
        'sko56': 'sko56.dat',
        'sko64': 'sko64.dat',
        'sko72': 'sko72.dat',
        'sko81': 'sko81.dat',
        'sko90': 'sko90.dat',
        'sko100a': 'sko100a.dat',
        'sko100b': 'sko100b.dat',
        'sko100c': 'sko100c.dat',
        'sko100d': 'sko100d.dat',
        'sko100e': 'sko100e.dat',
        'sko100f': 'sko100f.dat',
        'tai12a': 'tai12a.dat',
        'tai12b': 'tai12b.dat',
        'tai15a': 'tai15a.dat',
        'tai15b': 'tai15b.dat',
        'tai17a': 'tai17a.dat',
        'tai20a': 'tai20a.dat',
        'tai20b': 'tai20b.dat',
        'tai25a': 'tai25a.dat',
        'tai25b': 'tai25b.dat',
        'tai30a': 'tai30a.dat',
        'tai30b': 'tai30b.dat',
        'tai35a': 'tai35a.dat',
        'tai35b': 'tai35b.dat',
        'tai40a': 'tai40a.dat',
        'tai40b': 'tai40b.dat',
        'tai50a': 'tai50a.dat',
        'tai50b': 'tai50b.dat',
        'tai60a': 'tai60a.dat',
        'tai60b': 'tai60b.dat',
        'tai64c': 'tai64c.dat',
        'tai80a': 'tai80a.dat',
        'tai80b': 'tai80b.dat',
        'tai100a': 'tai100a.dat',
        'tai100b': 'tai100b.dat',
        'tho30': 'tho30.dat',
        'tho40': 'tho40.dat',
        'tho150': 'tho150.dat',
        'wil50': 'wil50.dat',
        'wil100': 'wil100.dat'
    }

    @classmethod
    def load_from_url(cls, problem_name: str) -> QAPProblem:
        """
        Load a QAPLIB problem instance from the online repository.
        
        Args:
            problem_name: Name of the problem (e.g., 'chr12a', 'nug12', etc.)
            
        Returns:
            QAPProblem instance
            
        Raises:
            ValueError: If problem name is not found
            requests.RequestException: If download fails
        """
        if problem_name not in cls.POPULAR_INSTANCES:
            raise ValueError(f"Problem '{problem_name}' not found. Available problems: {list(cls.POPULAR_INSTANCES.keys())}")
        
        filename = cls.POPULAR_INSTANCES[problem_name]
        url = f"{cls.BASE_URL_DAT}/{filename}"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            return cls._parse_qap_data(content, problem_name)
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to download {problem_name}: {e}")
        
    
    @classmethod
    def load_from_file(cls, filepath: str, problem_name: Optional[str] = None) -> QAPProblem:
        """
        Load a QAPLIB problem instance from a local file.
        
        Args:
            filepath: Path to the .dat file
            problem_name: Optional name for the problem
            
        Returns:
            QAPProblem instance
        """
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            
            if problem_name is None:
                problem_name = filepath.split('/')[-1].replace('.dat', '')
            
            return cls._parse_qap_data(content, problem_name)
        except IOError as e:
            raise IOError(f"Failed to read file {filepath}: {e}")

    @classmethod
    def _parse_qap_data(cls, content: str, problem_name: str) -> QAPProblem:
        """
        Parse QAPLIB data format.
        
        QAPLIB format:
        - First line: problem size (n)
        - Next n lines: distance matrix
        - Next n lines: flow matrix
        """
        lines = [line.strip() for line in content.strip().split('\n') if line.strip()]
        
        try:
            # First line contains the problem size
            n = int(lines[0])
            
            # Parse distance matrix (next n lines)
            distance_matrix = []
            for i in range(1, n + 1):
                row = [int(x) for x in lines[i].split()]
                if len(row) != n:
                    raise ValueError(f"Distance matrix row {i} has incorrect length: expected {n}, got {len(row)}")
                distance_matrix.append(row)
            
            # Parse flow matrix (next n lines)
            flow_matrix = []
            for i in range(n + 1, 2 * n + 1):
                row = [int(x) for x in lines[i].split()]
                if len(row) != n:
                    raise ValueError(f"Flow matrix row {i-n} has incorrect length: expected {n}, got {len(row)}")
                flow_matrix.append(row)
            
            # Convert to numpy arrays
            distance_matrix = np.array(distance_matrix)
            flow_matrix = np.array(flow_matrix)
            
            return QAPProblem(distance_matrix, flow_matrix, problem_name)
            
        except (ValueError, IndexError) as e:
            raise ValueError(f"Failed to parse QAPLIB data for {problem_name}: {e}")


    @classmethod
    def get_available_problems(cls) -> List[str]:
        """Get list of available problem names."""
        return list(cls.POPULAR_INSTANCES.keys())

    @classmethod
    def get_small_problems(cls, max_size: int = 25) -> List[str]:
        """Get list of small problems (good for testing)."""
        small_problems = []
        for name in cls.POPULAR_INSTANCES.keys():
            # Extract size from problem name if possible
            size_str = ''.join(filter(str.isdigit, name))
            if size_str and int(size_str) <= max_size:
                small_problems.append(name)
        return small_problems


# Example usage functions
def load_problem_example():
    """Example of how to load and use a QAP problem."""
    # Load a small problem for testing
    loader = QAPLIBLoader()
    
    try:
        # Load chr12a problem (12x12)
        problem = loader.load_from_url('tai60a')
        print(f"Loaded problem: {problem.name}")
        print(f"Problem size: {problem.n}")
        print(f"Distance matrix shape: {problem.distance_matrix.shape}")
        print(f"Flow matrix shape: {problem.flow_matrix.shape}")
        
        # Test with a random assignment
        import random
        random_assignment = list(range(problem.n))
        random.shuffle(random_assignment)
        cost = problem.calculate_cost(random_assignment)
        print(f"Random assignment: {random_assignment}")
        print(f"Cost: {cost}")

        return problem, random_assignment, cost
        
    except Exception as e:
        print(f"Error loading problem: {e}")

"""
def test_initializers_example():
    #Example of how to use the population initializers.
    from src.PopulationInitializers.QAPRandomInitializer import QAPRandomInitializer
    from src.PopulationInitializers.QAPSAPopulationInitializer import QAPSAPopulationInitializer
    
    # Load a problem
    loader = QAPLIBLoader()
    problem = loader.load_from_url('chr12a')
    
    # Test random initializer
    random_init = QAPRandomInitializer()
    population = random_init.initialize(population_size=5, problem=problem)
    print("Random initialization results:")
    for i, (assignment, cost) in enumerate(population):
        print(f"  Individual {i+1}: cost = {cost}")
    
    # Test SA initializer
    sa_init = QAPSAPopulationInitializer()
    population = sa_init.initialize(population_size=5, problem=problem)
    print("\nSimulated Annealing initialization results:")
    for i, (assignment, cost) in enumerate(population):
        print(f"  Individual {i+1}: cost = {cost}")
"""

if __name__ == "__main__":
    # Run examples
    load_problem_example()
    print("\n" + "="*50 + "\n")
    #test_initializers_example()