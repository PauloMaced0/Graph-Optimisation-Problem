# Sedgewick & Wayne TXT Files

## Graph Types

- **G - Graph**  
*Undirected Graph*

- **DG - Digraph**  
*Directed Graph*

- **DAG - Directed Acyclic Graph**  
*Directed Acyclic Graph*

- **EWD - Edge-Weighted Digraph**  
*Directed Graph with weights associated to edges*

## NOTE:

1. **Edge Weights:**  
When present, the weights of the edges are real numbers.

2. **Loops:**  
Some files contain loops (i.e., edges where the starting vertex is the same as the ending vertex, `vi = vj`).  
*Identify these in the reading function and do not include these edges.*

## FORMAT:

1. **Directed Graph Indicator (`0 / 1`):**  
   - `0` → Undirected Graph  
   - `1` → Directed Graph

2. **Edge Weights Indicator (`0 / 1`):**  
   - `0` → No weights associated with edges  
   - `1` → Weights are associated with edges

3. **Number of Vertices:**  
An integer representing the total number of vertices in the graph.

4. **Number of Edges:**  
An integer representing the total number of edges in the graph.

5. **Edge Definitions:**  
Each subsequent line defines an edge with the following format:  

    - **starting_vertex:** Identifier for the starting vertex.
    - **ending_vertex:** Identifier for the ending vertex.
    - **weight (optional):** A real number representing the weight of the edge (included only if weights are associated).
