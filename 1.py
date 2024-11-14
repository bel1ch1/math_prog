import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 20
BRICK_ROWS, BRICK_COLS = 5, 10

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Арканоид ZV(типо Звонков)")

# Класс для мяча
class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x <= 0 or self.rect.x >= WIDTH - BALL_RADIUS * 2:
            self.speed_x *= -1
        if self.rect.y <= 0:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([-4, 4])
        self.speed_y = -4

# Класс для ракетки
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dx):
        self.rect.x += dx
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > WIDTH - PADDLE_WIDTH:
            self.rect.x = WIDTH - PADDLE_WIDTH

# Класс для кирпичей
class Brick:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hit = False

# Основная игра
def main():
    clock = pygame.time.Clock()
    ball = Ball()
    paddle = Paddle()
    bricks = [Brick(x * BRICK_WIDTH, y * BRICK_HEIGHT + 50) for y in range(BRICK_ROWS) for x in range(BRICK_COLS)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-5)
        if keys[pygame.K_RIGHT]:
            paddle.move(5)

        ball.move()

        # Проверка столкновений
        if ball.rect.colliderect(paddle.rect):
            ball.speed_y *= -1
            ball.rect.bottom = paddle.rect.top

        for brick in bricks:
            if not brick.hit and ball.rect.colliderect(brick.rect):
                ball.speed_y *= -1
                brick.hit = True

        # Проверка падения мяча
        if ball.rect.y >= HEIGHT:
            ball.reset()

        # Отрисовка
        screen.fill(BLACK)
        pygame.draw.ellipse(screen, WHITE, ball.rect)
        pygame.draw.rect(screen, BLUE, paddle.rect)

        for brick in bricks:
            if not brick.hit:
                pygame.draw.rect(screen, RED, brick.rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
