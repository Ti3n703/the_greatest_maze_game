import pygame
import random
import maze
class Safe_Zone:
    def __init__(self, player  ):
        self.rect = pygame.Rect(50, 50, 200, 200)  # Define the safe zone rectangle
        self.safe_zone_list = set()
        self.player = player 
    
        
    
    
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 255), self.rect)  # Blue color for the safe zone
    def create_safezone(self, size, count=10): # count is the number of safe zones to create
        self.safe_zone_list = set()
        self.safe_zone_list.add((0, 0))
        self.safe_zone_list.add((0, size-1))
        self.safe_zone_list.add((size-1, 0))
        self.safe_zone_list.add((size-1, size-1))
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
        while len(self.safe_zone_list) < len(self.safe_zone_list) + count:
            y = random.randint(0, size-1)
            x = random.randint(0, size-1)
            self.safe_zone_list.add((y, x))
    def player_is_in_safe_zone(self):
        return self.player.position in self.safe_zone_list 
