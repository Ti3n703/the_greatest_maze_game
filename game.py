import pygame
from Mymaze import Maze, My_maze_path
from screen import Game_Screen
import exitPoint
import safezone 
import pacman 
import ghost

class Game:
    def __init__(self, size):
        pygame.init()
        self.size = size
        self.environ = Game_Screen(20, size * 40, size * 40)
        self.screen = self.environ.screen
        
        # Create the path object first
        self.path = My_maze_path(self.size)
        
        self.path.create_path('prim')
        # Then create the maze, passing the path object explicitly
        self.maze = Maze(self, self.path)
        self.ghost_speed = 5

        self.maze.draw_maze(animate=True)
        
        self.player = pacman.player(self)
        self.safe_zone = safezone.Safe_Zone(self)
        self.safe_zone.create_safezone(size)
        self.ghost = ghost.ghost(self)
        # FIX: Correctly initialize Exit_Point with the maze instance
        self.exit_point = exitPoint.Exit_Point(self.maze)
        self.CELL_SIZE = 40
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            self.screen.fill((255, 255, 255))
            self.maze.draw_maze(animate=False)
            self.safe_zone.draw_safe_zone(self.maze)
            self.exit_point.draw_exit_point()

            self.player.update_player()
            self.ghost.update_ghost()

            self.environ.flip()
            self.clock.tick(60)

        pygame.quit()
if __name__ =="__main__":
    game = Game(20)
    game.run()