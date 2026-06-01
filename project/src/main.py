"""Running the project"""

import os
import sys
import time 


# Add path to import modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph_structure import Graph
from algorithms import bfs, dfs, count_connected_components
from utils import load_graph_from_file, measure_algorithm, save_results


def process_files(datasets_to_process, output_dir, summary_file):
    """Process files"""
    print("=" * 70)
    print("Road Graph Analysis")
    print("=" * 70)
    
    for name, filepath in datasets_to_process:
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
        
        # 2. BFS
        print("\nProcessing BFS...")
        visited_bfs = set()
        start_time = time.time()
        
        for vertex in graph.get_vertices():
            if vertex not in visited_bfs:
                (visited_bfs, _) = bfs(graph, vertex, visited_bfs, internal_visited=None)
        bfs_time = time.time() - start_time
        print(f"  Completed BFS in {bfs_time:.4f} seconds")

        # 3. DFS
        print("Processing DFS...")
        
        # Create variables to save the order
        order_list = []
        counter = [1]
        visited_dfs = set()
        start_time = time.time()
        
        for vertex in graph.get_vertices():
            if vertex not in visited_dfs:
                # DFS for the component that contains the current vertex
                (visited_dfs, _) = dfs(graph, vertex, visited=visited_dfs, 
                           order_list=order_list, counter=counter, internal_visited=None)
        dfs_time = time.time() - start_time

            # Outputs CSV
        dfs_csv_file = os.path.join(output_dir, f"dfs_order_{name}.csv")
        with open(dfs_csv_file, 'w', encoding='utf-8') as csv_f:
            csv_f.write("Order,Vertex_ID\n")
            for order, vertex in order_list:
                csv_f.write(f"{order},{vertex}\n")
            # Outputs by console log
        # print(f"\nDFS Traversal Order (total {len(order_list)} vertices):")
        # print(f"{'Order':<10} {'Node ID'}")
        # for order, vertex in order_list:
        #     print(f"{order:<10} {vertex}")
        print(f"  Completed DFS in {dfs_time:.4f} seconds")
        
        # 4. Count connected components
        # BFS
        print("Counting connected components...")
        start_time = time.time()
        (num_components, component_sizes)= count_connected_components(graph, True)
        bfs_comp_time = time.time() - start_time
        print(f"  Number of connected components: {num_components}")
        print(f"  Completed counting connected components by BFS in {bfs_comp_time:.4f} seconds")

        #DFS
        start_time = time.time()
        (num_components, component_sizes) = count_connected_components(graph, False)
        dfs_comp_time = time.time() - start_time
        print(f"  Completed counting connected components by DFS in {dfs_comp_time:.4f}")

        # 5. Save results
        output_file = os.path.join(output_dir, f"results_{name}.txt")
        save_results(
            output_file, name,
            graph.num_vertices, graph.num_edges,
            num_components, bfs_time, dfs_time, 
            max(component_sizes), min(component_sizes),
            bfs_comp_time, dfs_comp_time
        )
        
        # 6. Save to the summary file
        with open(summary_file, 'a', encoding='utf-8') as sf:
            sf.write(f"{name},{graph.num_vertices},{graph.num_edges},"
                    f"{num_components},{bfs_time},{dfs_time},{max(component_sizes)},{min(component_sizes)},{bfs_comp_time},{dfs_comp_time}\n")
    
    print("\n" + "=" * 70)
    print("DONE.")


def main():
    """main function"""
    # path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # access the base folder "project"
    data_dir = os.path.join(base_dir, 'data') # access data folder
    output_dir = os.path.join(base_dir, 'outputs') #access outputs folder
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # List of original datasets
    full_datasets = [
        ('roadNet-CA', os.path.join(data_dir, 'roadNet-CA.txt')),
        ('roadNet-PA', os.path.join(data_dir, 'roadNet-PA.txt')),
        ('roadNet-TX', os.path.join(data_dir, 'roadNet-TX.txt'))
    ]
    
    # Summary file CSV
    summary_file = os.path.join(output_dir, 'summary.csv')
    with open(summary_file, 'w', encoding='utf-8') as sf:
        sf.write("Dataset,Vertices,Edges,Components,BFSTime,DFSTime,MaxComponent,MinComponent,BFSCompTime,DFSCompTime\n")
    
    # Input starts
    scope = input("Choosing files to analysis (enter 'a' for all files, 's' for specific ones): ")
    
    if scope == 'a':
        # All files
        print("\nProcessing all files...")
        process_files(full_datasets, output_dir, summary_file)
        
    elif scope == 's':
        # Specific files
        try:
            scope_num = int(input("Enter number n (1, 2, or 3) of files: "))
        except ValueError: # loop until inputing valid value
            print("Invalid input!")
            return
        
        if scope_num not in (1, 2, 3):
            print("Invalid number!")
            return
        
        print("Available names: roadNet-CA, roadNet-PA, roadNet-TX")
        print("Enter the name of file(s):")
                
        fname = []
        for i in range(scope_num):
            name = input().strip() # strip deletes the blank space
            fname.append(name)
        
        # Create temp_datasets
        temp_datasets = []
        for requested_name in fname:
            found = False
            for dataset_name, filepath in full_datasets:
                if requested_name == dataset_name:
                    temp_datasets.append((dataset_name, filepath))
                    found = True
                    break
            if not found:
                print(f"'{requested_name}' not found!")
                
        print(f"\nProcessing selected file(s)...")
        process_files(temp_datasets, output_dir, summary_file)
        
    else:
        # Invalid input
        print("Invalid input!")


if __name__ == "__main__":
    main()