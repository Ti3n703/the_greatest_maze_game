import pygame

class player:
    def __init__(self, game):
        self.color = game.player_color
        self.position = [0, 0]  # Lưu vị trí dưới dạng [x, y]
        self.maze = game.maze
        self.screen = game.screen
        self.path = game.path
        self.move_delay = game.player_movement_delay
        self.CELL_SIZE = game.CELL_SIZE
        self.move_counter = 0

    def _get_position(self):
        """Trả về vị trí của người chơi dưới dạng tuple (x, y)."""
        return self.position[0], self.position[1]

    def _move_up(self):
        self.position[1] -= 1

    def _move_down(self):
        self.position[1] += 1

    def _move_left(self):
        self.position[0] -= 1

    def _move_right(self):
        self.position[0] += 1

    def _check_valid_move(self, x, y):
        """Kiểm tra xem một nước đi đến (x, y) có hợp lệ không."""
        cur_x, cur_y = self.position[0], self.position[1]
        new_x, new_y = cur_x + x, cur_y + y

        # In ra thông tin debug
        print(f"Kiểm tra di chuyển từ ({cur_x},{cur_y}) đến ({new_x},{new_y})")

        if not (0 <= new_x < self.maze.size and 0 <= new_y < self.maze.size):
            print(" -> Không hợp lệ: Vượt quá biên giới mê cung.")
            return False

        # Tọa độ bây giờ đã đồng bộ, không cần đảo ngược
        cur_position_str = f"{cur_x},{cur_y}"
        new_position_str = f"{new_x},{new_y}"

        # Kiểm tra xem vị trí mới có phải là hàng xóm trong đường đi mê cung không
        if new_position_str in self.path.adjacency_list.get(cur_position_str, {}):
            print(" -> Hợp lệ: Có đường đi.")
            return True
        print(f" -> Không hợp lệ: Không có đường đi. Các hàng xóm của {cur_position_str} là {list(self.path.adjacency_list.get(cur_position_str, {}).keys())}")
        return False

    def check_event(self):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return

        self.move_counter = 0
        keys = pygame.key.get_pressed()
        
        # Kiểm tra và di chuyển theo một hướng mỗi khung hình
        if keys[pygame.K_UP] and self._check_valid_move(0, -1):
            self._move_up()
        elif keys[pygame.K_DOWN] and self._check_valid_move(0, 1):
            self._move_down()
        elif keys[pygame.K_LEFT] and self._check_valid_move(-1, 0):
            self._move_left()
        elif keys[pygame.K_RIGHT] and self._check_valid_move(1, 0):
            self._move_right()

    def draw_player(self):
        pixel_x = self.position[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        pixel_y = self.position[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        pygame.draw.circle(self.screen, self.color, (pixel_x, pixel_y), 10)

    def update_player(self):
        self.check_event()
        self.draw_player()
