import pygame
import sys
from clock import MickeyClock

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")
clock = pygame.time.Clock()

center_x = WIDTH // 2
center_y = HEIGHT // 2 - 50

mickey_clock = MickeyClock(screen, center_x, center_y)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), 180, 4)
    
    for i in range(60):
        angle = i * 6
        x1 = center_x + 165 * pygame.math.Vector2(0, -1).rotate(angle).x
        y1 = center_y + 165 * pygame.math.Vector2(0, -1).rotate(angle).y
        
        if i % 5 == 0:
            x2 = center_x + 150 * pygame.math.Vector2(0, -1).rotate(angle).x
            y2 = center_y + 150 * pygame.math.Vector2(0, -1).rotate(angle).y
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 5)
            
            num_font = pygame.font.Font(None, 30)
            if i == 0:
                num_text = num_font.render("12", True, (0, 0, 0))
                text_x = center_x + 130 * pygame.math.Vector2(0, -1).rotate(angle).x - 15
                text_y = center_y + 130 * pygame.math.Vector2(0, -1).rotate(angle).y - 15
            else:
                num_text = num_font.render(str(i//5), True, (0, 0, 0))
                text_x = center_x + 135 * pygame.math.Vector2(0, -1).rotate(angle).x - 10
                text_y = center_y + 135 * pygame.math.Vector2(0, -1).rotate(angle).y - 10
            screen.blit(num_text, (text_x, text_y))
        else:
            x2 = center_x + 160 * pygame.math.Vector2(0, -1).rotate(angle).x
            y2 = center_y + 160 * pygame.math.Vector2(0, -1).rotate(angle).y
            pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 2)
    
    mickey_clock.update()
    
    font_title = pygame.font.Font(None, 36)
    title_text = font_title.render("Mickey's Clock", True, (0, 0, 255))
    screen.blit(title_text, (center_x - 70, 30))
    
    pygame.display.flip()
    clock.tick(60)