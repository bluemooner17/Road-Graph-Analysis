"""Structure of graph"""

class Graph:
    def __init__(self):
        """Initialize an empty graph"""
        self.adjacency_list = {}  # dict: vertex -> list of neighbors
        self.num_vertices = 0
        self.num_edges = 0
    
    def add_vertex(self, vertex):
        """Add a vertex to the graph"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.num_vertices += 1
    
    def add_edge(self, u, v):
        """Add scalar u-v edge (both u and v)"""
        # Add vertices if they are not in the graph
        if u not in self.adjacency_list:
            self.add_vertex(u)
        if v not in self.adjacency_list:
            self.add_vertex(v)
        
        # Add edge
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)
            self.num_edges += 1 # if the edge already exists, num_edges unchanges
    
    def get_neighbors(self, vertex):
        """Returns the list of vertices adjacent to the vertex"""
        return self.adjacency_list.get(vertex, [])
    
    def get_vertices(self):
        """Returns the list of all vertices"""
        return list(self.adjacency_list.keys())
    
    def __len__(self):
        """Number of vertices in the list"""
        return self.num_vertices
    
    def __repr__(self):
        """Representation"""
        return f"Graph(vertices={self.num_vertices}, edges={self.num_edges})"
    