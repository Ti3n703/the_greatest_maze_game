import random
import heapq
from collections import deque
import pygame
class Maze:
    def __init__(self, size=20):
        self.size = size
        self.path = Maze_Path(size)
        self.path.add_grid(size)
        self.CELL_SIZE = 40
        self.WALL_COLOR = (0, 0, 0)
    def _draw_grid(self, screen):
        for row in range(self.size):
            for col in range(self.size):
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE

                # Draw 4 walls for each cell
                pygame.draw.line(screen, self.WALL_COLOR, (x, y), (x + self.CELL_SIZE, y), 2)  # top
                pygame.draw.line(screen, self.WALL_COLOR, (x + self.CELL_SIZE, y), (x + self.CELL_SIZE, y + self.CELL_SIZE), 2)  # right
                pygame.draw.line(screen, self.WALL_COLOR, (x + self.CELL_SIZE, y + self.CELL_SIZE), (x, y + self.CELL_SIZE), 2)  # bottom
                pygame.draw.line(screen, self.WALL_COLOR, (x, y + self.CELL_SIZE), (x, y), 2)  # left
    def create_path(self, algorithm='prim'):
        if algorithm == 'prim':
            self.path.prim('0,0', self.size)
        elif algorithm == 'kruskal':
            self.path.kruskal(self.size)
        elif algorithm == 'bfs':
            self.path.bfs('0,0', self.size)
        elif algorithm == 'dfs':
            self.path.dfs('0,0', self.size)
        else:
            raise ValueError("Unknown algorithm: {}".format(algorithm))

    def _draw_maze(self, screen):
            
        for start, end in self.path.build_steps:
            x1, y1 = map(int, start.split(','))
            x2, y2 = map(int, end.split(','))

            # convert to pixel coordinates
            cx = min(x1, x2) * self.CELL_SIZE
            cy = min(y1, y2) * self.CELL_SIZE

            # erase wall between start and end
            if x1 == x2:
                # horizontal movement → erase vertical wall
                mid = (y1 + y2) // 2
                pygame.draw.line(screen, (255, 255, 255), 
                    (x1 * self.CELL_SIZE, mid * self.CELL_SIZE), 
                    ((x1 + 1) * self.CELL_SIZE, mid * self.CELL_SIZE), 2)
            elif y1 == y2:
                # vertical movement → erase horizontal wall
                mid = (x1 + x2) // 2
                pygame.draw.line(screen, (255, 255, 255), 
                    (mid * self.CELL_SIZE, y1 * self.CELL_SIZE), 
                    (mid * self.CELL_SIZE, (y1 + 1) * self.CELL_SIZE), 2)

        


class Maze_Path:
    def __init__(self,size=20):
        self.adjacency_list = {}
        self.build_steps = []
        self.deleted_edges = []
        self.size = size
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}
    def add_edge(self, from_node, to_node, weight=1):
        if from_node not in self.adjacency_list:
            self.adjacency_list[from_node] = {}
        self.adjacency_list[from_node][to_node] = weight


    def is_neighbour(self, v1, v2):
        return v2 in self.adjacency_list[v1]

    
    def add_grid(self,x,):
        for row in range(x):
            for col in range(x):
                self.add_vertex(f'{row},{col}')
    def connect_all_vertices(self, size):
        for row in range(size):
            for col in range(size):
                vertex = f"{row},{col}"
                for neighbor in self.get_potential_connection(vertex, size):
                    if neighbor not in self.adjacency_list[vertex]:
                        self.add_edge(vertex, neighbor, 1)
                
    def get_potential_connection(self, vertex, size):
        connections = []
        row, col = map(int, vertex.split(','))
        if row > 0:
            connections.append(f"{row-1},{col}")
        if row < size - 1:
            connections.append(f"{row+1},{col}")
        if col > 0:
            connections.append(f"{row},{col-1}")
        if col < size - 1:
            connections.append(f"{row},{col+1}")
        random.shuffle(connections)
        return connections

    def manhattan(self, pos1, pos2):
        if isinstance(pos1, list):
            x1, y1 = pos1
        elif isinstance(pos1, tuple):
            x1, y1 = pos1
        else:
            x1, y1 = map(int, pos1.split(','))
        if isinstance(pos2, list):
            x2, y2 = pos2
        elif isinstance(pos2, tuple):
            x2, y2 = pos2
        else:
            x2, y2 = map(int, pos2.split(','))
        return abs(x1 - x2) + abs(y1 - y2)


    def prim(self, start, size ):
        self.build_steps = []
        visited = set([start])
        frontier = []
        start_pos = tuple(map(int, start.split(',')))
        for neighbor in self.get_potential_connection(start, size):
            if neighbor in self.adjacency_list and self.is_neighbour(start, neighbor):
                weight = self.adjacency_list[start][neighbor]
                heapq.heappush(frontier, (weight, random.random(), start, neighbor))
        while frontier:
            weight,  _, u, v = heapq.heappop(frontier)
            if v not in visited:
                visited.add(v)
                self.build_steps.append((u, v))
                print(f"Adding edge: ({u}, {v}),  from start: ")  # Debug
                for next_neighbor in self.get_potential_connection(v, size):
                    if next_neighbor not in visited and v in self.adjacency_list and next_neighbor in self.adjacency_list[v]:
                        next_weight = self.adjacency_list[v][next_neighbor]
                        
                        heapq.heappush(frontier, (next_weight, random.random(), v, next_neighbor))
    def kruskal(self, size):
        self.build_steps = []
        def find(parent, i):
            if parent[i] == i:
                return i
            return find(parent, parent[i])
        def union(parent, rank, x, y):
            xroot = find(parent, x)
            yroot = find(parent, y)
            if rank[xroot] < rank[yroot]:
                parent[xroot] = yroot
            elif rank[xroot] > rank[yroot]:
                parent[yroot] = xroot
            else:
                parent[yroot] = xroot
                rank[xroot] += 1
        edges = []
        for r in range(size):
            for c in range(size):
                u = f"{r},{c}"
                if r + 1 < size:
                    v = f"{r+1},{c}"
                    edges.append((self.adjacency_list[u][v], random.random(), u, v))
                if c + 1 < size:
                    v = f"{r},{c+1}"
                    edges.append((self.adjacency_list[u][v], random.random(), u, v))
        edges.sort()
        parent = {vertex: vertex for vertex in self.adjacency_list}
        rank = {vertex: 0 for vertex in self.adjacency_list}
        for weight, _, u, v in edges:
            x = find(parent, u)
            y = find(parent, v)
            if x != y:
                self.build_steps.append((u, v))
                union(parent, rank, x, y)

    def dfs(self, vertex, size, visited=None):
        if visited is None:
            visited = set()
        visited.add(vertex)
        potential_neighbors_from_grid = self.get_potential_connection(vertex, size)
        random.shuffle(potential_neighbors_from_grid)
        for neighbor in potential_neighbors_from_grid:
            if neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    self.build_steps.append((vertex, neighbor))
                    self.dfs(neighbor, size, visited)
    def bfs(self, start, size):
        # Generate spanning tree using randomized BFS
        self.build_steps = []
        visited = set()
        queue = deque([start])
        visited.add(start)
        print(f"Starting BFS from {start}")

        while queue:
            # Randomize the order of processing current level
            current_level = list(queue)
            random.shuffle(current_level)
            for current in current_level:
                queue.remove(current)
                neighbors = self.get_potential_connection(current, size)
                if neighbors:
                    random.shuffle(neighbors)
                    for neighbor in neighbors:
                        if neighbor in self.adjacency_list[current] and neighbor not in visited:
                            visited.add(neighbor)
                            self.build_steps.append((current, neighbor))
                            queue.append(neighbor)
        # Rebuild graph with spanning tree edges and random weights
        final_edges = self.build_steps
        self.adjacency_list = {}
        for u, v in final_edges:
            self.add_edge(u, v, random.randint(1, 5))
        print(f"Rebuilt graph with {len(self.adjacency_list)} vertices and {sum(len(edges) for edges in self.adjacency_list.values()) // 2} edges")
    def bfs_path(self, start, goal):
        queue = deque([[start]])
        visited = set([start])
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == goal:
                return path
            for neighbor in self.adjacency_list[node]:
                nkey = neighbor
                if nkey not in visited:
                    visited.add(nkey)
                    queue.append(path + [nkey])
        return []

    def dfs_path(self, start, goal):
        stack = [[start]]
        visited = set([start])
        while stack:
            path = stack.pop()
            node = path[-1]
            if node == goal:
                return path
            for neighbor in self.adjacency_list[node]:
                nkey = neighbor
                if nkey not in visited:
                    visited.add(nkey)
                    stack.append(path + [nkey])
        return []

    def dijkstra_path(self, start, goal):
        distances = {vertex: float('inf') for vertex in self.adjacency_list}
        distances[start] = 0
        previous = {vertex: None for vertex in self.adjacency_list}
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            if current_distance > distances[current_vertex]:
                continue
            if current_vertex == goal:
                break
            for neighbor, weight in self.adjacency_list[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        if not path or path[0] != start:
            return []
        return path

    def is_connected(self, start):
        visited = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
        return len(visited) == len(self.adjacency_list)

    def delete_random_edges(self, size):
        g = Maze_Path()
        for vertex, neighbors in self.adjacency_list.items():
            g.adjacency_list[vertex] = neighbors.copy()
        g.build_steps = self.build_steps.copy()
        g.deleted_edges = []
        potential_edges = []
        for row in range(size):
            for col in range(size):
                vertex = f"{row},{col}"
                for neighbor in self.get_potential_connection(vertex, size):
                    if neighbor not in g.adjacency_list[vertex]:
                        potential_edges.append((vertex, neighbor))
        random.shuffle(potential_edges)
        extra_edges = int(len(potential_edges) * 0.1)
        added_edges = []
        for i in range(min(extra_edges, len(potential_edges))):
            u, v = potential_edges[i]
            g.add_edge(u, v, random.randint(1, 5))
            added_edges.append((u, v))
        print(f"Added {len(added_edges)} extra edges: {added_edges[:10]}")
        return g

    def get_all_edges(self):
        edges = []
        added_edges = set()
        for vertex in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[vertex].items():
                edge = tuple(sorted([vertex, neighbor]))
                if edge not in added_edges:
                    edges.append((vertex, neighbor, weight))
                    added_edges.add(edge)
        return edges
    
if __name__ == "__main__":
    pygame.init()
    size = 20  # Size of the maze (20x20)
    screen = pygame.display.set_mode((size * 20, size * 20))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    
    maze_instance = Maze(size)
    maze_instance.create_path('prim')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Clear the screen with white color
        maze_instance._draw_maze(screen)
        maze_instance._draw_grid(screen)
  
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit() 

if __name__ == "__main__":
    pygame.init()
    size = 20  # Size of the maze (20x20)
    screen = pygame.display.set_mode((size * 20, size * 20))
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()
    
    maze_instance = Maze(size)
    maze_instance.create_path('prim')
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Clear the screen with white color
        maze_instance._draw_grid(screen)
  
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()