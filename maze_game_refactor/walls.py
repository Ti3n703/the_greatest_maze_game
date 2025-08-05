import pygame
class walls:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen, path_list):
        for path in  path_list:
            x, y = map(int, path.split(','))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(x * 10, y * 10, 10, 10))

        pygame.draw.rect(screen, (0, 0, 0), self.rect)  # Draw the wall in black
    
    
    
