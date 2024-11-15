import pygame
import sys

# Настройки игры
WIDTH, HEIGHT = 600, 400
FPS = 60
CELL_SIZE = 40

# Определяем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Определяем лабиринт (1 - стена, 0 - проход)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Определяем начальную позицию игрока
player_pos = [1, 1]

def draw_maze(screen):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_player(screen, pos):
    pygame.draw.circle(screen, GREEN, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Лабиринт")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and maze[player_pos[1] - 1][player_pos[0]] == 0:  # Вверх
            player_pos[1] -= 1
        if keys[pygame.K_s] and maze[player_pos[1] + 1][player_pos[0]] == 0:  # Вниз
            player_pos[1] += 1
        if keys[pygame.K_a] and maze[player_pos[1]][player_pos[0] - 1] == 0:  # Влево
            player_pos[0] -= 1
        if keys[pygame.K_d] and maze[player_pos[1]][player_pos[0] + 1] == 0:  # Вправо
            player_pos[0] += 1

        screen.fill(WHITE)
        draw_maze(screen)
        draw_player(screen, player_pos)

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
