import itertools
import time

def is_dominating_set(G, D):
    dominated = set(D)
    for v in D:
        dominated.update(G.neighbors(v))
    return dominated == set(G.nodes())

def exhaustive_search(G, weights):
    min_weight = float('inf')
    min_dominating_set = None
    nodes = list(G.nodes())
    total_configs_tested = 0
    start_time = time.time()
    num_basic_operations = 0
    for r in range(1, len(nodes) + 1):
        for subset in itertools.combinations(nodes, r):
            total_configs_tested += 1
            num_basic_operations += 1  # Counting the combination generation as a basic operation
            if is_dominating_set(G, subset):
                num_basic_operations += len(subset)  # Counting checks within is_dominating_set
                weight = sum(weights[v] for v in subset)
                num_basic_operations += len(subset)  # Counting the sum operation
                if weight < min_weight:
                    min_weight = weight
                    min_dominating_set = subset
    end_time = time.time()
    execution_time = end_time - start_time
    return min_dominating_set, min_weight, total_configs_tested, execution_time, num_basic_operations
