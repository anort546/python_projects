import pygame
import random

pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

#define colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (200, 0,   0)
GREEN  = (0,   200, 0)
YELLOW = (255, 215, 0)
GRAY   = (100, 100, 100)
DARK_GRAY = (50, 50, 50)

#displaying text
font = pygame.font.SysFont("Arial", 24)

#player car
player_x = 160
player_y = 500
player_w = 40
player_h = 60
player_speed = 5

#enemy cars
enemy_w = 40
enemy_h = 60
enemy_speed = 4
enemies = []
enemy_timer = 0          # counts frames between spawns

def spawn_enemy():
    # place enemy at a random x position in 3 lanes
    lane = random.choice([60, 160, 260])
    return {"x": lane, "y": -enemy_h}

#road markings
line_y_positions = list(range(0, 600, 80))   # dashed centre lines
road_speed = 4                               # moves at same speed as enemies

#coins 
coins = []
coin_timer = 0
coin_radius = 10
coin_score = 0           # number of collected coins

def spawn_coin():
    #сoins appear in the same 3 lanes as cars
    lane = random.choice([60, 160, 260])
    return {"x": lane + enemy_w // 2, "y": -coin_radius}

#score
distance = 0
game_over = False

#main loop
running = True
while running:

    clock.tick(60)

    #events 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # restart on R when game is over
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            # reset everything
            enemies.clear()
            coins.clear()
            player_x = 160
            distance = 0
            coin_score = 0
            game_over = False

    if not game_over:

        #player movement 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player_x > 40:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 320:
            player_x += player_speed
        if keys[pygame.K_UP]    and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN]  and player_y < 540:
            player_y += player_speed

        #spawn enemies every 80 frames
        enemy_timer += 1
        if enemy_timer >= 80:
            enemies.append(spawn_enemy())
            enemy_timer = 0

        # spawn coins randomly every 120 frames
        coin_timer += 1
        if coin_timer >= 120:
            coins.append(spawn_coin())
            coin_timer = 0

        #move road lines 
        line_y_positions = [(y + road_speed) % 600 for y in line_y_positions]

        #move and check enemies
        for enemy in enemies[:]:
            enemy["y"] += enemy_speed
            # check collision with player
            player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
            enemy_rect  = pygame.Rect(enemy["x"], enemy["y"], enemy_w, enemy_h)
            if player_rect.colliderect(enemy_rect):
                game_over = True
            # remove enemy when it goes off screen
            if enemy["y"] > 600:
                enemies.remove(enemy)
                distance += 1        # increase distance score

        #move and collect coins
        for coin in coins[:]:
            coin["y"] += enemy_speed
            # check if player picks up the coin
            player_rect  = pygame.Rect(player_x, player_y, player_w, player_h)
            coin_rect    = pygame.Rect(
                coin["x"] - coin_radius, coin["y"] - coin_radius,
                coin_radius * 2,         coin_radius * 2
            )
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                coin_score += 1
            elif coin["y"] > 600:
                coins.remove(coin)

    

    # road background
    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, GRAY, (40, 0, 320, 600))   # road surface

    # dashed white centre lines
    for y in line_y_positions:
        pygame.draw.rect(screen, WHITE, (118, y, 8, 40))
        pygame.draw.rect(screen, WHITE, (198, y, 8, 40))

    # draw coins as yellow circles
    for coin in coins:
        pygame.draw.circle(screen, YELLOW, (coin["x"], coin["y"]), coin_radius)

    # draw enemy cars
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_w, enemy_h))

    # draw player car
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_w, player_h))

    #distance score (top left) 
    score_text = font.render(f"Score: {distance}", True, WHITE)
    screen.blit(score_text, (10, 10))

    #coin counter (top right)
    coin_text = font.render(f"Coins: {coin_score}", True, YELLOW)
    screen.blit(coin_text, (400 - coin_text.get_width() - 10, 10))

    #game over message
    if game_over:
        over_text = font.render("GAME OVER  (R to restart)", True, WHITE)
        screen.blit(over_text, (400 // 2 - over_text.get_width() // 2, 280))

    pygame.display.flip()

pygame.quit()
