import pygame
class Game_Screen:
    def __init__(self, size, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.size =  size
        pygame.display.set_caption("Maze Game")
        self.CELL_SIZE = 20  # Size of each cell in the maze
    
    def fill(self, color):
        self.screen.fill(color)
    
    def flip(self):
        pygame.display.flip()
    
    def draw_grid(self, maze):
        maze.draw_grid(self.screen)
    
    def draw_maze(self, maze):
        maze.draw_maze(self.screen)