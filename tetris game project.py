import pygame
import sys
import random

pygame.init()

# Screen and grid
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Colors
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),   
    (0, 0, 255),     
    (255, 165, 0),   
    (255, 255, 0),   
    (0, 255, 0),     
    (128, 0, 128),   
    (255, 0, 0)      
]

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],                         
    [[1, 0, 0], [1, 1, 1]],                 
    [[0, 0, 1], [1, 1, 1]],                 
    [[1, 1], [1, 1]],                       
    [[0, 1, 1], [1, 1, 0]],                 
    [[0, 1, 0], [1, 1, 1]],                 
    [[1, 1, 0], [0, 1, 1]]                  
]

# Game grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = COLORS[grid[y][x] - 1] if grid[y][x] else GRAY
            pygame.draw.rect(screen, color, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x*BLOCK_SIZE, y*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= COLS or y + off_y >= ROWS:
                    return True
                if grid[y + off_y][x + off_x]:
                    return True
    return False

def join_shape(shape, offset, color_id):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                grid[y + off_y][x + off_x] = color_id

def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < ROWS:
        grid.insert(0, [0 for _ in range(COLS)])

def rotate(shape):
    return [list(row) for row in zip(*shape[::-1])]

# Initial piece
current_shape = random.choice(SHAPES)
current_color = SHAPES.index(current_shape) + 1
offset = [COLS // 2 - len(current_shape[0]) // 2, 0]
fall_time = 0
fall_speed = 500  # milliseconds
game_over = False

def new_piece():
    global current_shape, current_color, offset
    current_shape = random.choice(SHAPES)
    current_color = SHAPES.index(current_shape) + 1
    offset = [COLS // 2 - len(current_shape[0]) // 2, 0]
    if check_collision(current_shape, offset):
        return True
    return False

# Game loop
while True:
    screen.fill(BLACK)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_offset = [offset[0] - 1, offset[1]]
                    if not check_collision(current_shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_RIGHT:
                    new_offset = [offset[0] + 1, offset[1]]
                    if not check_collision(current_shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_DOWN:
                    new_offset = [offset[0], offset[1] + 1]
                    if not check_collision(current_shape, new_offset):
                        offset = new_offset
                elif event.key == pygame.K_UP:
                    rotated = rotate(current_shape)
                    if not check_collision(rotated, offset):
                        current_shape = rotated

    if not game_over:
        fall_time += clock.get_rawtime()
        if fall_time > fall_speed:
            fall_time = 0
            new_offset = [offset[0], offset[1] + 1]
            if not check_collision(current_shape, new_offset):
                offset = new_offset
            else:
                join_shape(current_shape, offset, current_color)
                clear_lines()
                game_over = new_piece()

        # Draw current shape
        for y, row in enumerate(current_shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, COLORS[current_color - 1],
                                     ((offset[0] + x) * BLOCK_SIZE, (offset[1] + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(screen, BLACK,
                                     ((offset[0] + x) * BLOCK_SIZE, (offset[1] + y) * BLOCK_SIZE,
                                      BLOCK_SIZE, BLOCK_SIZE), 1)

    if game_over:
        text = font.render("Game Over!", True, (255, 0, 0))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 30))

    pygame.display.update()
    clock.tick(60)
