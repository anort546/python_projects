import pygame
from datetime import datetime

class MickeyClock:
    def __init__(self, screen, center_x, center_y):
        self.screen = screen
        self.center_x = center_x
        self.center_y = center_y
        
        original = pygame.image.load("images/mickey_hand.png").convert_alpha()
        
        self.minute_hand = pygame.transform.scale(original, (20, 140))
        self.second_hand = pygame.transform.scale(original, (12, 160))
    
    def update(self):
        now = datetime.now()
        minutes = now.minute
        seconds = now.second
        hours = now.hour
        
        minute_angle = minutes * 6
        second_angle = seconds * 6
        
        rotated_minute = pygame.transform.rotate(self.minute_hand, -minute_angle)
        rotated_second = pygame.transform.rotate(self.second_hand, -second_angle)
        
        minute_rect = rotated_minute.get_rect(center=(self.center_x, self.center_y))
        second_rect = rotated_second.get_rect(center=(self.center_x, self.center_y))
        
        self.screen.blit(rotated_minute, minute_rect)
        self.screen.blit(rotated_second, second_rect)
        
        font_big = pygame.font.Font(None, 52)
        time_text = font_big.render(f"{hours:02d}:{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        self.screen.blit(time_text, (self.center_x - 80, self.center_y + 180))