# ghost.py
import random
import pygame

class ghost:
    def __init__(self,game):
        # Vị trí ban đầu của ma, giờ là góc dưới bên phải
        self.position = [game.size - 1, game.size - 1]
        self.color = (255, 0, 0)
        self.target = None
        self.state = "roaming"
        self.maze = game.maze
        self.screen = game.screen
        self.player = game.player
        self.path = game.path
        self.safe_zone = game.safe_zone
        self.move_delay = game.ghost_speed

        self.move_counter = 0
        self.CELL_SIZE = game.CELL_SIZE

    def draw_ghost(self):
        pixel_x = self.position[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        pixel_y = self.position[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        pygame.draw.circle(self.screen, self.color, (pixel_x, pixel_y), 10)

    def chase_target(self):
        """Di chuyển ma về phía mục tiêu theo đường ngắn nhất."""
        start = f"{self.position[0]},{self.position[1]}"
        path_to_target = self.path._dijkstra_path(start, self.target)
        
        # Di chuyển đến bước tiếp theo trên đường đi
        if path_to_target and len(path_to_target) > 1:
            x, y = map(int, path_to_target[1].split(','))
            self.position = [x, y]
        else:
            # Nếu không tìm thấy đường đi hoặc đã đến nơi, chọn một hướng ngẫu nhiên để di chuyển
            # Trong trường hợp này, hành vi "roam" mới sẽ được kích hoạt bởi update_ghost
            self.target = None


    def roam(self):
        """Di chuyển ngẫu nhiên đến một ô lân cận hợp lệ. (Chức năng này không còn được sử dụng trực tiếp cho trạng thái roaming, thay vào đó, ma sẽ đi đến một điểm ngẫu nhiên.)"""
        current_pos_str = f"{self.position[0]},{self.position[1]}"
        # Lấy danh sách các ô lân cận hợp lệ từ đường đi
        neighbors = list(self.path.adjacency_list.get(current_pos_str, {}).keys())
        if neighbors:
            next_pos_str = random.choice(neighbors)
            x, y = map(int, next_pos_str.split(','))
            self.position = [x, y]
            
    def check_event(self):
        """
        Cập nhật logic và vị trí của ma trong mỗi khung hình.
        Đây là hàm chính để xử lý hành vi của ma.
        """
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        
        self.move_counter = 0
        
        px, py = self.player._get_position()
        player_pos = f"{px},{py}"
        
        # Cập nhật trạng thái của ma
        if self.safe_zone.player_is_in_safe_zone():
            self.state = 'roaming'
        else:
            current_ghost_pos = f"{self.position[0]},{self.position[1]}"
            distance_path = self.path._dijkstra_path(current_ghost_pos, player_pos)
            distance = len(distance_path) if distance_path else float('inf')
            self.state = 'roaming' if distance > 5 else 'chasing'
        
        # Thực hiện hành động dựa trên trạng thái
        if self.state == 'roaming':
            # Nếu ma không có mục tiêu hoặc đã đến mục tiêu, chọn một điểm ngẫu nhiên mới
            if self.target is None or self.position == list(map(int, self.target.split(','))):
                x = random.randint(0, self.maze.size - 1)
                y = random.randint(0, self.maze.size - 1)
                self.target = f"{x},{y}"
            
            # Di chuyển đến mục tiêu ngẫu nhiên
            self.chase_target()
        else:  # 'chasing'
            self.target = player_pos
            self.chase_target()
        
    def update_ghost(self):
        self.check_event()
        self.draw_ghost()
    
