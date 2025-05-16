import pygame
import sys
import numpy as np

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция столкновения тележек")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Параметры тележек
CART_WIDTH = 80
CART_HEIGHT = 50
GROUND_Y = HEIGHT - 100

# Физические параметры
m1 = 2.0  # Масса первой тележки (кг)
m2 = 4.0  # Масса второй тележки (кг)
v1 = 2.0  # Начальная скорость первой тележки (м/с)
v2 = -1.5  # Начальная скорость второй тележки (м/с)
restitution = 0.9  # Коэффициент упругости (1 - абсолютно упругий удар, 0 - абсолютно неупругий)

# Позиции тележек
x1 = 100
x2 = WIDTH - 100 - CART_WIDTH

# Флаг для паузы
paused = False

# Шрифт
font = pygame.font.SysFont('Arial', 16)

def calculate_collision(v1, v2, m1, m2, restitution):
    """Вычисление скоростей после столкновения с учетом упругости"""
    # Скорости после столкновения по формулам для упругого удара
    v1_new = ((m1 - m2 * restitution) * v1 + (m2 * (1 + restitution)) * v2) / (m1 + m2)
    v2_new = ((m1 * (1 + restitution)) * v1 + (m2 - m1 * restitution) * v2) / (m1 + m2)
    return v1_new, v2_new

clock = pygame.time.Clock()

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                # Сброс симуляции
                x1 = 100
                x2 = WIDTH - 100 - CART_WIDTH

    if not paused:
        # Проверка столкновения
        if x1 + CART_WIDTH >= x2:
            v1, v2 = calculate_collision(v1, v2, m1, m2, restitution)

        # Обновление позиций
        x1 += v1
        x2 += v2

        # Проверка границ экрана (чтобы тележки не уезжали)
        if x1 < 0:
            x1 = 0
            v1 = -v1 * restitution
        if x2 > WIDTH - CART_WIDTH:
            x2 = WIDTH - CART_WIDTH
            v2 = -v2 * restitution

    # Отрисовка
    screen.fill(WHITE)

    # Земля
    pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

    # Тележки
    pygame.draw.rect(screen, RED, (x1, GROUND_Y - CART_HEIGHT, CART_WIDTH, CART_HEIGHT))
    pygame.draw.rect(screen, BLUE, (x2, GROUND_Y - CART_HEIGHT, CART_WIDTH, CART_HEIGHT))

    # Колеса
    wheel_radius = 15
    pygame.draw.circle(screen, BLACK, (x1 + 20, GROUND_Y), wheel_radius, 2)
    pygame.draw.circle(screen, BLACK, (x1 + CART_WIDTH - 20, GROUND_Y), wheel_radius, 2)
    pygame.draw.circle(screen, BLACK, (x2 + 20, GROUND_Y), wheel_radius, 2)
    pygame.draw.circle(screen, BLACK, (x2 + CART_WIDTH - 20, GROUND_Y), wheel_radius, 2)

    # Информация
    info_text = [
        f"Красная тележка: масса = {m1} кг, скорость = {v1:.2f} м/с",
        f"Синяя тележка: масса = {m2} кг, скорость = {v2:.2f} м/с",
        "Пробел: пауза, R: сброс"
    ]

    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
