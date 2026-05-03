import pygame
import sys
import math

pygame.init()

# window settings
WIDTH, HEIGHT = 900, 600
TOOLBAR_H = 60
CANVAS_H  = HEIGHT - TOOLBAR_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock  = pygame.time.Clock()

font       = pygame.font.SysFont("Arial", 15)
small_font = pygame.font.SysFont("Arial", 12)

# canvas is a separate surface so old drawings are kept
canvas = pygame.Surface((WIDTH, CANVAS_H))
canvas.fill((255, 255, 255))

# color palette
PALETTE = [
    (0,   0,   0),
    (255, 255, 255),
    (255, 0,   0),
    (0,   200, 0),
    (0,   0,   255),
    (255, 215, 0),
    (255, 140, 0),
    (160, 0,   200),
    (0,   200, 200),
    (200, 100, 50),
    (255, 182, 193),
    (128, 128, 128),
]

#  tools list now includes new shapes 
TOOLS = ["pen", "rect", "square", "circle", "r_tri", "eq_tri", "rhombus", "eraser"]

# state variables
current_color  = (0, 0, 0)
current_tool   = "pen"
brush_size     = 4
drawing        = False
start_pos      = None
preview_canvas = None   # snapshot taken before drawing a shape, used for live preview

#helper: convert screen coords to canvas coords
def canvas_pos(screen_x, screen_y):
    return (screen_x, screen_y - TOOLBAR_H)

#helper: get points for a right triangle
# right angle is at bottom-left, defined by two corners (sx,sy) and (cx,cy)
def right_triangle_points(sx, sy, cx, cy):
    return [(sx, cy), (cx, cy), (sx, sy)]

#helper: get points for an equilateral triangle
# base goes from (sx,cy) to (cx,cy), apex is calculated above the midpoint
def equilateral_triangle_points(sx, sy, cx, cy):
    base_x1 = sx
    base_x2 = cx
    base_y  = cy
    mid_x   = (base_x1 + base_x2) / 2
    base_len = abs(cx - sx)
    # height of equilateral triangle: h = side * sqrt(3)/2
    h = base_len * math.sqrt(3) / 2
    apex_y = base_y - h   # apex is above the base
    return [(base_x1, base_y), (base_x2, base_y), (mid_x, apex_y)]

#helper: get points for a rhombus (diamond shape)
# defined by bounding box from start to current mouse position
def rhombus_points(sx, sy, cx, cy):
    mid_x = (sx + cx) // 2
    mid_y = (sy + cy) // 2
    return [(mid_x, sy), (cx, mid_y), (mid_x, cy), (sx, mid_y)]

#draw a shape preview or commit it to a surface
def draw_shape(surface, tool, sx, sy, cx, cy, color, size, offset_y=0):
    # offset_y shifts drawing down when rendering on screen (not canvas)
    if tool == "rect":
        r = pygame.Rect(min(sx, cx), min(sy, cy) + offset_y,
                        abs(cx - sx), abs(cy - sy))
        pygame.draw.rect(surface, color, r, size)

    elif tool == "square":
        # force equal width and height using the smaller side
        side = min(abs(cx - sx), abs(cy - sy))
        r = pygame.Rect(sx, sy + offset_y, side, side)
        pygame.draw.rect(surface, color, r, size)

    elif tool == "circle":
        if abs(cx - sx) > 1 and abs(cy - sy) > 1:
            pygame.draw.ellipse(surface, color,
                pygame.Rect(min(sx, cx), min(sy, cy) + offset_y,
                            abs(cx - sx), abs(cy - sy)), size)

    elif tool == "r_tri":
        pts = right_triangle_points(sx, sy, cx, cy)
        # apply vertical offset for screen preview
        pts = [(x, y + offset_y) for x, y in pts]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool == "eq_tri":
        pts = equilateral_triangle_points(sx, sy, cx, cy)
        pts = [(x, y + offset_y) for x, y in pts]
        pygame.draw.polygon(surface, color, pts, size)

    elif tool == "rhombus":
        pts = rhombus_points(sx, sy, cx, cy)
        pts = [(x, y + offset_y) for x, y in pts]
        pygame.draw.polygon(surface, color, pts, size)

#draw the toolbar and return rects for buttons we need to detect clicks on
def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_H))

    # draw color palette swatches
    for i, color in enumerate(PALETTE):
        x    = 10 + i * 32
        rect = pygame.Rect(x, 8, 28, 28)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        if color == current_color:
            pygame.draw.rect(screen, (255, 255, 0), rect, 3)

    # draw tool buttons - smaller to fit all on toolbar
    btn_x = 10 + len(PALETTE) * 32 + 6
    btn_w = 62   # width per button
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(btn_x + i * btn_w, 8, btn_w - 2, 28)
        color = (180, 230, 180) if tool == current_tool else (200, 200, 200)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 1)
        label = small_font.render(tool, True, (0, 0, 0))
        screen.blit(label, (rect.x + 4, rect.y + 8))

    # brush size controls (minus and plus buttons)
    size_x      = btn_x + len(TOOLS) * btn_w + 6
    minus_rect  = pygame.Rect(size_x,      14, 22, 22)
    plus_rect   = pygame.Rect(size_x + 56, 14, 22, 22)
    pygame.draw.rect(screen, (200, 200, 200), minus_rect)
    pygame.draw.rect(screen, (200, 200, 200), plus_rect)
    pygame.draw.rect(screen, (0, 0, 0), minus_rect, 1)
    pygame.draw.rect(screen, (0, 0, 0), plus_rect, 1)
    screen.blit(font.render("-", True, (0, 0, 0)), (size_x + 7, 16))
    screen.blit(font.render("+", True, (0, 0, 0)), (size_x + 63, 16))
    screen.blit(font.render(f"S:{brush_size}", True, (0, 0, 0)), (size_x + 25, 20))

    return minus_rect, plus_rect

# set of tools that use click-drag to define a shape
SHAPE_TOOLS = {"rect", "square", "circle", "r_tri", "eq_tri", "rhombus"}

running = True
while running:
    clock.tick(60)

    minus_rect, plus_rect = draw_toolbar()

    # blit canvas below toolbar
    screen.blit(canvas, (0, TOOLBAR_H))

    # live preview while dragging a shape tool
    if drawing and current_tool in SHAPE_TOOLS and start_pos:
        mx, my = pygame.mouse.get_pos()
        cx, cy = canvas_pos(mx, my)
        sx, sy = start_pos
        screen.blit(preview_canvas, (0, TOOLBAR_H))   # restore snapshot first
        draw_shape(screen, current_tool, sx, sy, cx, cy,
                   current_color, brush_size, offset_y=TOOLBAR_H)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            if my < TOOLBAR_H:
                # check palette clicks
                for i, color in enumerate(PALETTE):
                    rect = pygame.Rect(10 + i * 32, 8, 28, 28)
                    if rect.collidepoint(mx, my):
                        current_color = color

                # check tool button clicks
                btn_x = 10 + len(PALETTE) * 32 + 6
                btn_w = 62
                for i, tool in enumerate(TOOLS):
                    rect = pygame.Rect(btn_x + i * btn_w, 8, btn_w - 2, 28)
                    if rect.collidepoint(mx, my):
                        current_tool = tool

                # check brush size buttons
                if minus_rect.collidepoint(mx, my):
                    brush_size = max(1, brush_size - 1)
                if plus_rect.collidepoint(mx, my):
                    brush_size = min(40, brush_size + 1)

            elif my >= TOOLBAR_H:
                # start drawing on canvas
                cx, cy   = canvas_pos(mx, my)
                drawing  = True
                start_pos = (cx, cy)
                preview_canvas = canvas.copy()   # save snapshot for shape preview

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing and current_tool in SHAPE_TOOLS and start_pos:
                mx, my = event.pos
                cx, cy = canvas_pos(mx, my)
                sx, sy = start_pos
                # commit the final shape to the canvas (no offset needed)
                draw_shape(canvas, current_tool, sx, sy, cx, cy,
                           current_color, brush_size, offset_y=0)
            drawing   = False
            start_pos = None

        # freehand drawing: pen and eraser work on mouse drag
        if event.type == pygame.MOUSEMOTION and drawing:
            mx, my = event.pos
            if my >= TOOLBAR_H:
                cx, cy = canvas_pos(mx, my)
                if current_tool == "pen":
                    pygame.draw.circle(canvas, current_color, (cx, cy), brush_size)
                elif current_tool == "eraser":
                    pygame.draw.circle(canvas, (255, 255, 255), (cx, cy), brush_size * 3)

    pygame.display.flip()

pygame.quit()
