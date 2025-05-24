import random
import re
from textwrap import dedent


class PromptResponseManager:
    """
    A static class to manage prompt templates and generation
    """

    @staticmethod
    def getSystemPrompt(selfHints: str = "", populationSize: int = 16) -> str:
        # get default crossover and mutation prompt and instructions for them
        crossoverPrompt, crossoverInstruction = (
            PromptResponseManager.getCrossoverPrompt()
        )
        mutationPrompt, mutationInstruction = PromptResponseManager.getMutationPrompt()

        # get the tinder selection prompt
        selectionPrompt = PromptResponseManager.getPAIRSelectionPrompt()

        # get self hints
        selfHints = """
            """
        # Get the system prompt
        prompt = dedent(f"""You are an evolutionary computing expert for the Quadratic Assignment Problem (QAP).
                    You are given:  
                    1.  A distance matrix (distances between locations) and a flow matrix (flows between facilities).  
                    2.  A list of current assignments (permutation of locations for the facilities, each facility (value) is assigned to a location (value's index)) and their calculated costs.  
                    The assignments are arranged in descending order by their costs, where lower values are better.
                    You are tasked to generate new assignments from the given data, that have lower costs.

                    As example, give the following input:  
                    -----START OF EXAMPLE INPUT-----
                    **facilities count:** 8
                    **locations count:** 8
                    **iteration number:** 2
                    **assignments and costs:** <assignment>0,1,2,3,4,5,6,7</assignment>,cost:5200; <assignment>2,6,4,0,5,7,1,3</assignment>,cost:4300;
                    -----END OF EXAMPLE INPUT-----

                    **EC knowledge:** {crossoverPrompt}\n{mutationPrompt}\n
            
                    You should follow the below instruction step-by-step to generate new assignments from given matrices and assignments. 
                    {selfHints}
                    Ensure you preserve selected crossover operator in Step 2, selected mutation operator in Step 3, and the assignments at each step, repeat Step 1, 2, 3 for a given iteration number.
                    1. {selectionPrompt} Save the two chosen assignments, bracketed them with <sel> and </sel>.
                    2. {crossoverInstruction} the two assignments got in Step 1 and generate a new assignment that is different from all assignments, and has a cost lower than any of these two assignments. 
                    The generated assignment should assign each facility to exactly one location and each location to exactly one facility. Save the selected crossover operator and bracketed it with <c> and </c>. Save the generated assignment and bracketed it with <cross> and </cross>.
                    3. {mutationInstruction} the assignment generated in Step 2 and generate a new assignment that is different from all assignments, and has a lower cost.
                    The assignment should assign each facility to exactly one location and each location to exactly one facility. Save the selected mutation operator and bracketed it with <m> and </m>. Save the generated assignment and bracketed it with <assignment> and </assignment>.
                    
                    Directly give me all the saved selected crossover operator from Step 2, the mutation operator from Step 3, and the assignments from each Step without any explanations.
                    The output format should be similar with below, and the output should contain {populationSize} iterations:
                    Iteration 1:
                    Step 1: <sel>0,1,2,3,4,5,6,7</sel>, <sel>2,6,4,0,5,7,1,3</sel>
                    Step 2: <c>PMX (Partially Mapped Crossover)</c><cross>2,6,7,3,4,5,1,0</cross>
                    Step 3: <m>Swap Mutation</m><assignment>2,6,5,3,4,7,1,0</assignment>
                    Iteration 2:
                    Step 1: <sel>2,6,4,0,5,7,1,3</sel>, <sel>0,1,2,3,4,5,6,7</sel>
                    Step 2: <c>OX (Ordered Crossover)</c><cross>2,6,0,3,4,5,7,1</cross>
                    Step 3: <m>Inversion Mutation</m><assignment>2,6,5,4,3,0,7,1</assignment>""")
        return prompt

    @staticmethod
    def getNewGenerationPrompt(
        population: list[tuple[list, int]], problemSize: int, populationSize: int
    ) -> str:
        prompt = dedent(f"""**facilities count:** {problemSize}
            **locations count:** {problemSize}
            **iteration number:** {populationSize}
            **assignments and costs:** {PromptResponseManager.structureAssignmentsAndCosts(population)}
            """)
        return prompt

    # endregion public methods

    @staticmethod
    def structureAssignmentsAndCosts(population: list[tuple[list, int]]) -> str:
        # make Assignments and Costs into a string format for the llm prompt
        # <assignment>0,1,2,3,4,5,6,7</assignment>,cost:4300; <assignment>2,6,4,0,5,7,1,3</assignment>,cost:5200;....
        assignments = ""
        for assignment, cost in population:
            assignments += f"<assignment>{','.join(str(facility) for facility in assignment)}</assignment>,cost:{cost};"

        return assignments

    @staticmethod
    def getPAIRSelectionPrompt() -> str:
        prompt = dedent("""Act as an assignment of one of the available assignments.
        You are in a dating app, and you want to match with the most suitable assignment from the dating pool for crossover, with the goal of producing an offspring with a cost lower than you and your partner.
        You have the following standards to pick your partner on, but you can define your own set of standards to look for in other assignments:

        A. **Genetic Diversity:**
        - **Complementary Traits:** Identify individual whose genetic makeup introduces beneficial variations when combined with yours, enhancing the offspring's potential to explore new solution spaces.

        B. **Fitness Level:**
        - **High Performance:** Prioritize individuals demonstrating less costs, indicating effective solutions to the Traveling Salesman Problem, to increase the likelihood of producing a high-quality offspring.

        C. **Crossover Compatibility:**
        - **Effective Combination:** Assess the compatibility of your genetic representation with potential partners to ensure that the chosen crossover operator can effectively merge the genomes, maintaining valid QAP solutions.
        Any selected assignments in a previous iterations should not be selected again.
        You can select an offspring from the previous iterations for crossover in the next iterations.""")
        return prompt

    @staticmethod
    def getCrossoverPrompt() -> tuple[str, str]:
        crossoverOperatorsExplanation = dedent("""There are 2 different crossover operators you can use:
                1. **PMX (Partially Mapped Crossover):**
                    - **Description:** PMX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions of the offspring by mapping elements from parent 2.
                    Below is an example.
                        - **Parent 1:** 1 2 3 4 5 6 7 8
                        - **Parent 2:** 3 7 5 1 6 8 2 4
                        - **Randomly select a segment from parent 1 (e.g., positions 4 to 6):** 4 5 6
                        - **Copy the segment from Parent 1 to offspring solution:** _ _ _ 4 5 6 _ _ 
                        - **Fill in the remaining positions by mapping elements from parent 2 (note elements cannot be repeated) to the offspring:** 3 7 8 4 5 6 2 1
                2. **OX (Ordered Crossover):**
                    - **Description:** OX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions with the missing elements in the order in which they appear in parent 2.
                    Below is an example.
                        - **Parent 1:** 1 2 3 4 5 6 7 8
                        - **Parent 2:** 3 7 5 1 6 8 2 4
                        - **Randomly select a segment from parent 1 (e.g., positions 4 to 6):** 4 5 6
                        - **Copy the segment from Parent 1 to the offspring:** _ _ _ 4 5 6 _ _ 
                        - **The missing elements in the order in which they appear in parent 2 are {3, 7, 1, 8, 2}**
                        - **Fill in the remaining positions of the offspring based on the above sorted elements:** 3 7 1 4 5 6 8 2""")

        crossoverOperatorsInstruction = "Select one of the crossover operators based on above EC knowledge , use the selected crossover operator to crossover"

        return crossoverOperatorsExplanation, crossoverOperatorsInstruction

    @staticmethod
    def getMutationPrompt() -> tuple[str, str]:
        mutationOperatorsExplanation = dedent("""There are 3 different mutation operators you can use:
                1. **Swap Mutation:**
                    - **Description:** swap mutation randomly selects two positions in an individual and swaps the elements at those two positions.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select two positions, e.g., position 3 and posision 6:** 3 6
                        - **Swap the elements 8 and 7 at position 3 and position 6:** 5 2 7 4 1 8 6 3
                2. **Insert Mutation:**
                    - **Description:** insert mutation randomly selects one position in the individual and moves the element at that position to another randomly chosen position.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select one position**, e.g., position 3: 3
                        - **Move the element 8 at position 3 to another randomly chosen position 6:** 5 2 4 1 7 8 6 3
                3. **Inversion Mutation:**
                    - **Description:** inversion mutation randomly selects two positions in an individual and inverts the order of the elements between those positions.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select two positions, e.g., position 3 and posision 6:** 3 6
                        - **inverts the order of the elements between position 3 and position 6:** 5 2 7 1 4 8 6 3""")

        mutationOperatorsInstruction = "Select one of the Mutation operators based on above EC knowledge, use the selected crossover operator to mutate"

        return mutationOperatorsExplanation, mutationOperatorsInstruction

    @staticmethod
    def parseNewGeneration(response: str, nodeCount: int) -> list[list[int]]:
        """Find all traces in the response -> list of lists,
        Each list is a trace, each element is an integer, which is a point

        Example output:
        [[0, 1, 2, 3, 4, 5, 6, 7],
        [2, 6, 4, 0, 5, 7, 1, 3],
        [2, 6, 5, 3, 4, 7, 1, 0],
        [2, 6, 5, 4, 3, 0, 7, 1]]
        """

        # Find all traces in the response -> list of strings, each string is a trace
        assignments_strings = re.findall(r"<trace>(.*?)</trace>", response)
        # Convert each trace string into a list of integers -> each integer is a point
        assignments = [
            list(map(lambda pointChar: int(pointChar), assignment_string.split(",")))
            for assignment_string in assignments_strings
        ]

        # Validate the traces
        valid_assignments = []
        for assignment in assignments:
            if PromptResponseManager.validateAssignment(assignment, nodeCount):
                valid_assignments.append(assignment)
            else:
                valid_assignments.append(
                    PromptResponseManager.fixAssignment(assignment, nodeCount)
                )

        return valid_assignments

    @staticmethod
    def parseSelectedTraces(response: str) -> list[list[str]]:
        """Find all assignment pairs selected for mating -> list of lists
        Each list is an assignment pair


        Example output:
        [['5,2,6,4,3,7,1,8,9,0', '4,3,1,9,0,7,6,8,5,2'],
        ['5,2,6,4,3,7,1,8,9,0', '9,0,5,8,7,3,6,4,2,1'],
        ['5,2,6,4,3,7,1,8,9,0', '9,0,2,5,8,4,6,3,1,7']]
        """

        # Find all assignments selected for mating -> list of strings, each string is an assignment
        selected_assignments = re.findall(r"<sel>(.*?)</sel>", response)
        # Pair each two assignments together (pairwise assignments are the ones who mated in each iteration) -> list of lists, each list is a pair of assignments
        pair_assignments = [
            list([selected_assignments[i], selected_assignments[i + 1]])
            for i in range(0, len(selected_assignments), 2)
        ]
        return pair_assignments

    @staticmethod
    def parseCrossoverMethods(response: str) -> list[tuple[str, str]]:
        """Find all crossover methods and the assignment resulted from the crossover -> list of tuples
        Each tuple is a crossover method and the assignment resulted from the crossover

        Example output:
        [('PMX (Partially Mapped Crossover)','4,3,6,8,9,7,1,5,2,0'),
        ('OX (Ordered Crossover)', '5,2,6,4,3,7,8,9,0,1'),
        ('PMX (Partially Mapped Crossover)', '9,0,6,4,3,7,1,8,5,2')]"""

        # Find all crossover methods and the assignment resulted from the crossover -> list of tuples
        selectedCrossoversAndAssignmentResulted = re.findall(
            r"<c>(.*?)</c><cross>(.*?)</cross>", response
        )
        return selectedCrossoversAndAssignmentResulted

    @staticmethod
    def parseMutationMethods(response: str) -> set[tuple[str, int]]:
        """Find all mutation methods used in the iteration and the count of uses of each mutation method -> set of tuples
        Each tuple is a mutation method and the count of usages in the iteration
        Example output:
        {('Insert Mutation', 5),
        ('Inversion Mutation', 5),
        ('Swap Mutation', 6)}"""

        # Find all mutation methods used in the iteration -> list of strings, each string is a mutation method
        selectedMutations = re.findall(r"<m>(.*?)</m>", response)
        # Pair each mutation method with its count of usages -> set of tuples
        selectedMutationsAndCounts = set(
            (selectedMutation, selectedMutations.count(selectedMutation))
            for selectedMutation in selectedMutations
        )
        return selectedMutationsAndCounts

    @staticmethod
    def parseThoughts(response: str) -> list[str]:
        thoughts = re.findall(r"<thought>(.*?)</thought>", response)
        return thoughts

    @staticmethod
    def validateAssignment(assignment: list[int], problemSize: int) -> bool:
        return (
            (len(assignment) == problemSize)
            and (len(set(assignment)) == problemSize)
            and all(facility in range(problemSize) for facility in assignment)
        )

    @staticmethod
    def fixAssignment(assignment: list[int], problemSize: int) -> list[int]:
        # remove the facilities that are not in the range of 0 to problemSize-1
        assignment = [
            facility for facility in assignment if facility in range(problemSize)
        ]
        # get the facilities in the assignment
        setAssignment = set(assignment)
        # get the facilities that are not in the assignment
        unavailableFacilities = [
            facility for facility in range(problemSize) if facility not in setAssignment
        ]
        # shuffle the unavailable facilities
        random.shuffle(unavailableFacilities)
        # add the shuffled unavailable facilities to the assignment
        assignment.extend(unavailableFacilities)
        return assignment
