import pygame
import math
import random
import sys

# Инициализация
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Коридор")
clock = pygame.time.Clock()

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

# Настройки игрока
player_x, player_y = 100, 300
player_angle = 0
fov = math.pi / 3  # 60 градусов
move_speed = 3
rotate_speed = 0.05

# Карта коридора (1 - стены, 0 - проход)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
CELL_SIZE = 64

# Генератор случайных текстур
def generate_texture(size=64):
    texture = pygame.Surface((size, size))
    colors = [
        (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        for _ in range(5)
    ]

    # Рисуем узоры на текстуре
    for _ in range(random.randint(5, 15)):
        color = random.choice(colors)
        start = (random.randint(0, size), random.randint(0, size))
        end = (random.randint(0, size), random.randint(0, size))
        pygame.draw.line(texture, color, start, end, random.randint(1, 3))

        # Добавляем случайные фигуры
        if random.random() > 0.7:
            rect = (random.randint(0, size), random.randint(0, size),
                   random.randint(5, 20), random.randint(5, 20))
            pygame.draw.rect(texture, color, rect, random.randint(1, 2))

    return texture

# Создаем текстуры для стен
wall_textures = [generate_texture() for _ in range(3)]

def cast_ray(angle):
    """Бросает луч и возвращает расстояние до стены и тип текстуры"""
    ray_x, ray_y = player_x, player_y
    ray_cos, ray_sin = math.cos(angle), math.sin(angle)

    # Маленькое значение для избежания деления на ноль
    epsilon = 0.00001

    # Проверяем вертикальные стены
    vert_dist = float('inf')
    vert_texture = 0
    vert_tex_x = 0
    if abs(ray_cos) > epsilon:  # Только если луч не вертикальный
        x_sign = 1 if ray_cos > 0 else -1
        for i in range(1000):
            vert_x = (int(ray_x // CELL_SIZE) + (x_sign > 0)) * CELL_SIZE
            vert_y = ray_y + (vert_x - ray_x) * ray_sin / ray_cos

            map_x, map_y = int(vert_x // CELL_SIZE), int(vert_y // CELL_SIZE)
            if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                if MAP[map_y][map_x] == 1:
                    vert_dist = ((vert_x - ray_x) ** 2 + (vert_y - ray_y) ** 2) ** 0.5
                    vert_texture = (map_x + map_y) % len(wall_textures)
                    vert_tex_x = vert_y % CELL_SIZE
                    break
            else:
                break
            ray_x, ray_y = vert_x + x_sign, vert_y

    # Проверяем горизонтальные стены
    horiz_dist = float('inf')
    horiz_texture = 0
    horiz_tex_x = 0
    if abs(ray_sin) > epsilon:  # Только если луч не горизонтальный
        y_sign = 1 if ray_sin > 0 else -1
        for i in range(1000):
            horiz_y = (int(ray_y // CELL_SIZE) + (y_sign > 0)) * CELL_SIZE
            horiz_x = ray_x + (horiz_y - ray_y) * ray_cos / (ray_sin if abs(ray_sin) > epsilon else epsilon)

            map_x, map_y = int(horiz_x // CELL_SIZE), int(horiz_y // CELL_SIZE)
            if 0 <= map_x < MAP_WIDTH and 0 <= map_y < MAP_HEIGHT:
                if MAP[map_y][map_x] == 1:
                    horiz_dist = ((horiz_x - ray_x) ** 2 + (horiz_y - ray_y) ** 2) ** 0.5
                    horiz_texture = (map_x + map_y) % len(wall_textures)
                    horiz_tex_x = horiz_x % CELL_SIZE
                    break
            else:
                break
            ray_x, ray_y = horiz_x, horiz_y + y_sign

    if vert_dist < horiz_dist:
        return vert_dist, vert_texture, vert_tex_x
    else:
        return horiz_dist, horiz_texture, horiz_tex_x

def render():
    """Отрисовка 3D вида"""
    screen.fill(BLACK)

    # Рисуем пол
    pygame.draw.rect(screen, (40, 40, 40), (0, HEIGHT//2, WIDTH, HEIGHT//2))

    # Рисуем потолок
    pygame.draw.rect(screen, (30, 30, 50), (0, 0, WIDTH, HEIGHT//2))

    # Рендерим стены
    for x in range(WIDTH):
        ray_angle = player_angle - fov/2 + (x/WIDTH)*fov
        dist, texture_idx, tex_x = cast_ray(ray_angle)

        if dist == float('inf'):
            continue  # Пропускаем лучи, которые не нашли стену

        # Коррекция искажения
        dist *= math.cos(player_angle - ray_angle)

        # Вычисляем высоту стены
        wall_height = min(int(HEIGHT * CELL_SIZE / (dist + 0.0001)), HEIGHT)

        # Берем текстуру
        texture = wall_textures[texture_idx]
        tex_x = int(tex_x)

        # Вырезаем вертикальную полосу
        wall_slice = texture.subsurface((tex_x, 0, 1, CELL_SIZE))
        wall_slice = pygame.transform.scale(wall_slice, (1, wall_height))

        # Рисуем полосу
        screen.blit(wall_slice, (x, HEIGHT//2 - wall_height//2))

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:  # Новая текстура
                wall_textures = [generate_texture() for _ in range(3)]

    # Управление
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_angle -= rotate_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rotate_speed

    if keys[pygame.K_w]:
        new_x = player_x + math.cos(player_angle) * move_speed
        new_y = player_y + math.sin(player_angle) * move_speed
        if MAP[int(new_y/CELL_SIZE)][int(new_x/CELL_SIZE)] == 0:
            player_x, player_y = new_x, new_y

    if keys[pygame.K_s]:
        new_x = player_x - math.cos(player_angle) * move_speed
        new_y = player_y - math.sin(player_angle) * move_speed
        if MAP[int(new_y/CELL_SIZE)][int(new_x/CELL_SIZE)] == 0:
            player_x, player_y = new_x, new_y

    # Отрисовка
    render()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
