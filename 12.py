import pygame
import random
import time

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
TANK_SPEED = 5
BULLET_SPEED = 10
ENEMY_SPEED = 2
ENEMY_SPAWN_RATE = 30  # Количество кадров до спавна нового противника
POWER_UP_SPAWN_RATE = 500  # Количество кадров до спавна усиления

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Инициализация Pygame и звуков
pygame.init()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("shoot.mp3")
explosion_sound = pygame.mixer.Sound("exp.mp3")
powerup_sound = pygame.mixer.Sound("bonus.mp3")

# Установка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tank Shooter")
clock = pygame.time.Clock()

# Класс для танка
class Tank:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT - 60, 40, 40)
        self.bullets = []
        self.power_ups = []
        self.shoot_delay = 0
        self.bullet_size = 5
        self.max_bullets = 10
        self.power_up_active = None

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.clamp_ip(screen.get_rect())  # Ограничение движения танка в границах экрана

    def shoot(self):
        if len(self.bullets) < self.max_bullets:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.bullet_size)
            self.bullets.append(bullet)
            shoot_sound.play()

    def update(self):
        if self.power_up_active:
            self.power_up_active.update()
            if self.power_up_active.duration <= 0:
                self.power_up_active = None

        # Обновление пуль
        for bullet in self.bullets:
            bullet.update()
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)

# Класс для пуль
class Bullet:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x - size // 2, y - size, size, size)
        self.speed = BULLET_SPEED

    def update(self):
        self.rect.y -= self.speed

# Класс для врагов
class Enemy:
    def __init__(self):
        self.rect = pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40)
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed

# Класс для усилений
class PowerUp:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = random.choice(['slow', 'infinite', 'size'])
        self.duration = 500  # Длительность в кадрах

    def update(self):
        self.rect.y += 2
        self.duration -= 1

# Инициализация объектов
tank = Tank()
enemies = []
power_ups = []
score = 0
enemy_spawn_timer = 0
power_up_spawn_timer = 0

# Основной игровой цикл
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        tank.move(-TANK_SPEED, 0)
    if keys[pygame.K_RIGHT]:
        tank.move(TANK_SPEED, 0)
    if keys[pygame.K_SPACE]:
        tank.shoot()

    # Спавн врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer >= ENEMY_SPAWN_RATE:
        enemies.append(Enemy())
        enemy_spawn_timer = 0

    # Спавн усилений
    power_up_spawn_timer += 1
    if power_up_spawn_timer >= POWER_UP_SPAWN_RATE:
        power_up = PowerUp(random.randint(0, WIDTH - 30), -30)
        power_ups.append(power_up)
        power_up_spawn_timer = 0

    # Обновление объектов
    tank.update()
    for enemy in enemies:
        enemy.update()
        if enemy.rect.y > HEIGHT:
            enemies.remove(enemy)  # Удаляем врагов, которые вышли за пределы экрана
        if enemy.rect.colliderect(tank.rect):
            explosion_sound.play()
            running = False  # Конец игры при столкновении

    for power_up in power_ups:
        power_up.update()
        if power_up.rect.colliderect(tank.rect):
            powerup_sound.play()
            if power_up.type == 'slow':
                ENEMY_SPEED *= 0.5
            elif power_up.type == 'infinite':
                tank.max_bullets = float('inf')  # Бесконечные патроны
            elif power_up.type == 'size':
                tank.bullet_size += 2  # Увеличение размера пули
            power_ups.remove(power_up)

    # Отрисовка объектов
    pygame.draw.rect(screen, GREEN, tank.rect)
    for bullet in tank.bullets:
        pygame.draw.rect(screen, BLUE, bullet.rect)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy.rect)
    for power_up in power_ups:
        pygame.draw.rect(screen, (255, 255, 0), power_up.rect)

    tank.bullets = [bullet for bullet in tank.bullets if bullet.rect.y > 0]  # Удаляем пули, которые вышли за пределы экрана
    for bullet in tank.bullets:
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect):
                explosion_sound.play()
                enemies.remove(enemy)
                tank.bullets.remove(bullet)
                score += 1
                break

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
