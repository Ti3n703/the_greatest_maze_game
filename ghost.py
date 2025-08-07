import random
import pygame
class ghost:
    def __init__(self,game):
        self.position = [0, 0]  # Vị trí ban đầu của ma
        self.color = (255, 0, 0)  # Màu đỏ cho ma
        self.target = None
        self.state = "roaming"  # Các trạng thái: roaming, chasing
        self.maze = game.maze
        self.screen = game.screen
        self.player = game.player
        self.path = game.path
        self.safe_zone = game.safe_zone
        self.move_delay = game.ghost_speed

        self.move_counter = 0
        self.CELL_SIZE = 40

    def draw_ghost(self):
        pixel_x = self.position[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        pixel_y = self.position[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        pygame.draw.circle(self.screen, self.color, (pixel_x, pixel_y), 10)

    def chase_target(self):
        """Di chuyển ma về phía người chơi theo đường ngắn nhất."""
        px, py = self.player._get_position()
        self.target = f"{py},{px}" # Sửa lỗi: Đảo tọa độ để khớp với định dạng (y,x) của mê cung

        start = f"{self.position[1]},{self.position[0]}" # Sửa lỗi: Đảo tọa độ (y,x)
        path = self.path._dijkstra_path(start, self.target)
        
        if path and len(path) > 1:
            x, y = map(int, path[1].split(','))
            self.position = [y, x] # Sửa lỗi: Đảo tọa độ để cập nhật vị trí (x,y)
            print(f"Ghost đang đuổi theo. Từ {start} đến {self.target}, bước tiếp theo là ({y},{x})")
        else:
            print(f"Không tìm thấy đường đi từ {start} đến {self.target}. Ghost đứng yên.")


    def update_ghost(self):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        
        self.move_counter = 0
        
        px, py = self.player._get_position()
        # Sửa lỗi: Đảo tọa độ để khớp với định dạng (y,x) của mê cung
        player_pos = f"{py},{px}"
        
        # Kiểm tra nếu người chơi ở trong vùng an toàn
        if self.safe_zone.player_is_in_safe_zone():
            self.state = 'roaming'
        else:
            # Tính khoảng cách đến người chơi và quyết định trạng thái
            current_ghost_pos = f"{self.position[1]},{self.position[0]}" # Sửa lỗi: Đảo tọa độ (y,x)
            distance_path = self.path._dijkstra_path(current_ghost_pos, player_pos)
            distance = len(distance_path) if distance_path else float('inf')
            self.state = 'roaming' if distance > 5 else 'chasing'
            
        if self.state == 'roaming':
            # Logic di chuyển ngẫu nhiên
            current_pos_str = f"{self.position[1]},{self.position[0]}" # Sửa lỗi: Đảo tọa độ (y,x)
            neighbors = list(self.path.adjacency_list.get(current_pos_str, {}).keys())
            if neighbors:
                next_pos_str = random.choice(neighbors)
                x, y = map(int, next_pos_str.split(','))
                self.position = [y, x] # Sửa lỗi: Đảo tọa độ để cập nhật vị trí (x,y)
                print(f"Ghost đang đi lang thang. Vị trí hiện tại: ({self.position[0]},{self.position[1]})")
        else: # Chasing
            self.chase_target()
        
        self.draw_ghost()