import pygame
import random

pygame.init()

# window settings
CELL   = 20
COLS   = 30
ROWS   = 25
WIDTH  = COLS * CELL
HEIGHT = ROWS * CELL + 60   # extra 60px for hud at the bottom

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
ORANGE     = (255, 140, 0)
CYAN       = (0,   200, 200)
PURPLE     = (180, 0,   200)
GRAY       = (40,  40,  40)
WALL_COLOR = (80,  80,  100)

font     = pygame.font.SysFont("Consolas", 22)
big_font = pygame.font.SysFont("Consolas", 36)
sm_font  = pygame.font.SysFont("Consolas", 13)

# level settings
FOOD_PER_LEVEL = 3
BASE_FPS       = 8
FPS_INCREMENT  = 2

#food types with different weights and scores
# weight = chance of spawning (higher = more common)
# lifetime = how many frames before it disappears (None = never)
FOOD_TYPES = [
    {"color": RED,    "score": 10, "weight": 50, "lifetime": None},  # normal food, never disappears
    {"color": ORANGE, "score": 20, "weight": 30, "lifetime": 180},   # medium food, disappears after 3 sec
    {"color": CYAN,   "score": 30, "weight": 15, "lifetime": 120},   # rare food, disappears after 2 sec
    {"color": PURPLE, "score": 50, "weight": 5,  "lifetime": 60},    # very rare food, disappears after 1 sec
]

# build weighted pool for food selection
food_pool = []
for i, ft in enumerate(FOOD_TYPES):
    food_pool.extend([i] * ft["weight"])

def new_game():
    snake     = [(COLS // 2, ROWS // 2)]
    direction = (1, 0)
    score     = 0
    level     = 1
    foods_eaten = 0
    fps       = BASE_FPS
    # start with one food item on the board
    foods = [make_food(snake)]
    return dict(
        snake=snake, direction=direction,
        foods=foods, score=score,
        level=level, foods_eaten=foods_eaten,
        fps=fps, alive=True
    )

def make_food(snake):
    # pick a random food type using weighted pool
    ftype_index = random.choice(food_pool)
    ft = FOOD_TYPES[ftype_index]
    # find a free cell not occupied by the snake
    while True:
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if (x, y) not in snake:
            return {
                "pos":      (x, y),
                "color":    ft["color"],
                "score":    ft["score"],
                "lifetime": ft["lifetime"],   # remaining frames, or None
                "max_life": ft["lifetime"],   # keep original for blink effect
            }

def draw_cell(surface, col, row, color):
    rect = pygame.Rect(col * CELL, row * CELL, CELL, CELL)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, BLACK, rect, 1)

def draw_walls(surface):
    for col in range(COLS):
        draw_cell(surface, col, 0,       WALL_COLOR)
        draw_cell(surface, col, ROWS - 1, WALL_COLOR)
    for row in range(ROWS):
        draw_cell(surface, 0,       row, WALL_COLOR)
        draw_cell(surface, COLS - 1, row, WALL_COLOR)

def draw_hud(surface, state):
    hud_y = ROWS * CELL
    pygame.draw.rect(surface, GRAY, (0, hud_y, WIDTH, 60))
    score_text = font.render(f"Score: {state['score']}", True, WHITE)
    level_text = font.render(f"Level: {state['level']}", True, YELLOW)
    surface.blit(score_text, (10, hud_y + 18))
    surface.blit(level_text, (WIDTH - level_text.get_width() - 10, hud_y + 18))

state   = new_game()
running = True

while running:

    clock.tick(state["fps"])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            dx, dy = state["direction"]
            if event.key == pygame.K_UP    and dy != 1:
                state["direction"] = (0, -1)
            if event.key == pygame.K_DOWN  and dy != -1:
                state["direction"] = (0, 1)
            if event.key == pygame.K_LEFT  and dx != 1:
                state["direction"] = (-1, 0)
            if event.key == pygame.K_RIGHT and dx != -1:
                state["direction"] = (1, 0)
            if event.key == pygame.K_r and not state["alive"]:
                state = new_game()
    expired=[]
    if state["alive"]:

        #update food lifetimes and remove expired food
        for food in state["foods"]:
            if food["lifetime"] is not None:
                food["lifetime"] -= 1
                if food["lifetime"] <= 0:
                    expired.append(food)
        for food in expired:
            state["foods"].remove(food)
            # replace expired food with a new one so board never runs out
            state["foods"].append(make_food(state["snake"]))

        # move the snake head one step in current direction
        head_x, head_y = state["snake"][0]
        dx, dy = state["direction"]
        new_head = (head_x + dx, head_y + dy)

        nx, ny = new_head
        # check wall collision
        if nx == 0 or nx == COLS - 1 or ny == 0 or ny == ROWS - 1:
            state["alive"] = False
        # check self collision
        elif new_head in state["snake"]:
            state["alive"] = False
        else:
            state["snake"].insert(0, new_head)

            # check if snake ate any food
            ate = None
            for food in state["foods"]:
                if new_head == food["pos"]:
                    ate = food
                    break

            if ate:
                state["score"]      += ate["score"]
                state["foods_eaten"] += 1
                state["foods"].remove(ate)
                # spawn a new food to replace it
                state["foods"].append(make_food(state["snake"]))

                # level up every FOOD_PER_LEVEL foods eaten
                if state["foods_eaten"] % FOOD_PER_LEVEL == 0:
                    state["level"] += 1
                    state["fps"]    = BASE_FPS + (state["level"] - 1) * FPS_INCREMENT
            else:
                state["snake"].pop()   # no food eaten, remove tail

    #drawing
    screen.fill(BLACK)

    # draw dark grid background
    for r in range(ROWS):
        for c in range(COLS):
            draw_cell(screen, c, r, (20, 20, 20))

    draw_walls(screen)

    # draw all food items
    for food in state["foods"]:
        fx, fy = food["pos"]
        # make food blink when it's about to disappear (last 60 frames)
        visible = True
        if food["lifetime"] is not None and food["lifetime"] < 60:
            # blink every 6 frames
            visible = (food["lifetime"] // 6) % 2 == 0
        if visible:
            draw_cell(screen, fx, fy, food["color"])
            # show score value of the food as a small label
            label = sm_font.render(str(food["score"]), True, WHITE)
            screen.blit(label, (fx * CELL + 2, fy * CELL + 3))

    # draw snake, head is darker green
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
