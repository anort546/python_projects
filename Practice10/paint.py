import pygame
import sys


pygame.init()


WIDTH, HEIGHT = 900, 600
TOOLBAR_H = 60    # height of the toolbar at the top
CANVAS_H  = HEIGHT - TOOLBAR_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()

font       = pygame.font.SysFont("Arial", 16)
small_font = pygame.font.SysFont("Arial", 13)

#canvas (we draw on this surface so we can keep old drawings) 
canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill((255, 255, 255))    # white background

#color palette
PALETTE = [
    (0,   0,   0),    # black
    (255, 255, 255),  # white
    (255, 0,   0),    # red
    (0,   200, 0),    # green
    (0,   0,   255),  # blue
    (255, 215, 0),    # yellow
    (255, 140, 0),    # orange
    (160, 0,   200),  # purple
    (0,   200, 200),  # cyan
    (200, 100, 50),   # brown
    (255, 182, 193),  # pink
    (128, 128, 128),  # gray
]

#tools
TOOLS = ["pen", "rect", "circle", "eraser"]

#state
current_color  = (0, 0, 0)
current_tool   = "pen"
brush_size     = 4
drawing        = False
start_pos      = None     # used for rect / circle
preview_canvas = None     # snapshot before drawing shape

#helper: draw toolbar
def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_H))

    # palette swatches (12 colors, each 30x30)
    for i, color in enumerate(PALETTE):
        x = 10 + i * 35
        rect = pygame.Rect(x, 10, 30, 30)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        # highlight selected color
        if color == current_color:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)

    # tool buttons
    btn_x = 10 + len(PALETTE) * 35 + 10
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(btn_x + i * 75, 10, 70, 30)
        color = (180, 230, 180) if tool == current_tool else (200, 200, 200)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        label = font.render(tool, True, (0, 0, 0))
        screen.blit(label, (rect.x + 5, rect.y + 7))

    # brush size controls
    size_x = btn_x + len(TOOLS) * 75 + 15
    minus_rect = pygame.Rect(size_x,      12, 26, 26)
    plus_rect  = pygame.Rect(size_x + 60, 12, 26, 26)
    pygame.draw.rect(screen, (200, 200, 200), minus_rect)
    pygame.draw.rect(screen, (200, 200, 200), plus_rect)
    pygame.draw.rect(screen, (0,0,0), minus_rect, 1)
    pygame.draw.rect(screen, (0,0,0), plus_rect, 1)
    screen.blit(font.render("-", True, (0,0,0)), (size_x + 8, 14))
    screen.blit(font.render("+", True, (0,0,0)), (size_x + 68, 14))
    size_label = font.render(f"Size:{brush_size}", True, (0, 0, 0))
    screen.blit(size_label, (size_x + 29, 20))

    return minus_rect, plus_rect    # return rects for click detection

#helper: canvas position from screen position──
def canvas_pos(screen_x, screen_y):
    return (screen_x, screen_y - TOOLBAR_H)

#main loop
running = True
while running:
    clock.tick(60)

    # draw toolbar and get button rects
    minus_rect, plus_rect = draw_toolbar()

    # blit the canvas below the toolbar
    screen.blit(canvas, (0, TOOLBAR_H))

    # show live preview while drawing shapes
    if drawing and current_tool in ("rect", "circle") and start_pos:
        mx, my = pygame.mouse.get_pos()
        cx, cy = canvas_pos(mx, my)
        sx, sy = start_pos
        # blit snapshot first, then draw preview on top
        screen.blit(preview_canvas, (0, TOOLBAR_H))
        if current_tool == "rect":
            r = pygame.Rect(min(sx, cx), min(sy, cy) + TOOLBAR_H,
                            abs(cx - sx), abs(cy - sy))
            pygame.draw.rect(screen, current_color, r, brush_size)
        elif current_tool == "circle":
            center = ((sx + cx) // 2 + 0, (sy + cy) // 2 + TOOLBAR_H)
            rx = abs(cx - sx) // 2
            ry = abs(cy - sy) // 2
            if rx > 1 and ry > 1:
                pygame.draw.ellipse(screen,
                    current_color,
                    pygame.Rect(min(sx, cx), min(sy, cy) + TOOLBAR_H,
                                abs(cx - sx), abs(cy - sy)),
                    brush_size)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        #toolbar clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # click inside toolbar area
            if my < TOOLBAR_H:
                # palette color selection
                for i, color in enumerate(PALETTE):
                    rect = pygame.Rect(10 + i * 35, 10, 30, 30)
                    if rect.collidepoint(mx, my):
                        current_color = color

                # tool selection
                btn_x = 10 + len(PALETTE) * 35 + 10
                for i, tool in enumerate(TOOLS):
                    rect = pygame.Rect(btn_x + i * 75, 10, 70, 30)
                    if rect.collidepoint(mx, my):
                        current_tool = tool

                # brush size
                if minus_rect.collidepoint(mx, my):
                    brush_size = max(1, brush_size - 1)
                if plus_rect.collidepoint(mx, my):
                    brush_size = min(40, brush_size + 1)

            # click inside canvas area
            elif my >= TOOLBAR_H:
                cx, cy = canvas_pos(mx, my)
                drawing = True
                start_pos = (cx, cy)
                # save canvas snapshot for shape preview
                preview_canvas = canvas.copy()

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tool in ("rect", "circle") and start_pos:
                mx, my = event.pos
                cx, cy = canvas_pos(mx, my)
                sx, sy = start_pos
                # commit the shape onto the canvas
                if current_tool == "rect":
                    r = pygame.Rect(min(sx, cx), min(sy, cy),
                                    abs(cx - sx), abs(cy - sy))
                    pygame.draw.rect(canvas, current_color, r, brush_size)
                elif current_tool == "circle":
                    pygame.draw.ellipse(canvas,
                        current_color,
                        pygame.Rect(min(sx, cx), min(sy, cy),
                                    abs(cx - sx), abs(cy - sy)),
                        brush_size)
            drawing   = False
            start_pos = None

        #mouse drag: pen / eraser
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my >= TOOLBAR_H:
                cx, cy = canvas_pos(mx, my)
                if current_tool == "pen":
                    pygame.draw.circle(canvas, current_color, (cx, cy), brush_size)
                elif current_tool == "eraser":
                    # eraser draws white (same as background)
                    pygame.draw.circle(canvas, (255, 255, 255), (cx, cy), brush_size * 3)

    pygame.display.flip()

pygame.quit()
