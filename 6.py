import pygame
import random

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
NUM_SHIPS = 5

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)  # Цвет для кораблей (скрыт)
RED = (255, 0, 0)   # Цвет для попаданий
GRAY = (200, 200, 200)  # Цвет для ячеек
GREEN = (0, 255, 0)  # Цвет для промахов

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морской бой")

# Функция для создания поля
def create_grid():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Функция для размещения кораблей
def place_ships(grid):
    ships = 0
    while ships < NUM_SHIPS:
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if grid[x][y] == 0:
            grid[x][y] = 1  # 1 обозначает корабль
            ships += 1

# Функция для отрисовки поля
def draw_grid(grid):
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[x][y] == -1:
                pygame.draw.rect(screen, RED, rect)  # Попадание
            elif grid[x][y] == 2:
                pygame.draw.rect(screen, GREEN, rect)  # Промах
            pygame.draw.rect(screen, GRAY, rect, 1)  # Границы ячеек

# Основная функция игры
def main():
    computer_grid = create_grid()
    place_ships(computer_grid)

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(computer_grid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE
                if computer_grid[grid_x][grid_y] == 1:
                    computer_grid[grid_x][grid_y] = -1  # Попадание
                elif computer_grid[grid_x][grid_y] == 0:
                    computer_grid[grid_x][grid_y] = 2  # Промах

        draw_grid(computer_grid)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
