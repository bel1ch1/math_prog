import pygame
import random

# Константы
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 60
MAX_ATTEMPTS = 20

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)   # Попадание
LIGHT_BLUE = (173, 216, 230)  # Пустые клетки
GRAY = (192, 192, 192)  # Промах

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Морской бой")
clock = pygame.time.Clock()

# Класс для игры
class BattleshipGame:
    def __init__(self):
        self.enemy_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.ships = [2, 3, 3, 4, 5]  # Длина кораблей
        self.attempts = MAX_ATTEMPTS
        self.hits = 0
        self.place_enemy_ships()

    def is_valid_position(self, x, y, ship_length, orientation):
        if orientation == 'h':
            if x + ship_length > GRID_SIZE:
                return False
            for i in range(ship_length):
                if self.enemy_grid[y][x + i] != 0:
                    return False
            # Проверка соседних клеток
            if y > 0 and any(self.enemy_grid[y - 1][x + i] != 0 for i in range(ship_length)):  # Верх
                return False
            if y < GRID_SIZE - 1 and any(self.enemy_grid[y + 1][x + i] != 0 for i in range(ship_length)):  # Низ
                return False
            if x > 0 and self.enemy_grid[y][x - 1] != 0:  # Лево
                return False
            if x + ship_length < GRID_SIZE and self.enemy_grid[y][x + ship_length] != 0:  # Право
                return False
        elif orientation == 'v':
            if y + ship_length > GRID_SIZE:
                return False
            for i in range(ship_length):
                if self.enemy_grid[y + i][x] != 0:
                    return False
            # Проверка соседних клеток
            if x > 0 and any(self.enemy_grid[y + i][x - 1] != 0 for i in range(ship_length)):  # Лево
                return False
            if x < GRID_SIZE - 1 and any(self.enemy_grid[y + i][x + 1] != 0 for i in range(ship_length)):  # Право
                return False
            if y > 0 and self.enemy_grid[y - 1][x] != 0:  # Верх
                return False
            if y + ship_length < GRID_SIZE and self.enemy_grid[y + ship_length][x] != 0:  # Низ
                return False
        return True

    def place_enemy_ships(self):
        for ship in self.ships:
            placed = False
            while not placed:
                orientation = random.choice(['h', 'v'])
                x = random.randint(0, GRID_SIZE - 1)
                y = random.randint(0, GRID_SIZE - 1)

                if self.is_valid_position(x, y, ship, orientation):
                    if orientation == 'h':
                        for i in range(ship):
                            self.enemy_grid[y][x + i] = 1  # Корабль
                    elif orientation == 'v':
                        for i in range(ship):
                            self.enemy_grid[y + i][x] = 1  # Корабль
                    placed = True

    def check_winner(self):
        return self.hits == sum(self.ships)

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

                # Обозначение клеток
                if self.enemy_grid[y][x] == 2:  # Попадание
                    pygame.draw.rect(screen, RED, rect)
                elif self.enemy_grid[y][x] == 3:  # Промах
                    pygame.draw.rect(screen, GRAY, rect)
                elif self.enemy_grid[y][x] == 1:  # Корабль (скрыт)
                    pygame.draw.rect(screen, LIGHT_BLUE, rect)
                else:  # Пустая клетка
                    pygame.draw.rect(screen, LIGHT_BLUE, rect)

                # Рисуем границы клеток
                pygame.draw.rect(screen, WHITE, rect, 1)  # Граница клетки

    def handle_click(self, x, y):
        if self.enemy_grid[y][x] == 0:  # Если клетка не была атакована
            if self.enemy_grid[y][x] == 1:  # Попадание
                self.enemy_grid[y][x] = 2  # Изменяем на 2 для отображения попадания
                self.hits += 1
            else:  # Промах
                self.enemy_grid[y][x] = 3  # Изменяем на 3 для отображения промаха
            self.attempts -= 1

            # Проверка на победителя
            if self.check_winner():
                print("Поздравляем! Вы нашли все корабли!")
                return True  # Игра окончена
            elif self.attempts <= 0:
                print("У вас закончились попытки. Игра окончена!")
                return True  # Игра окончена
        elif self.enemy_grid[y][x] == 1:  # Если попали в корабль
            self.enemy_grid[y][x] = 2  # Закрашиваем клетку красным
            self.hits += 1

        return False  # Игра продолжается

# Основной игровой цикл
def main():
    game = BattleshipGame()
    running = True
    while running:
        screen.fill(WHITE)
        game.draw_grid()

        # Отображение оставшихся попыток
        font = pygame.font.Font(None, 36)
        attempts_text = font.render(f'Осталось попыток: {game.attempts}', True, (0, 0, 0))
        screen.blit(attempts_text, (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # ЛКМ
                    x, y = pygame.mouse.get_pos()
                    grid_x = x // CELL_SIZE
                    grid_y = y // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        if game.handle_click(grid_x, grid_y):
                            running = False  # Игра окончена

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
