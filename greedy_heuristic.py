import time

def greedy_dominating_set(G, weights):
    start_time = time.time()
    D = set()
    dominated = set()
    nodes = set(G.nodes())
    num_basic_operations = 0
    while dominated != nodes:
        best_vertex = None
        best_value = float('inf')
        for v in nodes - D:
            undominated_neighbors = set(G.neighbors(v)) - dominated
            value = weights[v] / (len(undominated_neighbors) + 1)
            if value < best_value:
                best_value = value
                best_vertex = v
            num_basic_operations += 1  # Counting the for loop iterations 
        D.add(best_vertex)
        dominated.update([best_vertex])
        dominated.update(G.neighbors(best_vertex))
    total_weight = sum(weights[v] for v in D)
    end_time = time.time()
    execution_time = end_time - start_time
    return D, total_weight, execution_time * 1000, num_basic_operations
