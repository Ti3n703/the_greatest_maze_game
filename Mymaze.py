# Mymaze.py
import random
import heapq
from collections import deque
import pygame

class Maze:
    # Hàm khởi tạo giờ đây nhận đối tượng path từ Game
    def __init__(self, game, path):
        # The game instance is now correctly passed and referenced
        self.size = game.size
        self.screen = game.screen
        self.CELL_SIZE = 40
        self.WALL_COLOR = (0, 0, 0)
        self.WALL_THICKNESS = 2
        self.highlight_color = (255, 0, 0)
        # Đối tượng path được nhận từ bên ngoài
        self.path = path

    

    def draw_maze(self, animate=True, delay=0.05):
        """
        Draws the maze on the screen.
        
        Args:
            animate: If True, animates the maze generation.
            delay: Delay in seconds between animation steps.
        """
        self.screen.fill((255, 255, 255))
        
        if animate:
            temp_path = My_maze_path(self.size)
            temp_path.add_grid(self.size)
            
            for cell1, cell2 in self.path.build_steps:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                
                temp_path.add_edge(cell1, cell2, 1)
                
                self.screen.fill((255, 255, 255))
                self._draw_final_maze(temp_path)
                
                row, col = map(int, cell1.split(','))
                x = col * self.CELL_SIZE    
                y = row * self.CELL_SIZE
                pygame.draw.rect(self.screen, self.highlight_color, (x, y, self.CELL_SIZE-3, self.CELL_SIZE-3))
                pygame.display.flip()
                pygame.time.delay(int(delay * 1000))

        # Draw the final, complete maze
        self._draw_final_maze(self.path)
        
    def _draw_final_maze(self, maze_path):
        """Helper function to draw the maze based on a given path object."""
        self.screen.fill((255, 255, 255))
        
        # Draw the outer boundary of the maze
        pygame.draw.rect(self.screen, self.WALL_COLOR, (0, 0, self.size * self.CELL_SIZE, self.size * self.CELL_SIZE), self.WALL_THICKNESS)
        
        # Draw internal walls where no path exists
        for row in range(self.size):
            for col in range(self.size):
                current = f"{row},{col}"
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE

                # Check for a path to the right neighbor
                right_neighbor = f"{row},{col+1}"
                if col + 1 < self.size and right_neighbor not in maze_path.adjacency_list.get(current, {}):
                    pygame.draw.line(self.screen, self.WALL_COLOR, (x  + self.CELL_SIZE, y), (x + self.CELL_SIZE, y + self.CELL_SIZE), self.WALL_THICKNESS)

                # Check for a path to the bottom neighbor
                bottom_neighbor = f"{row+1},{col}"
                if row + 1 < self.size and bottom_neighbor not in maze_path.adjacency_list.get(current, {}):
                    pygame.draw.line(self.screen, self.WALL_COLOR, (x, y + self.CELL_SIZE), (x + self.CELL_SIZE, y + self.CELL_SIZE), self.WALL_THICKNESS)

class My_maze_path:
    def __init__(self, size=20):
        self.adjacency_list = {}
        self.build_steps = []
        self.size = size

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}

    def add_edge(self, from_node, to_node, weight=1):
        self.add_vertex(from_node)
        self.add_vertex(to_node)
        self.adjacency_list[from_node][to_node] = weight
        self.adjacency_list[to_node][from_node] = weight
        self.build_steps.append((from_node, to_node))

    def _prim(self, start_vertex, size):
        # Implementation of Prim's algorithm
        visited = set()
        min_heap = [(0, start_vertex, None)]  # (weight, vertex, parent)
        
        while min_heap and len(visited) < size * size:
            weight, current_vertex, parent_vertex = heapq.heappop(min_heap)
            
            if current_vertex in visited:
                continue
                
            visited.add(current_vertex)
            if parent_vertex:
                self.add_edge(parent_vertex, current_vertex, weight)
            
            row, col = map(int, current_vertex.split(','))
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row, next_col = row + dr, col + dc
                neighbor_vertex = f"{next_row},{next_col}"
                
                if 0 <= next_row < size and 0 <= next_col < size and neighbor_vertex not in visited:
                    edge_weight = random.randint(1, 10)  # Random weight for Prim's
                    heapq.heappush(min_heap, (edge_weight, neighbor_vertex, current_vertex))

    def _dijkstra_path(self, start_vertex, end_vertex):
        """Finds the shortest path from start to end using Dijkstra's algorithm."""
        distances = {vertex: float('infinity') for vertex in self.adjacency_list}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]
        previous_vertices = {vertex: None for vertex in self.adjacency_list}

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue
            
            if current_vertex == end_vertex:
                path = []
                while previous_vertices[current_vertex]:
                    path.insert(0, current_vertex)
                    current_vertex = previous_vertices[current_vertex]
                path.insert(0, start_vertex)
                return path

            for neighbor, weight in self.adjacency_list[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        return None

    def add_grid(self, size):
        for row in range(size):
            for col in range(size):
                self.add_vertex(f'{row},{col}')

    def create_path(self, algorithm='prim'):
        """Creates the maze path using a specified algorithm."""
        self.add_grid(self.size)
        if algorithm == 'prim':
            self._prim('0,0', self.size)
        else:
            raise ValueError("Unknown algorithm: {}".format(algorithm))