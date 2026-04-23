import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 36)

player = MusicPlayer()

running = True
while running:
    screen.fill((0, 0, 0))

    
    track_text = font.render("Now playing:", True, (255, 255, 255))
    screen.blit(track_text, (50, 80))

    name_text = font.render(player.get_current_track(), True, (0, 255, 0))
    screen.blit(name_text, (50, 120))

   
    seconds = player.get_position()
    time_text = font.render(f"Time: {seconds}s", True, (255, 255, 255))
    screen.blit(time_text, (50, 160))

   
    controls = font.render("P-Play S-Stop N-Next B-Back Q-Quit", True, (255, 255, 255))
    screen.blit(controls, (50, 300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                running = False

    pygame.display.flip()

pygame.quit()