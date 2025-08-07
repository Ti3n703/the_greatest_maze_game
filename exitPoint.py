import pygame
import Mymaze
import screen

class Exit_Point:
    def __init__(self, maze):
        self.maze = maze
        self.exit_pos = [self.maze.size - 1, self.maze.size - 1]
    def draw_exit_point(self):
        exit_x = self.exit_pos[0]
        exit_y = self.exit_pos[1]
        pixel_x = exit_x * self.maze.CELL_SIZE + self.maze.CELL_SIZE // 2
        pixel_y = exit_y * self.maze.CELL_SIZE + self.maze.CELL_SIZE // 2
        pygame.draw.circle(self.maze.screen, (0, 0, 255), (pixel_x, pixel_y), 10)