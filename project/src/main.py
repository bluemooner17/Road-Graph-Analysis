"""Running the project"""

import sys
import os

# Add folder to path (ensure that other files will be found when using import)
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 

from graph_struture import Graph
from algorithms import bfs, dfs, count_connected_components
from utils import load_graph_from_file, measure_algorithm, save_results

def main():
    """main function"""
    # path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    output_dir = os.path.join(base_dir, 'outputs')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # List of input files
    datasets = [
        ('roadNet-CA', os.path.join(data_dir, 'roadNet-CA.txt')),
        ('roadNet-PA', os.path.join(data_dir, 'roadNet-PA.txt')),
        ('roadNet-TX', os.path.join(data_dir, 'roadNet-TX.txt'))
    ]
    
    # Summary file CSV
    summary_file = os.path.join(output_dir, 'summary.csv')
    with open(summary_file, 'w', encoding='utf-8') as sf:
        sf.write("Dataset,Vertices,Edges,Components,MaxComponent,BFSTime,DFSTime,CompTime\n")
    
    print("=" * 70)
    print("Road Graph Analysis")
    print("=" * 70)
    
    for name, filepath in datasets:
        print(f"\n{'='*50}")
        print(f"PROCESSING: {name}")
        print(f"{'='*50}")
        
        # Check file existence
        if not os.path.exists(filepath):
            print(f"ERROR: File not found! {filepath}")
            continue
        
        # 1. Read graph
        graph = load_graph_from_file(filepath)
        
        if graph.num_vertices == 0:
            print("This graph is empty!")
            continue
        
        # Traverse from the first vertex
        first_vertex = graph.get_vertices()[0]
        
        # 2. Measure BFS time
        print("\nProcessing BFS...")
        _, bfs_time = measure_algorithm(bfs, graph, first_vertex)
        print(f"  Completed BFS in {bfs_time:.4f} seconds")
        
        # 3. Measure DFS time
        print("Processing DFS...")
        _, dfs_time = measure_algorithm(dfs, graph, first_vertex)
        print(f"  Completed DFS in {dfs_time:.4f} seconds")
        
        # 4. Count connected components
        print("Counting connected components...")
        (num_components, component_sizes), comp_time = measure_algorithm(
            count_connected_components, graph, True
        )
        print(f"  Number of connected components: {num_components}")
        print(f"  Completed counting connected components in {comp_time:.4f} seconds")
        
        # 5. Save results
        output_file = os.path.join(output_dir, f"results_{name}.txt")
        save_results(
            output_file, name,
            graph.num_vertices, graph.num_edges,
            num_components, component_sizes,
            bfs_time, dfs_time, comp_time
        )
        
        # 6. Save to the summary file
        with open(summary_file, 'a', encoding='utf-8') as sf:
            sf.write(f"{name},{graph.num_vertices},{graph.num_edges},"
                    f"{num_components},{max(component_sizes)},{bfs_time},{dfs_time},{comp_time}\n")
    
    print("\n" + "=" * 70)
    print("DONE! The results are saved in the outputs folder.")
    print("=" * 70)

if __name__ == "__main__":
    main()