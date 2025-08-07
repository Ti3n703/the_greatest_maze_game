# game.py
import random
import menu
import pygame
from Mymaze import Maze, My_maze_path
from screen import Game_Screen
import exitPoint
import safezone 
import pacman 
import ghost

class Game:
    def __init__(self, size):
        #init environment
        pygame.init()
        #color 
        self.sz_color = ((97, 55, 107))
        self.player_color = ((158, 124, 16))
        self.BG_COLOR=((23, 32, 38))
        self.WALL_COLOR = ((141, 226, 46))
        self.exit_color = ((185, 55, 93))
        #maze config
        self.WALL_THICKNESS = 4

        #environtment
        self.CELL_SIZE = 40
        self.game_state = 'start'
        self.size = size
        self.environ = Game_Screen(20, size * 40, size * 40)
        self.screen = self.environ.screen
        self.menu = menu.Menu(self.screen, self.size)
        
        #init maze
        self.path = My_maze_path(self.size)
        self.maze = Maze(self, self.path)
        self.maze.create_path('prim')
        self.path.add_random_edges(self.size)
        #maze config
        self.ghost_speed = 40
        #config environtment

        #player config

        self.player_movement_delay = 7
        self.player = pacman.player(self)
        self.safe_zone = safezone.Safe_Zone(self)
        self.safe_zone.create_safezone(size)
        #ghost config
        self.num_ghosts = 6
        self.exit_point = exitPoint.Exit_Point(self)
        self.CELL_SIZE = 40
        self.clock = pygame.time.Clock()
        self.ghosts = []
        for i in range(self.num_ghosts):
            new_ghost = ghost.ghost(self)
            # Gán vị trí ngẫu nhiên cho mỗi con ma
            new_ghost.position = [random.randint(0, self.size - 1), random.randint(0, self.size - 1)]
            # Gán màu sắc ngẫu nhiên
            new_ghost.color = ((225,0,0))
            self.ghosts.append(new_ghost)

        self.exit_point = exitPoint.Exit_Point(self)
        #safe zone config
        
        #draw maze animation
        self.maze.draw_maze(animate=True)


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.game_state == 'start':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_state = 'playing'
                elif self.game_state == 'win':
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        self.game_state = 'playing'
                        self.reset_game()
            if self.game_state == 'start':
                self.menu.draw_start_menu()
            elif self.game_state == 'lose':
                self.menu.draw_lose_menu()
            elif self.game_state == 'win':
                self.menu.draw_win_menu()

            elif self.game_state =='playing':


            
                self.screen.fill(self.BG_COLOR) 
                self.maze.draw_maze(animate=False) # Chỉ vẽ mê cung hoàn chỉnh
                self.safe_zone.draw_safe_zone()
               
                self.exit_point.draw_exit_point()

                self.player.update_player()
                if tuple(self.player.position) in self.safe_zone.safe_zone_list:
                    print(self.player.position)

                for g in self.ghosts: 
                    g.update_ghost()
                self.check_event()
                
                

                self.environ.flip()
                self.clock.tick(60) # Thiết lập tốc độ khung hình
                


        pygame.quit()
    def reset_game(self):
        self.path = My_maze_path(self.size)
        self.maze = Maze(self, self.path)
        self.maze.create_path('prim')
        self.ghost_speed = 5
        self.maze.draw_maze(animate=True)
        self.player = pacman.player(self)
        self.safe_zone = safezone.Safe_Zone(self)
        self.safe_zone.create_safezone(self.size)
        self.ghost = ghost.ghost(self)
        self.exit_point = exitPoint.Exit_Point(self.maze)
    def check_event(self):
        ghosts_p = []
        for g in self.ghosts:
            ghosts_p.append(g.position)
        if self.player.position == self.exit_point.exit_pos:
            self.game_state = 'win'
        if self.player.position in ghosts_p and tuple(self.player.position) not in self.safe_zone.safe_zone_list:
            self.game_state = 'lose'


if __name__ == '__main__':
    game = Game(20)
    game.run()



