import pygame
import random

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Простая гонка")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Настройки дороги
road_width = 400
road_x = WIDTH // 2
curves = [0] * 10  # Простые кривые дороги

# Машина игрока
car_width, car_height = 40, 60
car_x = WIDTH // 2
car_y = HEIGHT - 100
car_speed = 0
max_speed = 10
steering = 0

# Игровые переменные
game_over = False
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def generate_curve():
    """Генерирует простые кривые"""
    if random.random() < 0.05:  # 5% chance to change curve
        return random.choice([-3, -2, -1, 0, 1, 2, 3])
    return 0

def draw_road():
    """Рисует дорогу с перспективой"""
    # Горизонт
    pygame.draw.rect(screen, (70, 70, 70), (0, 0, WIDTH, HEIGHT//2))

    # Дорога (трапеция)
    top_width = road_width // 2
    pygame.draw.polygon(screen, GRAY, [
        (road_x - top_width, HEIGHT//2),
        (road_x + top_width, HEIGHT//2),
        (road_x + road_width//2, HEIGHT),
        (road_x - road_width//2, HEIGHT)
    ])

    # Разметка
    pygame.draw.rect(screen, WHITE, (road_x - 5, HEIGHT//2, 10, HEIGHT//2))

def update_game():
    """Обновляет состояние игры"""
    global car_x, road_x, curves, car_speed, game_over

    # Генерация кривых
    curves.pop(0)
    curves.append(generate_curve())

    # Движение дороги
    road_x += sum(curves) // 2

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and car_speed < max_speed:
        car_speed += 0.1
    if keys[pygame.K_DOWN] and car_speed > 0:
        car_speed -= 0.1
    if keys[pygame.K_LEFT]:
        car_x -= 3
    if keys[pygame.K_RIGHT]:
        car_x += 3

    # Проверка выезда за дорогу
    road_left = road_x - road_width//2 + 50
    road_right = road_x + road_width//2 - 50
    if car_x < road_left or car_x + car_width > road_right:
        game_over = True

def draw_car():
    """Рисует машину игрока"""
    pygame.draw.rect(screen, GREEN, (car_x, car_y, car_width, car_height))

def draw_hud():
    """Рисует информацию на экране"""
    speed_text = font.render(f"Скорость: {int(car_speed * 20)}", True, WHITE)
    screen.blit(speed_text, (10, 10))

def draw_game_over():
    """Экран завершения игры"""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    text = font.render("ИГРА ОКОНЧЕНА! Нажмите R", True, RED)
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
            # Сброс игры
            game_over = False
            car_speed = 0
            car_x = WIDTH // 2
            road_x = WIDTH // 2
            curves = [0] * 10

    # Очистка экрана
    screen.fill(BLACK)

    if not game_over:
        update_game()

    # Отрисовка
    draw_road()
    draw_car()
    draw_hud()

    if game_over:
        draw_game_over()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
