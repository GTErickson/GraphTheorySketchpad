import numpy as np
import sys

def calculate_components(nodes, edges):
    """Calculate the number of connected components in the graph."""
    from collections import defaultdict, deque

    if not nodes:
        return 0  # No components if no nodes

    # Build adjacency list
    adjacency_list = defaultdict(list)
    for n1, n2 in edges:
        adjacency_list[n1].append(n2)
        adjacency_list[n2].append(n1)

    visited = set()
    components = 0

    # BFS to count components
    for node in range(len(nodes)):
        if node not in visited:
            components += 1
            queue = deque([node])
            while queue:
                current = queue.popleft()
                for neighbor in adjacency_list[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components

def calculate_degree(node_index, edges, loops):
    """Calculate the total degree of a node."""
    degree = sum(1 for edge in edges if node_index in edge)
    degree += loops.count(node_index)  # Add loop count
    return degree

def calculate_parallel_edge_offset(index, total_edges, direction=1):
    """Calculate the offset for parallel edges uniformly."""
    spacing = 20  # Spacing between parallel edges
    offset = (((index - 1) // 2) + 1) * spacing
    return -offset if index % 2 == 0 else offset

def adjacency_matrix(nodes, edges, loops):
    """Calculate the adjacency matrix of the graph."""
    n = len(nodes)
    matrix = np.zeros((n, n), dtype=int)
    
    for node1, node2 in edges:
        matrix[node1][node2] = 1
        matrix[node2][node1] = 1  # For undirected graphs
    
    # Add loops to the adjacency matrix (self-loops)
    for loop_node in loops:
        matrix[loop_node][loop_node] = 1
    
    return matrix

def laplacian_matrix(nodes, edges, loops):
    """Calculate the Laplacian matrix of the graph."""
    n = len(nodes)
    adj_matrix = adjacency_matrix(nodes, edges, loops)
    degree_matrix = np.diag(np.sum(adj_matrix, axis=1))
    
    # Laplacian is the degree matrix minus the adjacency matrix
    return degree_matrix - adj_matrix

def calculate_eigen(matrix):
    if not isinstance(matrix, np.ndarray) or len(matrix.shape) != 2:
        raise ValueError(f"Input must be a 2D NumPy array. Got: {type(matrix)}, shape: {getattr(matrix, 'shape', None)}")
    return np.linalg.eig(matrix)