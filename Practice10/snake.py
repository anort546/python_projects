import pygame
import random


pygame.init()

# window and grid settings
CELL  = 20          # size of one grid cell in pixels
COLS  = 30          # number of columns
ROWS  = 25          # number of rows
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + 60   # extra 60px for HUD at the bottom

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()

# colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GREEN      = (0,   200, 50)
DARK_GREEN = (0,   140, 30)
RED        = (220, 50,  50)
YELLOW     = (255, 215, 0)
GRAY       = (40,  40,  40)
WALL_COLOR = (80,  80,  100)

font      = pygame.font.SysFont("Consolas", 22)
big_font  = pygame.font.SysFont("Consolas", 36)

#level settings
# food needed to advance each level (cumulative from level 1)
FOOD_PER_LEVEL = 3      # every 3 foods = new level
BASE_FPS       = 8      # starting speed
FPS_INCREMENT  = 2      # extra frames per level

#game state
def new_game():
    """return a fresh game state dictionary"""
    snake  = [(COLS // 2, ROWS // 2)]   # snake starts in the middle
    direction = (1, 0)                  # moving right
    food   = place_food(snake)
    score  = 0
    level  = 1
    foods_eaten = 0
    fps    = BASE_FPS
    return dict(
        snake=snake, direction=direction,
        food=food, score=score,
        level=level, foods_eaten=foods_eaten,
        fps=fps, alive=True
    )

def place_food(snake):
    """pick a random cell that is not on the snake and not on a wall"""
    while True:
        x = random.randint(1, COLS - 2)    # keep away from border walls
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake:
            return (x, y)

#  drawing helpers
def draw_cell(surface, col, row, color):
    rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)   # thin border between cells

def draw_walls(surface):
    # draw the border wall
    for col in range(COLS):
        draw_cell(surface, col, 0,       WALL_COLOR)
        draw_cell(surface, col, ROWS - 1, WALL_COLOR)
    for row in range(ROWS):
        draw_cell(surface, 0,       row, WALL_COLOR)
        draw_cell(surface, COLS - 1, row, WALL_COLOR)

def draw_hud(surface, state):
    # background strip for HUD
    hud_y = ROWS * CELL
    pygame.draw.rect(surface, GRAY, (0, hud_y, WIDTH, 60))
    score_text = font.render(f"Score: {state['score']}", True, WHITE)
    level_text = font.render(f"Level: {state['level']}", True, YELLOW)
    surface.blit(score_text, (10, hud_y + 18))
    surface.blit(level_text, (WIDTH - level_text.get_width() - 10, hud_y + 18))

#main
state = new_game()
running = True

while running:

    clock.tick(state["fps"])

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            dx, dy = state["direction"]

            # change direction
            if event.key == pygame.K_UP    and dy != 1:
                state["direction"] = (0, -1)
            if event.key == pygame.K_DOWN  and dy != -1:
                state["direction"] = (0, 1)
            if event.key == pygame.K_LEFT  and dx != 1:
                state["direction"] = (-1, 0)
            if event.key == pygame.K_RIGHT and dx != -1:
                state["direction"] = (1, 0)

            # restart after death
            if event.key == pygame.K_r and not state["alive"]:
                state = new_game()

    if state["alive"]:

        #move snake
        head_x, head_y = state["snake"][0]
        dx, dy = state["direction"]
        new_head = (head_x + dx, head_y + dy)

        # check wall collision (borders)
        nx, ny = new_head
        if nx == 0 or nx == COLS - 1 or ny == 0 or ny == ROWS - 1:
            state["alive"] = False

        # check self collision
        elif new_head in state["snake"]:
            state["alive"] = False

        else:
            state["snake"].insert(0, new_head)  # grow head

            # check if food is eaten
            if new_head == state["food"]:
                state["score"] += 10
                state["foods_eaten"] += 1
                state["food"] = place_food(state["snake"])

                #level up logic
                if state["foods_eaten"] % FOOD_PER_LEVEL == 0:
                    state["level"] += 1
                    state["fps"] = BASE_FPS + (state["level"] - 1) * FPS_INCREMENT
            else:
                state["snake"].pop()    # remove tail (no food eaten)

    #drawing
    screen.fill(BLACK)

    # draw grid background
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(screen, c, r, (20, 20, 20))

    draw_walls(screen)

    # draw food
    fx, fy = state["food"]
    draw_cell(screen, fx, fy, RED)

    # draw snake (head slightly different color)
    for i, (sx, sy) in enumerate(state["snake"]):
        color = DARK_GREEN if i == 0 else GREEN
        draw_cell(screen, sx, sy, color)

    draw_hud(screen, state)

    # game over overlay
    if not state["alive"]:
        msg  = big_font.render("GAME OVER", True, RED)
        msg2 = font.render("Press R to restart", True, WHITE)
        screen.blit(msg,  (WIDTH // 2 - msg.get_width()  // 2, ROWS * CELL // 2 - 40))
        screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, ROWS * CELL // 2 + 10))

    pygame.display.flip()

pygame.quit()
