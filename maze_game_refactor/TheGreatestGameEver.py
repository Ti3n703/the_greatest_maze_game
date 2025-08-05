import pygame
import ghost
import maze
import safezone
import pacman   
from maze import Maze_Path, Maze
from screen import Game_Screen
import walls

class greatest_game:
    def __init__(self, width, height):
        # Khởi tạo các thực thể
        self.safe_zone = safezone.Safe_Zone(self)  # Pass the game instance to Safe_Zone
        self.path = maze.Maze_Path()  # Giả sử Maze_Path là class path của maze
        self.maze = maze.Maze(20)
        self.walls = walls.walls(0, 0, width, height)   
        self.screen = Game_Screen(width, height)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = pacman.player(self.path)
        
        self.ghost = ghost.ghost(self.path)   

    def running_loop(self):
        # Khởi tạo safezone và maze nếu cần
        self.safe_zone.create_safezone(30, 10)
        self.maze.path.add_grid(30)
        while self.running:
            self.clock.tick(self.fps)
            self._check_event()
            self.update_ghost_player()
            self.draw_maze_animation()
            pygame.display.flip()

    def _check_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            # Xử lý sự kiện di chuyển player
            if event.type == pygame.KEYDOWN:
                self.player.check_event()

    def update_ghost_player(self):        
        # Cập nhật player và ghost
        self.player.update_player()     
        self.ghost.update_ghost(self.maze, self.player)
        # Kiểm tra va chạm
        if hasattr(self.player, 'rect') and hasattr(self.ghost, 'rect'):
            if self.player.position == self.ghost.position:
                self.running = False
        elif hasattr(self.player, 'position') and hasattr(self.ghost, 'position'):
            if self.player.position == self.ghost.position:
                print("Game Over! Bạn đã bị bắt.")
                self.running = False
        # Kiểm tra thắng
        if hasattr(self.safe_zone, 'rect') and hasattr(self.player, 'rect'):
            if self.player.position in self.safe_zone.safe_zone_list:
                print("Chúc mừng! Bạn đã thắng.")
                self.running = False

    def draw_maze_animation(self):
        self.screen.screen.fill((255, 255, 255))  # Clear the screen with white color
        # Vẽ maze
        if hasattr(self.maze, 'draw'):
            self.maze._draw_maze(self.screen.screen)
        # Vẽ safezone
        if hasattr(self.safe_zone, 'draw'):
            self.safe_zone.draw(self.screen.screen)
        # Vẽ player
        if hasattr(self.player, 'draw'):
            self.player.draw_player(self.screen.screen)
        # Vẽ ghost
        if hasattr(self.ghost, 'draw'):
            self.ghost.draw_ghost(self.screen.screen)







if __name__ == "__main__":
    pygame.init()
    width, height = 800, 600
    game = greatest_game(width, height)
    game.running_loop()
    pygame.quit()