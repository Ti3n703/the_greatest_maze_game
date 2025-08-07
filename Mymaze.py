import random
import heapq
from collections import deque
import pygame

class Maze:
    # Hàm khởi tạo giờ đây nhận đối tượng path từ Game
    def __init__(self, game, path):
        self.size = game.size
        self.screen = game.screen
        self.CELL_SIZE = 40
        self.WALL_COLOR = game.WALL_COLOR 
        self.WALL_THICKNESS = game.WALL_THICKNESS
        self.highlight_color = (255, 0, 0)
        # Đối tượng path được nhận từ bên ngoài
        self.path = path
        self.BG_COLOR = game.BG_COLOR

    def _draw_grid_walls(self):
        """Vẽ các đường lưới cho tất cả các bức tường tiềm năng."""
        for row in range(self.size):
            for col in range(self.size):
                x = col * self.CELL_SIZE
                y = row * self.CELL_SIZE

                # Vẽ 4 bức tường cho mỗi ô (chúng sẽ bị xóa nếu có đường đi)
                pygame.draw.line(self.screen, self.WALL_COLOR, (x, y), (x + self.CELL_SIZE, y), self.WALL_THICKNESS)  # trên
                pygame.draw.line(self.screen, self.WALL_COLOR, (x + self.CELL_SIZE, y), (x + self.CELL_SIZE, y + self.CELL_SIZE), self.WALL_THICKNESS)  # phải
                pygame.draw.line(self.screen, self.WALL_COLOR, (x + self.CELL_SIZE, y + self.CELL_SIZE), (x, y + self.CELL_SIZE), self.WALL_THICKNESS)  # dưới
                pygame.draw.line(self.screen, self.WALL_COLOR, (x, y + self.CELL_SIZE), (x, y), self.WALL_THICKNESS)  # trái
    
    def create_path(self, algorithm='prim'):
        """Tạo đường đi mê cung bằng thuật toán đã chỉ định."""
        self.path.add_grid(self.size)
        if algorithm == 'prim':
            # Tọa độ gốc bây giờ là "x,y" (cột, hàng)
            self.path._prim('0,0', self.size)
        elif algorithm == 'kruskal':
            self.path._kruskal(self.size)
        elif algorithm == 'bfs':
            self.path._bfs('0,0', self.size)
        elif algorithm == 'dfs':
            self.path._dfs('0,0', self.size)
        else:
            raise ValueError("Unknown algorithm: {}".format(algorithm))

    def draw_maze(self, animate=True, delay=0.05):
        """
        Vẽ mê cung ra màn hình.
        
        Args:
            animate: Nếu là True, sẽ hiển thị hiệu ứng tạo mê cung.
            delay: Thời gian trễ giữa các bước vẽ animation.
        """
       # self.screen.fill(self.BG_COLOR)

        
        if animate:
            temp_path = My_maze_path(self.size)
            temp_path.add_grid(self.size)
            
            for cell1, cell2 in self.path.build_steps:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        animate = False  # Allow skipping animation with spacebar
                        break
                if not animate:
                    break
                
                temp_path.add_edge(cell1, cell2, 1)
                
                self.screen.fill(self.BG_COLOR)
                self._draw_final_maze(temp_path)
                
                # Tọa độ từ chuỗi là (x,y)
                x, y = map(int, cell1.split(','))
                pixel_x = x * self.CELL_SIZE
                pixel_y = y * self.CELL_SIZE
                pygame.draw.rect(self.screen, self.highlight_color, (pixel_x, pixel_y, self.CELL_SIZE-3, self.CELL_SIZE-3))
                pygame.display.flip()
                pygame.time.delay(int(delay * 1000))

        # Vẽ mê cung hoàn chỉnh
        self._draw_final_maze(self.path)
        
    def _draw_final_maze(self, maze_path):
        """Hàm trợ giúp để vẽ mê cung dựa trên đối tượng path."""
        self.screen.fill(self.BG_COLOR)
        
        # Vẽ đường viền ngoài của mê cung
        pygame.draw.rect(self.screen, self.WALL_COLOR, (0, 0, self.size * self.CELL_SIZE, self.size * self.CELL_SIZE), self.WALL_THICKNESS)
        
        # Vẽ các bức tường bên trong nếu không có đường đi
        for x in range(self.size):
            for y in range(self.size):
                current = f"{x},{y}"
                pixel_x = x * self.CELL_SIZE
                pixel_y = y * self.CELL_SIZE

                # Kiểm tra đường đi đến ô bên phải
                right_neighbor = f"{x+1},{y}"
                if x + 1 < self.size and right_neighbor not in maze_path.adjacency_list.get(current, {}):
                    # Nếu không có đường đi, vẽ tường dọc
                    pygame.draw.line(self.screen, self.WALL_COLOR, (pixel_x + self.CELL_SIZE, pixel_y - 1), (pixel_x + self.CELL_SIZE, pixel_y + self.CELL_SIZE + 1 ), self.WALL_THICKNESS)

                # Kiểm tra đường đi đến ô phía dưới
                bottom_neighbor = f"{x},{y+1}"
                if y + 1 < self.size and bottom_neighbor not in maze_path.adjacency_list.get(current, {}):
                    # Nếu không có đường đi, vẽ tường ngang
                    pygame.draw.line(self.screen, self.WALL_COLOR , (pixel_x-1, pixel_y + self.CELL_SIZE), (pixel_x + self.CELL_SIZE + 1, pixel_y + self.CELL_SIZE), self.WALL_THICKNESS)

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
        # Thuật toán Prim để tạo cây bao trùm tối thiểu (Minimum Spanning Tree)
        visited = set()
        min_heap = [(0, start_vertex, None)]  # (weight, vertex, parent)
        
        while min_heap and len(visited) < size * size:
            weight, current_vertex, parent_vertex = heapq.heappop(min_heap)
            
            if current_vertex in visited:
                continue
                
            visited.add(current_vertex)
            if parent_vertex:
                self.add_edge(parent_vertex, current_vertex, weight)
            
            # Tọa độ được xử lý là (col, row)
            col, row = map(int, current_vertex.split(','))
            
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                next_row, next_col = row + dr, col + dc
                # Chuỗi tọa độ bây giờ là "x,y"
                neighbor_vertex = f"{next_col},{next_row}"
                
                if 0 <= next_row < size and 0 <= next_col < size and neighbor_vertex not in visited:
                    edge_weight = random.randint(1, 10)  # Gán trọng số ngẫu nhiên cho Prim
                    heapq.heappush(min_heap, (edge_weight, neighbor_vertex, current_vertex))

    def _dijkstra_path(self, start_vertex, end_vertex):
        """Tìm đường đi ngắn nhất từ start đến end bằng thuật toán Dijkstra."""
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
                # Chuỗi tọa độ bây giờ là "x,y" (cột, hàng)
                self.add_vertex(f'{col},{row}')
    def add_random_edges(self, size):
        """Thêm các cạnh ngẫu nhiên vào đồ thị hiện có để tạo thêm đường đi."""
        potential_edges = []
        for row in range(size):
            for col in range(size):
                vertex = f"{row},{col}"
                for neighbor in self.get_potential_connection(vertex, size):
                    # Thêm vào danh sách các cạnh tiềm năng nếu chúng chưa tồn tại
                    if neighbor not in self.adjacency_list.get(vertex, {}):
                        # Dùng tuple đã sắp xếp để tránh thêm các cạnh lặp lại (u,v) và (v,u)
                        edge = tuple(sorted((vertex, neighbor)))
                        if edge not in potential_edges:
                            potential_edges.append(edge)
        
        random.shuffle(potential_edges)
        
        # Thêm một phần nhỏ (ví dụ 10%) các cạnh tiềm năng này
        extra_edges_count = int(len(potential_edges) * 0.1)
        added_edges_log = []
        
        for i in range(min(extra_edges_count, len(potential_edges))):
            u, v = potential_edges[i]
            # Thêm cạnh với trọng số ngẫu nhiên
            self.add_edge(u, v, random.randint(1, 5))
            added_edges_log.append((u, v))
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