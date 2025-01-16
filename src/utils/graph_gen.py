import networkx as nx
import random
import itertools
import math

def generate_random_graph(n, edge_density, seed):
    random.seed(seed)
    G = nx.Graph()
    # Add n nodes with random positions
    positions = {}
    while len(positions) < n:
        x, y = random.randint(1, 1000), random.randint(1, 1000)
        # Ensure nodes are not too close
        too_close = False
        for pos in positions.values():
            if math.hypot(x - pos[0], y - pos[1]) < 10:
                too_close = True
                break
        if not too_close:
            positions[len(positions)] = (x, y)
    G.add_nodes_from(positions.keys())
    # Assign random weights
    weights = {v: random.uniform(1, 20) for v in G.nodes()}
    nx.set_node_attributes(G, weights, 'weight')
    # Assign x and y coordinates as separate attributes
    x_coords = {node: pos[0] for node, pos in positions.items()}
    y_coords = {node: pos[1] for node, pos in positions.items()}
    nx.set_node_attributes(G, x_coords, 'x')
    nx.set_node_attributes(G, y_coords, 'y')
    # Possible edges
    possible_edges = list(itertools.combinations(G.nodes(), 2))
    # Calculate number of edges based on density
    m = int(edge_density * len(possible_edges))
    # Randomly select edges
    edges = random.sample(possible_edges, m)
    G.add_edges_from(edges)
    return G, weights, positions  # positions can be left as is if needed elsewhere
