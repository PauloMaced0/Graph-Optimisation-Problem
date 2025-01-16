import random 
import time

def randomized_mwds(graph, weights, max_iterations=1000, max_time=100):
    start_time = time.time()
    best_solution = set()
    best_weight = float('inf')
    num_basic_operations = 0

    for _ in range(max_iterations):
        if time.time() - start_time > max_time:  # Stop if max_time is exceeded
            break

        # Randomly shuffle vertices
        vertices = list(graph.nodes)
        random.shuffle(vertices)

        # Build a candidate dominating set
        candidate_solution = set()
        dominated = set()
        candidate_weight = 0

        for vertex in vertices:
            if vertex not in dominated:
                # Add vertex to the solution
                candidate_solution.add(vertex)
                candidate_weight += weights[vertex]
                # Mark vertex and its neighbors as dominated
                dominated.add(vertex)
                dominated.update(graph.neighbors(vertex))
            num_basic_operations += 1

        # Update the best solution if the candidate is better
        if candidate_weight < best_weight:
            best_solution = candidate_solution
            best_weight = candidate_weight

    end_time = time.time()
    execution_time = end_time - start_time
    return best_solution, best_weight, execution_time * 1000, num_basic_operations
