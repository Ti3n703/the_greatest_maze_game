import pygame
class Menu:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = size * 40
        self.font = pygame.font.Font(None, 40)
    
    def draw_start_menu(self):
        self.screen.fill((200, 200, 200))
        text = self.font.render("Nhấn 'S' để bắt đầu", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.size // 2, self.size // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def draw_win_menu(self):
        self.screen.fill((100, 200, 100))
        text_win = self.font.render("Bạn đã thắng!", True, (255, 255, 255))
        text_restart = self.font.render("Nhấn 'R' để chơi lại", True, (255, 255, 255))
        text_win_rect = text_win.get_rect(center=(self.size // 2, self.size // 2 - 40))
        text_restart_rect = text_restart.get_rect(center=(self.size // 2, self.size // 2 + 20))
        self.screen.blit(text_win, text_win_rect)
        self.screen.blit(text_restart, text_restart_rect)
        pygame.display.flip()
    def draw_lose_menu(self):
        self.screen.fill((200, 100, 100))
        text_lose = self.font.render("Bạn đã thua!", True, (255, 255, 255))
        text_restart = self.font.render("Nhấn 'R' để chơi lại", True, (255, 255, 255))
        text_lose_rect = text_lose.get_rect(center=(self.size // 2, self.size // 2 - 40))
        text_restart_rect = text_restart.get_rect(center=(self.size // 2, self.size // 2 + 20))
        self.screen.blit(text_lose, text_lose_rect)
        self.screen.blit(text_restart, text_restart_rect)
        pygame.display.flip() 