"""Functions for reading files, measuring time, and logging"""

import time

def load_graph_from_file(filepath):
    """Read graph from file"""
    from graph_structure import Graph
    
    graph = Graph()
    
    print(f"Reading file: {filepath}")
    start_time = time.time()
    
    line_count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                u = int(parts[0])
                v = int(parts[1])
                graph.add_edge(u, v)
                line_count += 1
                    
    elapsed = time.time() - start_time
    print(f"Completed: {graph.num_vertices} vertices, {graph.num_edges} edges")
    print(f"Reading time: {elapsed:.2f} seconds")
    
    return graph

def measure_algorithm(algorithm_func, graph, *args, **kwargs):
    """Measure the execution time of an algorithm."""
    start = time.time()
    result = algorithm_func(graph, *args, **kwargs) # run the process of traversal to calculate the period of time
    elapsed = time.time() - start
    return result, elapsed # return result means the traversal is done

def save_results(filename, dataset_name, num_vertices, num_edges, 
                 num_components, component_sizes, bfs_time, dfs_time, comp_time):
    """Output"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"GRAPH ANALYSIS RESULTS: {dataset_name}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Number of Vertices: {num_vertices:,}\n")
        f.write(f"Number of Edges: {num_edges:,}\n")

        f.write("-" * 40 + "\n")
        f.write("CONNECTED COMPONENTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Number of connected components: {num_components}\n")
                        
        f.write("-" * 40 + "\n")
        f.write("EXECUTION TIME\n")
        f.write("-" * 40 + "\n")
        f.write(f"BFS: {bfs_time:.4f} seconds\n")
        f.write(f"DFS: {dfs_time:.4f} seconds\n")
        f.write(f"Counting connected components: {comp_time:.4f} seconds\n\n")
    
    print(f"Saved in: {filename}")