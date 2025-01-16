import matplotlib.pyplot as plt
import csv
import networkx as nx
import itertools
from graph_gen import generate_random_graph
from src.algorithms.greedy_heuristic import greedy_dominating_set

def visualize_initial_graph(G, n, density):
    plt.figure(figsize=(8, 6))
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw_networkx(G, pos, with_labels=True)
    plt.title(f'Initial Graph (n={n}, density={density})')
    plt.show()

def visualize_dominating_set(G, dominating_set, n, density):
    plt.figure(figsize=(12, 8))
    x_coords = nx.get_node_attributes(G, 'x')
    y_coords = nx.get_node_attributes(G, 'y')
    # Create position dictionary
    pos = {node: (x_coords[node], y_coords[node]) for node in G.nodes()}
    # Define node colors
    node_colors = [] 
    for node in G.nodes():
        if node in dominating_set:
            node_colors.append('red')  # Dominating set nodes in red
        else:
            node_colors.append('green')  # Other nodes in light blue
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1200)
    nx.draw_networkx_edges(G, pos)

    node_labels = {node: f"{G.nodes[node]['weight']:.2f}" for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=node_labels)

    plt.title(f'Minimum Weight Dominating Set Red Highlighted (n={n}, density={density})')
    plt.show()

def visualize_specific_graph(n, density, seed):
    # Generate the graph
    G, weights, positions = generate_random_graph(n, density, seed)
    nx.set_node_attributes(G, weights, 'weight')
    nx.set_node_attributes(G, positions, 'pos')
    
    # Visualize the initial graph
    visualize_initial_graph(G, n, density)
    
    # Run greedy heuristic
    (greedy_set, _, _, _) = greedy_dominating_set(G, weights)
    
    # Visualize the graph with the dominating set
    visualize_dominating_set(G, greedy_set, n, density)

def visualize_graph(n, density):
    G = nx.read_graphml(f"graphs/graph_n{n}_d{density}.graphml")
    # Convert node labels to integers starting from 0
    G = nx.convert_node_labels_to_integers(G, label_attribute='old_label')
    # Access positions and weights
    x_coords = nx.get_node_attributes(G, 'x')
    y_coords = nx.get_node_attributes(G, 'y')
    weights = nx.get_node_attributes(G, 'weight')
    # Create position dictionary
    pos = {node: (x_coords[node], y_coords[node]) for node in G.nodes()}
    # Visualize the graph
    nx.draw(G, pos, with_labels=True, node_size=[weights[v]*100 for v in G.nodes()])
    plt.show()

def visualize_results():
    results = []
    with open('experiment_results.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Convert string values to appropriate types
            row['n'] = int(row['n'])
            row['density'] = float(row['density'])
            row['exhaustive_weight'] = float(row['exhaustive_weight']) if row['exhaustive_weight'] != '' else None
            row['exhaustive_time'] = float(row['exhaustive_time']) if row['exhaustive_time'] != '' else None
            row['exhaustive_ops'] = int(row['exhaustive_ops']) if row['exhaustive_ops'] != '' else None
            row['exhaustive_configs'] = int(row['exhaustive_configs']) if row['exhaustive_configs'] != '' else None
            row['greedy_weight'] = float(row['greedy_weight'])
            row['greedy_time'] = float(row['greedy_time'])
            row['greedy_ops'] = int(row['greedy_ops'])
            row['greedy_precision'] = float(row['greedy_precision']) if row['greedy_precision'] != '' else None
            row['randomized_weight'] = float(row['randomized_weight']) if row['randomized_weight'] != '' else None
            row['randomized_time'] = float(row['randomized_time']) if row['randomized_time'] != '' else None
            row['randomized_ops'] = int(row['randomized_ops']) if row['randomized_ops'] != '' else None
            row['randomized_precision'] = float(row['randomized_precision']) if row['randomized_precision'] != '' else None
            results.append(row)

    densities = sorted(set([r['density'] for r in results]))
    markers = itertools.cycle(('o', 'x', '^', 's', 'D', '*'))
    colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y'))

    # Plot execution time for Greedy Heuristic
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density]
        ns = [r['n'] for r in density_results]
        greedy_times = [r['greedy_time'] for r in density_results]
        plt.plot(ns, greedy_times, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Greedy Heuristic Execution Time vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/execution_time_greedy_all_densities.png')
    plt.show()

    # Reset markers and colors for the next plot
    markers = itertools.cycle(('o', 'x', '^', 's', 'D', '*'))
    colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y'))

    # Plot execution time for Exhaustive Search
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density]
        ns = [r['n'] for r in density_results]
        exhaustive_times = [r['exhaustive_time'] for r in density_results]
        plt.plot(ns, exhaustive_times, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Exhaustive Search Execution Time vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/execution_time_exhaustive_all_densities.png')
    plt.show()

    # Reset markers and colors again
    markers = itertools.cycle(('o', 'x', '^', 's', 'D', '*'))
    colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y'))

    # Plot number of basic operations for Greedy Heuristic
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density]
        ns = [r['n'] for r in density_results]
        greedy_ops = [r['greedy_ops'] for r in density_results]
        plt.plot(ns, greedy_ops, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Number of Basic Operations')
    plt.title('Greedy Heuristic Basic Operations vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/basic_ops_greedy_all_densities.png')
    plt.show()

    # Reset markers and colors
    markers = itertools.cycle(('o', 'x', '^', 's', 'D', '*'))
    colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y'))

    # Plot number of basic operations for Exhaustive Search
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density]
        ns = [r['n'] for r in density_results]
        exhaustive_ops = [r['exhaustive_ops'] for r in density_results]
        plt.plot(ns, exhaustive_ops, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Number of Basic Operations')
    plt.title('Exhaustive Search Basic Operations vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/basic_ops_exhaustive_all_densities.png')
    plt.show()

    # Reset markers and colors
    markers = itertools.cycle(('o', 'x', '^', 's', 'D', '*'))
    colors = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y'))

    # Plot precision of Greedy Heuristic
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density and r['greedy_precision'] is not None]
        ns_precision = [r['n'] for r in density_results]
        precisions = [r['greedy_precision'] for r in density_results]
        if ns_precision:  # Check if the list is not empty
            plt.plot(ns_precision, precisions, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Precision (Greedy Weight / Optimal Weight)')
    plt.title('Precision of Greedy Heuristic')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/precision_all_densities.png')
    plt.show()

    # Plot execution time for Randomized Algorithm
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density]
        ns = [r['n'] for r in density_results]
        randomized_times = [r['randomized_time'] for r in density_results]
        plt.plot(ns, randomized_times, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Execution Time (milliseconds)')
    plt.title('Randomized Algorithm Execution Time vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/execution_time_randomized_all_densities.png')
    plt.show()

    # Plot precision of Randomized Algorithm
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density and r['randomized_precision'] is not None]
        ns_precision = [r['n'] for r in density_results]
        randomized_precisions = [r['randomized_precision'] for r in density_results]
        if ns_precision:  # Check if the list is not empty
            plt.plot(ns_precision, randomized_precisions, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Precision (Randomized Weight / Optimal Weight)')
    plt.title('Precision of Randomized Algorithm')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/precision_randomized_all_densities.png')
    plt.show()

    # Plot number of basic operations for Randomized Algorithm
    plt.figure(figsize=(10, 6))
    for density in densities:
        density_results = [r for r in results if r['density'] == density and r['randomized_ops'] is not None]
        ns_ops = [r['n'] for r in density_results]
        randomized_ops = [r['randomized_ops'] for r in density_results]
        if ns_ops:  # Check if the list is not empty
            plt.plot(ns_ops, randomized_ops, label=f'Density={density}', marker=next(markers), color=next(colors))
    plt.xlabel('Number of Vertices (n)')
    plt.ylabel('Number of Basic Operations')
    plt.title('Randomized Algorithm Basic Operations vs Number of Vertices')
    plt.legend()
    plt.grid(True)
    plt.savefig('plots/basic_ops_randomized_all_densities.png')
    plt.show()
