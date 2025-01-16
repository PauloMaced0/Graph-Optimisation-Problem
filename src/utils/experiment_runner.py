import networkx as nx
import csv
from graph_gen import generate_random_graph
from src.algorithms.exhaustive_search import exhaustive_search
from src.algorithms.randomized_search import randomized_mwds 
from src.algorithms.greedy_heuristic import greedy_dominating_set

def run_experiments(max_n, densities, seed):
    results = []
    for n in range(4, max_n):
        for density in densities:
            print(f"Running experiments for n={n}, density={density}")
            G, weights, positions = generate_random_graph(n, density, seed)
            # Assign positions and weights as node attributes
            nx.set_node_attributes(G, weights, 'weight')
            # Save the graph using GraphML
            nx.write_graphml(G, f"graphs/graph_n{n}_d{density}.graphml")
            # Run exhaustive search if feasible
            if n <= 23:  # Adjust this limit based on your computational resources
                (exhaustive_set, min_weight, total_configs_tested,
                 exec_time_exhaustive, num_ops_exhaustive) = exhaustive_search(G, weights)
                print(f"Exhaustive min dominating set weight: {min_weight}")
                # visualize_dominating_set(G, exhaustive_set, n, density)
            else:
                min_weight = None
                total_configs_tested = None
                exec_time_exhaustive = None
                num_ops_exhaustive = None
            # Run greedy heuristic
            (greedy_set, greedy_weight, exec_time_greedy,
             num_ops_greedy) = greedy_dominating_set(G, weights)
            # print(f"Greedy min dominating set weight: {greedy_weight}")
            # visualize_dominating_set(G, greedy_set, n, density)

            (randomized_set, randomized_weight, exec_time_random, num_ops_random) = randomized_mwds(G, weights, max_iterations=1000, max_time=5000)
            # print(f"Random min dominating set weight: {randomized_weight}")
            # print(f"Random execution time: {exec_time_random}")
            # visualize_dominating_set(G, randomized_set, n, density)

            # Calculate precision if possible
            if min_weight is not None:
                greedy_precision = greedy_weight / min_weight
                randomized_precision = randomized_weight / min_weight
            else:
                greedy_precision = None
                randomized_precision = None
            # Record the results
            results.append({
                'n': n,
                'density': density,
                'exhaustive_weight': min_weight,
                'exhaustive_time': exec_time_exhaustive,
                'exhaustive_ops': num_ops_exhaustive,
                'exhaustive_configs': total_configs_tested,
                'greedy_weight': greedy_weight,
                'greedy_time': exec_time_greedy,
                'greedy_ops': num_ops_greedy,
                'greedy_precision': greedy_precision,
                'randomized_weight': randomized_weight,
                'randomized_time': exec_time_random,
                'randomized_ops': num_ops_random,
                'randomized_precision': randomized_precision
            })
        # Save results to CSV
        keys = results[0].keys()
        with open('experiment_results.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
    return results
