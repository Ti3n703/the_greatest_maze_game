import random
import pygame
from maze import Maze_Path
import maze
class ghost:
    def __init__(self,maze):
        self.position = [0, 0]  # Initial position of the ghost
        self.color = (255, 0, 0)  # Red color for the ghost
        self.target = None
        self.state = "roaming"  # Possible states: roaming, chasing
        self.maze = maze 
        self.CELL_SIZE = 40
    def draw_ghost(self, screen):
        pygame.draw.circle(screen, self.color, ((self.position[0]+self.CELL_SIZE)/2, (self.position[1]+self.CELL_SIZE)/2), 10)
    def ghost_behavior(self, maze):
        def distance_to_player():
            return len(maze.dijkstra_path(self.position, maze.player.get_position()))
        if maze.safe_zone.player_is_in_safe_zone or distance_to_player() > 5:
            self.state = 'roaming'
        else :
            self.state = 'chasing'
        self.ghost_action(maze)

    def ghost_action(self, player):
        if self.state == 'roaming':
            x= random.randint(0, self.maze.size - 1)
            y = random.randint(0, self.maze.size - 1)
            random_position = f"{x},{y}"
            self.target = random_position
            self.chase_target(self.maze)
        elif self.state == 'chasing':
            self.target = player.get_position()
            self.chase_target(self.maze)
    def ghost_state(self, maze,player):
        path_to_player = maze.djikstra_path(self.position, player.get_position(), maze)
        distance_to_player = len(path_to_player)
        if self.state == 'roam' and distance_to_player <= 5:
            self.state = 'chasing'
        elif self.state == 'chasing' and distance_to_player > 5:
            self.state = 'roaming'
        return self.state
    def chase_target(self, maze):
        path = maze.dijkstra_path(self.position, self.target)
        if path:
            x,y = path[1].split(',')
            self.position = [int(x), int(y)]
    def update_ghost(self, maze, player):
        self.ghost_behavior(maze)
        self.ghost_state(maze, player)
        self.chase_target(maze)
        self.draw_ghost(maze.screen)
        


if __name__ == "__main__":
    pygame.init()
    size = 20  # Size of the maze (20x20)
    screen = pygame.display.set_mode((size * 20, size * 20))
    pygame.display.set_caption("Ghost Game")
    clock = pygame.time.Clock()
    
    maze_instance = Maze_Path(size)
    maze_instance.add_grid(size)
    maze_instance.connect_all_vertices(size)
    
    ghost_instance = ghost(maze_instance)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))  # Clear the screen with white color
        ghost_instance.draw_ghost(screen)
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 frames per second
    
    pygame.quit()
    
        
        


            

            
        



    



    