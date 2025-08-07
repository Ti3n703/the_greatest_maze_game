import pygame
import random

class Safe_Zone:
    def __init__(self, game):
        self.safe_zone_list = set()
        self.player = game.player 
        self.screen = game.screen
        self.maze = game.maze
        self.sz_color = game.sz_color
    
    
    def draw_safe_zone(self):
        for (x,y) in self.safe_zone_list:
            center_x = x * self.maze.CELL_SIZE + self.maze.CELL_SIZE // 2
            center_y = y * self.maze.CELL_SIZE + self.maze.CELL_SIZE // 2
            # Vẽ hình tròn
            pygame.draw.circle(self.screen, self.sz_color, (center_x, center_y), self.maze.CELL_SIZE // 2 - 4)
            
        
    def create_safezone(self, size, count=10):  # count is the number of additional safe zones to create
        self.safe_zone_list = set()
        # Add fixed safe zones
        self.safe_zone_list.add((0, 0))
        self.safe_zone_list.add((0, size-1))
        self.safe_zone_list.add((size-1, 0))
        
        if size > 2:
            self.safe_zone_list.add((size//2, size//2))
            self.safe_zone_list.add((0, size//2))
            self.safe_zone_list.add((size-1, size//2))
            self.safe_zone_list.add((size//2, 0))
            self.safe_zone_list.add((size//2, size-1))
            self.safe_zone_list.add((size//4, size//4))
            self.safe_zone_list.add((size//4, 3*size//4))
            self.safe_zone_list.add((3*size//4, size//4))
            self.safe_zone_list.add((3*size//4, 3*size//4))
            self.safe_zone_list.add((1, 1))
            self.safe_zone_list.add((size-2, size-2))
            self.safe_zone_list.add((size//3, size//3))
            self.safe_zone_list.add((size//3, 2*size//3))
            self.safe_zone_list.add((2*size//3, size//3))
            self.safe_zone_list.add((2*size//3, 2*size//3))
        # Add random safe zones up to count
        initial_count = len(self.safe_zone_list)
        while len(self.safe_zone_list) < initial_count + count:
            y = random.randint(0, size-1)
            x = random.randint(0, size-1)
            self.safe_zone_list.add((y, x))
    
    def player_is_in_safe_zone(self):
        return tuple(self.player.position) in self.safe_zone_list
