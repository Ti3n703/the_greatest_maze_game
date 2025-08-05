import pygame
import maze
import screen
import ghost

class player:
    def __init__(self,maze):
        self.color = (0, 255, 0)  # Green color for the player
        self.position = [0, 0]  # Initial position of the player
        self.maze = maze
        self.CELL_SIZE = 40  # Size of each cell in the maze
    def _move_up(self):
        self.position[1] -= 1
    def _move_down(self):
        self.position[1] += 1
    def _move_left(self):   
        self.position[0] -= 1
    def _move_right(self):
        self.position[0] += 1
    def _check_valid_move(self, dx, dy):
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        return self.maze.is_neighbour(new_x, new_y)
        
    def _get_position(self):
        return self.position
    def draw_player(self, screen):
        pygame.draw.circle(screen, self.color, ((self.position[0]+self.CELL_SIZE)/2,(self.position[1]+self.CELL_SIZE)/2), 10)
    def check_event(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if self._check_valid_move(0, -1):
                self._move_up()
        elif keys[pygame.K_DOWN]:
            if self._check_valid_move(0, 1):
                self._move_down()
        elif keys[pygame.K_LEFT]:
            if self._check_valid_move(-1, 0):
                self._move_left()
        elif keys[pygame.K_RIGHT]:
            if self._check_valid_move(1, 0): 
                self._move_right()
        
            
            return True

        
    def update_player(self):
        self.check_event()
        self.draw_player(self.maze.screen)