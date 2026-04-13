"""Algorithms of project"""

from collections import deque
import sys

def bfs(graph, start, visited=None):
    """BFS traversal from start vertex"""
    if visited is None:
        visited = set()
    
    queue = deque([start])
    visited.add(start)
    
    while queue:
        vertex = queue.popleft()
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return visited

def dfs(graph, start, visited=None):
    """Non-recursive DFS traversal (using stack to avoid stack overflow with large graphs)"""
    if visited is None:
        visited = set()
    
    stack = [start]
    visited.add(start)
    
    while stack:
        vertex = stack.pop()
        for neighbor in graph.get_neighbors(vertex):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    
    return visited

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
                component = bfs(graph, vertex, visited)
            else:
                component = dfs(graph, vertex, visited)
            components.append(len(component))
    
    return component_count, components
