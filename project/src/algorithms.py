"""Algorithms of project"""

from collections import deque

def bfs(graph, start, visited=None, internal_visited=None):
    """BFS traversal from start vertex"""
    if visited is None:
        visited = set()
    internal_visited = set()
    queue = deque([start])
    visited.add(start)
    internal_visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                internal_visited.add(neighbor)
                queue.append(neighbor)
    
    return visited, internal_visited

def dfs(graph, start, visited=None, order_list=None, counter=None, internal_visited=None):
    """Non-recursive DFS traversal (using stack to avoid stack overflow with large graphs)"""
    if visited is None:
        visited = set()
    internal_visited = set()
    if order_list is None:
        order_list = []
    if counter is None:
        counter = [1]
    
    stack = [start]
    
    while stack:
        vertex = stack.pop()
        
        if vertex not in visited:
            # Save order when traversal
            order_list.append((counter[0], vertex))
            counter[0] += 1
            visited.add(vertex)
            internal_visited.add(vertex)
            
            # Push neighbors to the stack
            for neighbor in graph.get_neighbors(vertex):
                if neighbor not in visited:
                    stack.append(neighbor)
    
    return visited, internal_visited

def count_connected_components(graph, use_bfs=True):
    """
    Count the number of connected components of the graph
    (use_bfs = True: use BFS 
    use_bfs = False: use DFS)
    """
    visited = set()
    components = []
    component_count = 0
    
    for vertex in graph.get_vertices():
        if vertex not in visited:
            component_count += 1
            if use_bfs:
                (_, component) = bfs(graph, vertex, visited, internal_visited=None)
            else:
                (_, component) = dfs(graph, vertex, visited, order_list=None, counter=None, internal_visited=None)
            components.append(len(component))
    
    return component_count, components