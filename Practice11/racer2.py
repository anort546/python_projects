import pygame
import random

#set up the window
pygame.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer Game")
clock = pygame.time.Clock()

#colors
WHITE     = (255, 255, 255)
BLACK     = (0,   0,   0)
RED       = (200, 0,   0)
GREEN     = (0,   200, 0)
YELLOW    = (255, 215, 0)
ORANGE    = (255, 140, 0)
CYAN      = (0,   200, 200)
GRAY      = (100, 100, 100)
DARK_GRAY = (50,  50,  50)

font = pygame.font.SysFont("Arial", 24)

#player car starting position and its size
player_x = 160
player_y = 500
player_w = 40
player_h = 60
player_speed = 5

# enemy car settings
enemy_w     = 40
enemy_h     = 60
enemy_speed = 4      # this will increase as player collects coins
enemies     = []
enemy_timer = 0

# how many coins needed to increase enemy speed
SPEED_UP_EVERY = 5

def spawn_enemy():
    # pick a random lane for the enemy car
    lane = random.choice([60, 160, 260])
    return {"x": lane, "y": -enemy_h}

# dashed road lines moving downward to simulate movement
line_y_positions = list(range(0, 600, 80))
road_speed = 4

#coin types with different weights (values)
# each coin type has: color, radius, score value, spawn weight
COIN_TYPES = [
    {"color": YELLOW, "radius": 10, "value": 1,  "weight": 60},  # common small coin
    {"color": ORANGE, "radius": 13, "value": 3,  "weight": 30},  # medium coin
    {"color": CYAN,   "radius": 16, "value": 5,  "weight": 10},  # rare big coin
]

# build a weighted list for random selection
#if weight=60, we add the index 60 times into the pool
coin_pool = []
for i, ct in enumerate(COIN_TYPES):
    coin_pool.extend([i] * ct["weight"])

coins      = []
coin_timer = 0
coin_score = 0   # total coins collected 

def spawn_coin():
    # pick a random coin type using weighted pool
    coin_type_index = random.choice(coin_pool)
    ct   = COIN_TYPES[coin_type_index]
    lane = random.choice([60, 160, 260])
    return {
        "x":      lane + enemy_w // 2,
        "y":      -ct["radius"],
        "type":   coin_type_index,   # store which type it is
        "color":  ct["color"],
        "radius": ct["radius"],
        "value":  ct["value"],
    }

distance  = 0
game_over = False

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # restart after game over
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            enemies.clear()
            coins.clear()
            player_x    = 160
            player_y    = 500
            distance    = 0
            coin_score  = 0
            enemy_speed = 4
            game_over   = False

    if not game_over:

        # player movement with arrow keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]  and player_x > 40:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < 320:
            player_x += player_speed
        if keys[pygame.K_UP]    and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN]  and player_y < 540:
            player_y += player_speed

        # spawn a new enemy every 80 frames
        enemy_timer += 1
        if enemy_timer >= 80:
            enemies.append(spawn_enemy())
            enemy_timer = 0

        # spawn a new coin every 120 frames
        coin_timer += 1
        if coin_timer >= 120:
            coins.append(spawn_coin())
            coin_timer = 0

        # scroll road lines down to create movement effect
        line_y_positions = [(y + road_speed) % 600 for y in line_y_positions]

        # move enemies and check for collision with player
        player_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        for enemy in enemies[:]:
            enemy["y"] += enemy_speed
            enemy_rect = pygame.Rect(enemy["x"], enemy["y"], enemy_w, enemy_h)
            if player_rect.colliderect(enemy_rect):
                game_over = True
            if enemy["y"] > 600:
                enemies.remove(enemy)
                distance += 1   # score goes up when enemy passes

        # move coins and check if player picks them up
        for coin in coins[:]:
            coin["y"] += enemy_speed
            coin_rect = pygame.Rect(
                coin["x"] - coin["radius"], coin["y"] - coin["radius"],
                coin["radius"] * 2,         coin["radius"] * 2
            )
            if player_rect.colliderect(coin_rect):
                coins.remove(coin)
                coin_score += coin["value"]   # add coin value to score

                # every SPEED_UP_EVERY points, enemy speed increases by 1
                if coin_score % SPEED_UP_EVERY == 0:
                    enemy_speed += 1
                    road_speed  += 1   # road lines speed up too for visual feel

            elif coin["y"] > 600:
                coins.remove(coin)

    #drawing

    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, GRAY, (40, 0, 320, 600))   # road surface

    # draw dashed centre lines
    for y in line_y_positions:
        pygame.draw.rect(screen, WHITE, (118, y, 8, 40))
        pygame.draw.rect(screen, WHITE, (198, y, 8, 40))

    # draw coins with their individual color and radius
    for coin in coins:
        pygame.draw.circle(screen, coin["color"], (coin["x"], coin["y"]), coin["radius"])
        # small label showing coin value
        val_text = pygame.font.SysFont("Arial", 11).render(str(coin["value"]), True, BLACK)
        screen.blit(val_text, (coin["x"] - val_text.get_width() // 2,
                               coin["y"] - val_text.get_height() // 2))

    # draw enemy cars as red rectangles
    for enemy in enemies:
        pygame.draw.rect(screen, RED, (enemy["x"], enemy["y"], enemy_w, enemy_h))

    # draw player car as green rectangle
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_w, player_h))

    # hud: distance score top left
    score_text = font.render(f"Score: {distance}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # hud: coin score top right
    coin_text = font.render(f"Coins: {coin_score}", True, YELLOW)
    screen.blit(coin_text, (400 - coin_text.get_width() - 10, 10))

    # hud: current enemy speed (so player can see it increasing)
    spd_text = font.render(f"Spd: {enemy_speed}", True, ORANGE)
    screen.blit(spd_text, (400 - spd_text.get_width() - 10, 38))

    # game over message
    if game_over:
        over_text = font.render("GAME OVER  (R to restart)", True, WHITE)
        screen.blit(over_text, (400 // 2 - over_text.get_width() // 2, 280))

    pygame.display.flip()

pygame.quit()
