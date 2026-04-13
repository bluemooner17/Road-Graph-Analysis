"""Functions for reading files, measuring time, and logging"""

import time
import os

def load_graph_from_file(filepath):
    """Read graph from file"""
    from graph_struture import Graph
    
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
                
                # if line_count % 1000000 == 0:
                #     print(f"  Read {line_count} edges...")
    
    elapsed = time.time() - start_time
    print(f"Completed: {graph.num_vertices} vertices, {graph.num_edges} edges")
    print(f"Reading time: {elapsed:.2f} seconds")
    
    return graph

def measure_algorithm(algorithm_func, graph, *args, **kwargs):
    """Measure the execution time of an algorithm."""
    start = time.time()
    result = algorithm_func(graph, *args, **kwargs)
    elapsed = time.time() - start
    return result, elapsed

def save_results(filename, dataset_name, num_vertices, num_edges, 
                 num_components, component_sizes, bfs_time, dfs_time, comp_time):
    """Output"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"GRAPH ANALYSIS RESULTS: {dataset_name}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write(f"Number of Vertices: {num_vertices:,}\n")
        f.write(f"Number of Edges: {num_edges:,}\n")
        f.write(f"Density of the graph: {2*num_edges/(num_vertices*(num_vertices-1)) if num_vertices>1 else 0:.2e}\n\n")
        
        f.write("-" * 40 + "\n")
        f.write("EXECUTION TIME\n")
        f.write("-" * 40 + "\n")
        f.write(f"BFS: {bfs_time:.4f} seconds\n")
        f.write(f"DFS: {dfs_time:.4f} seconds\n")
        f.write(f"Counting connected components: {comp_time:.4f} seconds\n\n")
        
        f.write("-" * 40 + "\n")
        f.write("CONNECTED COMPONENTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Number of connected components: {num_components}\n")
        
        # Show 10 largest components
        component_sizes_sorted = sorted(component_sizes, reverse=True)
        f.write("\nThe 10 largest components (number of vertices):\n")
        for i, size in enumerate(component_sizes_sorted[:10], 1):
            f.write(f"  #{i}: {size:,} vertices\n")
        
        f.write("\nSize distribution:\n")
        f.write(f"  Smallest: {min(component_sizes):,}\n")
        f.write(f"  Largest: {max(component_sizes):,}\n")
        f.write(f"  Medium: {sum(component_sizes)/len(component_sizes):.2f}\n")
    
    print(f"Saved in: {filename}")