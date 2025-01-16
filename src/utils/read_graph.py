import networkx as nx
import random
import os

from src.algorithms.exhaustive_search import exhaustive_search
from src.algorithms.greedy_heuristic import greedy_dominating_set
from src.algorithms.randomized_search import randomized_mwds

def read_graph(file_path):
    """
    Reads a graph from a file in the specified format and returns:
    - A NetworkX graph object.
    - The number of vertices.
    - The number of edges.
    - A dictionary of edge weights.
    """
    random.seed(102620)

    with open(file_path, 'r') as file:
        lines = file.readlines()
     
    num_vertices = int(lines[2].strip())
    num_edges = int(lines[3].strip())
    
    graph = nx.Graph()
    
    node_weights = {v: random.uniform(0.1, 10.0) for v in range(num_vertices)}  # Default random weights

    for node, weight in node_weights.items():
        graph.add_node(node, weight=weight)

    # Add edges
    for line in lines[4:]:
        if not line.strip():  # Skip empty lines
            continue

        edge_data = line.strip().split()
        u, v = int(edge_data[0]), int(edge_data[1])
        
        if u != v:  # Avoid self-loops
            graph.add_edge(u, v)

    return graph, num_vertices, num_edges, node_weights

def process_graphs(folder_path):
    """
    Processes each graph and applies appropriate algorithms based on graph size.
    """
    results = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt") and file_name != "SWlargeG.txt":
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing {file_name}...")
            
            graph, num_vertices, num_edges, weights = read_graph(file_path)

            results[file_name] = {
                "Vertices": num_vertices,
                "Edges": num_edges
            }

            if "tiny" in file_name.lower():
                _, best_weight, _, execution_time, num_basic_operations = exhaustive_search(graph, weights)
                results[file_name]["Exhaustive"] = {
                    "Best Weight": best_weight,
                    "Execution Time (ms)": execution_time,
                    "Basic Operations": num_basic_operations
                }

            _, best_weight, execution_time, num_basic_operations = greedy_dominating_set(graph, weights)
            results[file_name]["Greedy"] = {
                "Best Weight": best_weight,
                "Execution Time (ms)": execution_time,
                "Basic Operations": num_basic_operations
            }
            
            _, best_weight, execution_time, num_basic_operations = randomized_mwds(graph, weights, max_time=10000)
            results[file_name]["Random"] = {
                "Best Weight": best_weight,
                "Execution Time (ms)": execution_time,
                "Basic Operations": num_basic_operations
            }
    
    return results

if __name__ == "__main__":
    folder_path = "./data"
    results = process_graphs(folder_path)
    
    for file_name, result in results.items():
        print(f"Results for {file_name}:")
        print(f"  Vertices: {result['Vertices']}")
        print(f"  Edges: {result['Edges']}")
        for algo, algo_result in result.items():
            if algo in {"Exhaustive", "Greedy", "Random"}:  # Filter algorithms
                print(f"  {algo}:")
                print(f"    Best Weight: {algo_result['Best Weight']}")
                print(f"    Execution Time (ms): {algo_result['Execution Time (ms)']}")
                print(f"    Basic Operations: {algo_result['Basic Operations']}")
