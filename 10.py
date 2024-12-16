import pygame
import random
import math

# Константы
WIDTH, HEIGHT = 800, 600
RACE_RADIUS = 200
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
NUM_CHARACTERS = 5
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
COLOR_NAMES = ["Красный", "Зеленый", "Синий", "Желтый", "Розовый"]
CIRCLE_COLOR = (0, 0, 0)  # Цвет круга
FINISH_LINE_COLOR = (0, 255, 255)  # Новый цвет финишной линии (бирюзовый)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Гонка по кругу")
clock = pygame.time.Clock()

# Класс персонажа
class Character:
    def __init__(self, name, color, color_name):
        self.name = name
        self.color = color
        self.color_name = color_name  # Сохраняем название цвета
        self.angle = 0  # Начальный угол
        self.speed = random.uniform(1, 3)  # Начальная скорость
        self.laps = 0  # Количество кругов

    def update(self):
        # Обновление угла на основе скорости
        self.angle += self.speed / RACE_RADIUS
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
            self.laps += 1
            # Увеличиваем скорость после каждого круга
            self.speed = random.uniform(1, 5)

    def get_position(self):
        # Вычисление координат на круге
        x = CENTER_X + RACE_RADIUS * math.cos(self.angle)
        y = CENTER_Y + RACE_RADIUS * math.sin(self.angle)
        return x, y

# Создание персонажей
characters = [Character(f"Персонаж {i+1}", COLORS[i], COLOR_NAMES[i]) for i in range(NUM_CHARACTERS)]

def main():
    running = True
    winner = None  # Переменная для хранения победителя
    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Рисуем круг
        pygame.draw.circle(screen, CIRCLE_COLOR, (CENTER_X, CENTER_Y), RACE_RADIUS, 2)  # Толщина 2 пикселя

        # Рисуем финишную линию (перпендикулярно окружности на 90 градусов вправо)
        finish_line_start = (CENTER_X + RACE_RADIUS + 20, CENTER_Y)  # Начало черты
        finish_line_end = (CENTER_X + RACE_RADIUS - 20, CENTER_Y)  # Конец черты
        pygame.draw.line(screen, FINISH_LINE_COLOR, finish_line_start, finish_line_end, 5)  # Тонкая линия

        # Обновление персонажей
        for character in characters:
            character.update()
            x, y = character.get_position()
            pygame.draw.circle(screen, character.color, (int(x), int(y)), 10)

            # Отображение номера персонажа и его цвета
            font = pygame.font.Font(None, 24)
            text_surface = font.render(f"{character.name} - Цвет: {character.color_name} - Круги: {character.laps}", True, BLACK)
            screen.blit(text_surface, (20, 20 + characters.index(character) * 30))

            # Проверка на победителя
            if character.laps >= 5 and winner is None:
                winner = character.name
                running = False  # Останавливаем программу

        # Определение текущего лидера
        leader = max(characters, key=lambda c: (c.laps, -c.angle))  # Учитываем угол для определения лидера
        font = pygame.font.Font(None, 36)
        text = font.render(f"Текущий лидер: {leader.name} (Круги: {leader.laps})", True, BLACK)
        screen.blit(text, (20, 20 + NUM_CHARACTERS * 30 + 10))

        # Если есть победитель, выводим его имя
        if winner:
            winner_text = font.render(f"Победитель: {winner}!", True, (0, 255, 0))
            screen.blit(winner_text, (20, 20 + NUM_CHARACTERS * 30 + 50))

        pygame.display.flip()
        clock.tick(FPS)

    # Ожидание перед выходом
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

if __name__ == "__main__":
    main()
