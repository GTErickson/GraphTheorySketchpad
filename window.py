import pygame
import sys
from logic import calculate_components, calculate_degree, calculate_parallel_edge_offset, adjacency_matrix, laplacian_matrix, calculate_eigen
from style import LAUNCHER_HEIGHT, LAUNCHER_WIDTH, SKETCHPAD_HEIGHT, SKETCHPAD_WIDTH, BACKGROUND_COLOR, BUTTON_COLOR, TEXT_COLOR, NODE_COLOR, NODE_RADIUS, EDGE_COLOR, FONT_COLOR, font, COLOR_OPTIONS

def draw_button(screen, text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, text_color)
    screen.blit(label, (x + width // 2 - label.get_width() // 2, y + height // 2 - label.get_height() // 2))

def launcher_window():
    screen = pygame.display.set_mode((LAUNCHER_WIDTH, LAUNCHER_HEIGHT))
    pygame.display.set_caption("Launcher")
    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        draw_button(screen, "Open Sketchpad", 100, 100, 200, 50, BUTTON_COLOR, TEXT_COLOR)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 100 <= x <= 300 and 100 <= y <= 150:  # Button bounds
                    running = False
        pygame.display.flip()
    sketchpad_window()
    
def draw_curved_edge(screen, color, start_pos, end_pos, curvature, thickness=2):
    """Draw a curved edge using a quadratic Bézier approximation."""
    x1, y1 = start_pos
    x2, y2 = end_pos

    # Control point for the curve
    mid_x = (x1 + x2) // 2
    mid_y = (y1 + y2) // 2
    dx, dy = x2 - x1, y2 - y1
    length = (dx**2 + dy**2)**0.5
    norm_dx, norm_dy = -dy / length, dx / length  # Perpendicular direction

    # Offset control point based on curvature
    control_x = mid_x + norm_dx * curvature
    control_y = mid_y + norm_dy * curvature

    # Define the quadratic Bézier curve
    points = []
    for t in [i / 20 for i in range(21)]:  # Generate 21 points along the curve
        bezier_x = (1 - t)**2 * x1 + 2 * (1 - t) * t * control_x + t**2 * x2
        bezier_y = (1 - t)**2 * y1 + 2 * (1 - t) * t * control_y + t**2 * y2
        points.append((bezier_x, bezier_y))

    # Draw the curve
    pygame.draw.lines(screen, color, False, points, thickness) 
    
def draw_matrices_button(screen, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render("Matrices", True, text_color)
    screen.blit(label, (x + width // 2 - label.get_width() // 2, y + height // 2 - label.get_height() // 2))

def draw_eigenvectors_button(screen, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render("Eigenvectors", True, text_color)
    screen.blit(label, (x + width // 2 - label.get_width() // 2, y + height // 2 - label.get_height() // 2))

def sketchpad_window():
    screen = pygame.display.set_mode((SKETCHPAD_WIDTH, SKETCHPAD_HEIGHT))
    pygame.display.set_caption("Graph Theorist's Sketchpad")

    nodes = []  # List of node positions
    edges = []  # Edges are represented as pairs of node indices
    loops = []  # Loops are represented as node indices
    selected_node = None  # For displaying node details and deleting
    selected_edge = None  # For displaying edge details and deleting
    selected_loop = None  # For displaying loop details and deleting
    dragging_node = None  # For dragging nodes
    node_colors = []  # List to store colors for each node
    display_matrices = False  # Flag to control matrix display
    display_eigenvectors = False  # Flag to control eigenvector display

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the info box
        total_vertices = len(nodes)
        total_edges = len(edges)
        total_components = calculate_components(nodes, edges)
        info_box = pygame.Rect(10, 10, 200, 80)
        pygame.draw.rect(screen, (200, 200, 200), info_box)
        pygame.draw.rect(screen, (0, 0, 0), info_box, 2)
        info_text = [
            f"Vertices: {total_vertices}",
            f"Edges: {total_edges}",
            f"Components: {total_components}"
        ]
        for i, text in enumerate(info_text):
            label = font.render(text, True, FONT_COLOR)
            screen.blit(label, (20, 20 + i * 25))
            
        # Add button to show matrices
        draw_matrices_button(screen, 230, 10, 150, 40, BUTTON_COLOR, TEXT_COLOR)
        draw_eigenvectors_button(screen, 230, 60, 150, 40, BUTTON_COLOR, TEXT_COLOR)


        # Display matrices if the flag is set
        if display_matrices:
            adj_matrix = adjacency_matrix(nodes, edges, loops)
            laplacian_matrix_result = laplacian_matrix(nodes, edges, loops)
            
            # Define padding and column width
            padding = 0
            column_width = 20
            
            # Display adjacency matrix
            y_offset = 130
            label = font.render("Adjacency Matrix", True, FONT_COLOR)
            screen.blit(label, (10, y_offset - 20))
            for i, row in enumerate(adj_matrix):
                for j, value in enumerate(row):
                    # Create a string for each matrix entry, with appropriate spacing
                    label = font.render(f"{value}", True, FONT_COLOR)
                    screen.blit(label, (10 + padding + j * column_width, y_offset + i * 25))
            
            # Display Laplacian matrix
            y_offset += 25 + 25 * len(adj_matrix)
            label = font.render("Laplacian Matrix", True, FONT_COLOR)
            screen.blit(label, (10, y_offset - 20))
            for i, row in enumerate(laplacian_matrix_result):
                for j, value in enumerate(row):
                    # Create a string for each matrix entry, with appropriate spacing
                    label = font.render(f"{value}", True, FONT_COLOR)
                    screen.blit(label, (10 + padding + j * column_width, y_offset + i * 25))

                
        # Display eigen if the flag is set
        if display_eigenvectors:
            adj_matrix = adjacency_matrix(nodes, edges, loops)
            laplacian_matrix_result = laplacian_matrix(nodes, edges, loops)
            matrices = [adj_matrix, laplacian_matrix_result]
            labels = ["Adjacency Matrix", "Laplacian Matrix"]
            y_offset = 110
            step = 0
            for matrix in matrices:
                # Calculate eigenvalues and eigenvectors
                    eigenvalues, eigenvectors = calculate_eigen(matrix)
                    
                    
                    label = font.render(f"{labels[step]}:", True, FONT_COLOR)
                    screen.blit(label, (10, y_offset))
                    y_offset += 30  # Adjust spacing
                    
                    # Display eigenvalues
                    label = font.render("Eigenvalues:", True, FONT_COLOR)
                    screen.blit(label, (10, y_offset))
                    eigen_text = ", ".join(f"{val:.2f}" for val in eigenvalues)
                    label = font.render(eigen_text, True, FONT_COLOR)
                    screen.blit(label, (10, y_offset + 25))
                    
                    y_offset += 50  # Adjust spacing
                    
                    # Display eigenvectors
                    label = font.render("Eigenvectors:", True, FONT_COLOR)
                    screen.blit(label, (10, y_offset))
                    for i, vec in enumerate(eigenvectors.T):  # Transpose for column vectors
                        vec_text = ", ".join(f"{val:.2f}" for val in vec)
                        label = font.render(f"v{i+1}: {vec_text}", True, FONT_COLOR)
                        screen.blit(label, (10, y_offset + (i + 1) * 25))
                    
                    y_offset += 25 * (len(matrix) + 1)  # Adjust spacing for next matrix
                    
                    if (step == 0):
                        step = 1
                    else:
                        step = 0
                        

        # Draw edges
        edge_groups = {}
        for i, edge in enumerate(edges):
            node1, node2 = edge
            if node1 > node2:
                node1, node2 = node2, node1  # Ensure a consistent ordering

            # Group edges by their node pairs
            edge_groups.setdefault((node1, node2), []).append(i)

        for (node1, node2), edge_indices in edge_groups.items():
            x1, y1 = nodes[node1]
            x2, y2 = nodes[node2]

            # Calculate and draw each edge
            for index, edge_index in enumerate(edge_indices):
                curvature = calculate_parallel_edge_offset(index, len(edge_indices))
                if index == 0:
                    # Draw the first edge as a straight line
                    pygame.draw.line(screen, EDGE_COLOR, (x1, y1), (x2, y2), 2)
                else:
                    # Draw subsequent edges as curved lines with offset curvature
                    draw_curved_edge(screen, EDGE_COLOR, (x1, y1), (x2, y2), curvature, thickness=2)


        # Draw loops
        for loop_node_index in loops:
            x, y = nodes[loop_node_index]
            pygame.draw.circle(screen, EDGE_COLOR, (x, y + 15 + (NODE_RADIUS / 2)), NODE_RADIUS + 15, 2)

        # Draw nodes with labels
        for i, (x, y) in enumerate(nodes):
            pygame.draw.circle(screen, node_colors[i] if i < len(node_colors) else NODE_COLOR, (x, y), NODE_RADIUS)
            label = font.render(f"{i}", True, FONT_COLOR)
            screen.blit(label, (x - NODE_RADIUS, y - NODE_RADIUS - 20))

        # Highlight the selected node
        if selected_node is not None:
            pygame.draw.circle(screen, (255, 0, 0), nodes[selected_node], NODE_RADIUS + 2, 2)

        # Highlight the selected edge
        if selected_edge is not None:
            node1, node2 = edges[selected_edge]
            pygame.draw.line(screen, (255, 0, 0), nodes[node1], nodes[node2], 3)

        # Highlight the selected loop
        if selected_loop is not None:
            x, y = nodes[selected_loop]
            pygame.draw.circle(screen, (255, 0, 0), (x, y + 15 + (NODE_RADIUS / 2)), NODE_RADIUS + 15, 3)

        # Draw the right panel
        panel_start = SKETCHPAD_WIDTH * 5 // 6
        pygame.draw.rect(screen, (230, 230, 230), (panel_start, 0, SKETCHPAD_WIDTH // 6, SKETCHPAD_HEIGHT))
        pygame.draw.line(screen, (200, 200, 200), (panel_start, 0), (panel_start, SKETCHPAD_HEIGHT), 3)

        # Display node, edge, or loop information and delete button
        delete_button_rect = None
        if selected_node is not None:
            degree = calculate_degree(selected_node, edges, loops)
            node_text = [
                f"Node: {selected_node}",
                f"Degree: {degree}"
            ]
            for i, text in enumerate(node_text):
                label = font.render(text, True, FONT_COLOR)
                screen.blit(label, (SKETCHPAD_WIDTH - 150, 20 + i * 25))


            # Draw delete button
            delete_button_rect = pygame.Rect(panel_start + 20, 100, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, delete_button_rect)
            delete_label = font.render("Delete", True, TEXT_COLOR)
            screen.blit(delete_label, (panel_start + 20 + (100 - delete_label.get_width()) // 2,
                                       100 + (40 - delete_label.get_height()) // 2))

            # Draw color change buttons
            y_offset = 160
            for color_name, color in COLOR_OPTIONS.items():
                color_button_rect = pygame.Rect(panel_start + 20, y_offset, 100, 40)
                pygame.draw.rect(screen, color, color_button_rect)
                color_label = font.render(color_name, True, TEXT_COLOR)
                screen.blit(color_label, (panel_start + 20 + (100 - color_label.get_width()) // 2,
                                         y_offset + (40 - color_label.get_height()) // 2))
                y_offset += 50

        elif selected_edge is not None:
            node1, node2 = edges[selected_edge]
            label = font.render(f"Selected Edge: {node1} -> {node2}", True, FONT_COLOR)
            screen.blit(label, (panel_start + 20, 50))

            # Draw delete button
            delete_button_rect = pygame.Rect(panel_start + 20, 100, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, delete_button_rect)
            delete_label = font.render("Delete", True, TEXT_COLOR)
            screen.blit(delete_label, (panel_start + 20 + (100 - delete_label.get_width()) // 2,
                                       100 + (40 - delete_label.get_height()) // 2))

        elif selected_loop is not None:
            label = font.render(f"Selected Loop: {selected_loop}", True, FONT_COLOR)
            screen.blit(label, (panel_start + 20, 50))

            # Draw delete button
            delete_button_rect = pygame.Rect(panel_start + 20, 100, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, delete_button_rect)
            delete_label = font.render("Delete", True, TEXT_COLOR)
            screen.blit(delete_label, (panel_start + 20 + (100 - delete_label.get_width()) // 2,
                                       100 + (40 - delete_label.get_height()) // 2))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if event.button == 1:  # Left-click
                    # Check if clicking on the delete button
                    if delete_button_rect and delete_button_rect.collidepoint(x, y):
                        if selected_node is not None:
                            # Delete the node and associated edges and loops
                            nodes.pop(selected_node)
                            edges = [(n1, n2) for n1, n2 in edges if n1 != selected_node and n2 != selected_node]
                            loops = [loop for loop in loops if loop != selected_node]
                            edges = [(n1 - (n1 > selected_node), n2 - (n2 > selected_node)) for n1, n2 in edges]
                            loops = [loop - (loop > selected_node) for loop in loops]
                            node_colors.pop(selected_node)
                            selected_node = None
                        elif selected_edge is not None:
                            # Delete the selected edge
                            edges.pop(selected_edge)
                            selected_edge = None
                        elif selected_loop is not None:
                            # Delete the selected loop
                            loops.remove(selected_loop)
                            selected_loop = None
                        continue

                    # Check if clicking on a color button
                    if selected_node is not None:
                        y_offset = 160
                        for color_name, color in COLOR_OPTIONS.items():
                            color_button_rect = pygame.Rect(panel_start + 20, y_offset, 100, 40)
                            if color_button_rect.collidepoint(x, y):
                                node_colors[selected_node] = color
                                break
                            y_offset += 50

                    # Prioritize node selection
                    clicked_node = None
                    for i, (nx, ny) in enumerate(nodes):
                        if (x - nx) ** 2 + (y - ny) ** 2 <= NODE_RADIUS ** 2:
                            clicked_node = i
                            dragging_node = i
                            break
                        
                    # Check if matrix button is clicked
                    if 230 <= x <= 380 and 10 <= y <= 50:
                        display_matrices = not display_matrices  # Toggle matrix display
                        display_eigenvectors = False
                    # Check if clicking on the Show Eigenvectors button
                    elif 230 <= x <= 380 and 60 <= y <= 100:
                        display_eigenvectors = not display_eigenvectors
                        display_matrices = False
                    
                    elif clicked_node is not None:
                        selected_node = clicked_node
                        selected_edge = None
                        selected_loop = None
                    else:
                        # Check if a loop is clicked
                        clicked_loop = None
                        for i in loops:
                            lx, ly = nodes[i]
                            if (x - lx) ** 2 + (y - (ly + 15 + (NODE_RADIUS / 2))) ** 2 <= (NODE_RADIUS + 15) ** 2:
                                clicked_loop = i
                                break

                        if clicked_loop is not None:
                            selected_loop = clicked_loop
                            selected_node = None
                            selected_edge = None
                        else:
                            # Check if an edge is clicked
                            clicked_edge = None
                            for i, (node1, node2) in enumerate(edges):
                                x1, y1 = nodes[node1]
                                x2, y2 = nodes[node2]
                                if abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1) / (
                                    (x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 < 5:
                                    # Ensure edge part clicked is not under a node
                                    under_node = any(
                                        (x - nx) ** 2 + (y - ny) ** 2 <= NODE_RADIUS ** 2 for nx, ny in nodes
                                    )
                                    if not under_node:
                                        clicked_edge = i
                                        break

                            if clicked_edge is not None:
                                selected_edge = clicked_edge
                                selected_node = None
                                selected_loop = None
                            else:
                                if x < panel_start:  # Click is in the drawing area
                                    nodes.append((x, y))
                                    node_colors.append(NODE_COLOR)
                                    selected_node = len(nodes) - 1
                                    selected_edge = None
                                    selected_loop = None

                elif event.button == 3:  # Right-click
                    for i, (nx, ny) in enumerate(nodes):
                        if (x - nx) ** 2 + (y - ny) ** 2 <= NODE_RADIUS ** 2:
                            if selected_node is None:
                                selected_node = i
                            elif selected_node == i:
                                if i not in loops:
                                    loops.append(i)
                                selected_node = None
                            else:
                                # Allow parallel edges by not checking if edge already exists
                                edges.append((selected_node, i))
                                selected_node = None

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_node = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging_node is not None:
                    nodes[dragging_node] = event.pos

        pygame.display.flip()
    
    
