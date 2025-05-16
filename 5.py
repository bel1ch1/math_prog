import pygame
import sys
import math
import numpy as np
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Симуляция столкновения автомобилей")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Параметры автомобилей
CAR_WIDTH = 120
CAR_HEIGHT = 60
WHEEL_RADIUS = 15
GROUND_Y = HEIGHT - 150

# Физические параметры (начальные значения)
m1 = 1500.0  # Масса первого автомобиля (кг)
m2 = 2000.0  # Масса второго автомобиля (кг)
v1 = 20.0    # Начальная скорость первого автомобиля (м/с)
v2 = -15.0   # Начальная скорость второго автомобиля (м/с)
e = 0.8      # Коэффициент восстановления (упругости)
mu = 0.02    # Коэффициент трения
cargo_mass1 = 0.0  # Масса груза в первом автомобиле
cargo_mass2 = 0.0  # Масса груза во втором автомобиле

# Позиции и углы
x1 = 200
x2 = WIDTH - 200 - CAR_WIDTH
y1 = GROUND_Y - CAR_HEIGHT
y2 = GROUND_Y - CAR_HEIGHT
angle1 = 0
angle2 = 0
angular_vel1 = 0
angular_vel2 = 0

# Флаги
paused = False
show_vectors = True
collision_type = "center"  # "center", "offset", "glancing"
damage1 = 0
damage2 = 0

# Шрифты
font = pygame.font.SysFont('Arial', 16)
large_font = pygame.font.SysFont('Arial', 24)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.knob_rect = pygame.Rect(x, y, h, h)
        self.min = min_val
        self.max = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.update_knob()

    def update_knob(self):
        pos = int((self.value - self.min) / (self.max - self.min) * self.rect.width)
        self.knob_rect.x = self.rect.x + pos - self.knob_rect.width // 2

    def draw(self, surface):
        pygame.draw.rect(surface, GRAY, self.rect, border_radius=5)
        pygame.draw.rect(surface, BLUE if not self.dragging else RED, self.knob_rect, border_radius=5)

        # Отображение значения
        value_text = font.render(f"{self.label}: {self.value:.2f}", True, BLACK)
        surface.blit(value_text, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN and self.knob_rect.collidepoint(event.pos):
            self.dragging = True
        elif event.type == MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == MOUSEMOTION and self.dragging:
            # Обновление значения на основе позиции мыши
            rel_x = event.pos[0] - self.rect.x
            rel_x = max(0, min(rel_x, self.rect.width))
            self.value = self.min + (rel_x / self.rect.width) * (self.max - self.min)
            self.update_knob()
            return True
        return False

# Создание слайдеров
sliders = [
    Slider(20, HEIGHT - 120, 200, 20, 500, 3000, m1, "Масса авто 1 (кг)"),
    Slider(20, HEIGHT - 90, 200, 20, 500, 3000, m2, "Масса авто 2 (кг)"),
    Slider(20, HEIGHT - 60, 200, 20, 0, 1000, cargo_mass1, "Груз авто 1 (кг)"),
    Slider(240, HEIGHT - 120, 200, 20, -50, 50, v1, "Скорость авто 1 (м/с)"),
    Slider(240, HEIGHT - 90, 200, 20, -50, 50, v2, "Скорость авто 2 (м/с)"),
    Slider(240, HEIGHT - 60, 200, 20, 0, 1, e, "Коэф. упругости"),
    Slider(460, HEIGHT - 120, 200, 20, 0, 0.2, mu, "Коэф. трения"),
]

def reset_simulation():
    global x1, x2, y1, y2, angle1, angle2, angular_vel1, angular_vel2, v1, v2, damage1, damage2
    x1 = 200
    x2 = WIDTH - 200 - CAR_WIDTH
    y1 = GROUND_Y - CAR_HEIGHT
    y2 = GROUND_Y - CAR_HEIGHT
    angle1 = 0
    angle2 = 0
    angular_vel1 = 0
    angular_vel2 = 0
    damage1 = 0
    damage2 = 0

    # Обновление скоростей из слайдеров
    v1 = sliders[3].value
    v2 = sliders[4].value

def calculate_collision(v1, v2, m1, m2, e, collision_point1=0, collision_point2=0):
    """Расчет столкновения с возможностью учета смещенного удара"""
    global angular_vel1, angular_vel2, damage1, damage2

    # Расчет относительной скорости
    v_rel = v1 - v2

    # Импульс
    J = -(1 + e) * v_rel / (1/m1 + 1/m2)

    # Новые скорости
    v1_new = v1 + J / m1
    v2_new = v2 - J / m2

    # Если удар смещенный, добавляем вращение
    if collision_point1 != 0 or collision_point2 != 0:
        # Момент инерции автомобиля (упрощенно)
        I1 = (1/12) * m1 * (CAR_HEIGHT**2 + CAR_WIDTH**2)
        I2 = (1/12) * m2 * (CAR_HEIGHT**2 + CAR_WIDTH**2)

        # Угловые скорости от удара
        angular_vel1 += (J * collision_point1) / I1
        angular_vel2 += (-J * collision_point2) / I2

        # Расчет повреждений (упрощенно)
        damage1 += abs(J * collision_point1) / 10000
        damage2 += abs(J * collision_point2) / 10000

    return v1_new, v2_new

def draw_car(surface, x, y, angle, color, damage=0):
    """Рисует автомобиль с возможным поворотом и повреждениями"""
    # Создаем поверхность для автомобиля
    car_surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT), pygame.SRCALPHA)

    # Корпус
    pygame.draw.rect(car_surface, color, (0, 0, CAR_WIDTH, CAR_HEIGHT))

    # Окна
    pygame.draw.rect(car_surface, BLACK, (10, 5, CAR_WIDTH-20, 15))
    pygame.draw.rect(car_surface, BLACK, (10, CAR_HEIGHT-20, CAR_WIDTH-20, 15))

    # Повреждения
    if damage > 0:
        damage_color = (min(255, 100 + damage*155), max(0, 100 - damage*100), 0)
        d_w = min(CAR_WIDTH, damage * 30)
        pygame.draw.rect(car_surface, damage_color, (CAR_WIDTH//2 - d_w//2, 0, d_w, CAR_HEIGHT))

    # Поворачиваем автомобиль
    rotated_car = pygame.transform.rotate(car_surface, -angle * 180/math.pi)
    car_rect = rotated_car.get_rect(center=(x + CAR_WIDTH//2, y + CAR_HEIGHT//2))

    # Рисуем на основной поверхности
    surface.blit(rotated_car, car_rect)

    # Колеса (рисуем отдельно, чтобы они не вращались)
    wheel_positions = [
        (x + 20, y + CAR_HEIGHT),
        (x + CAR_WIDTH - 20, y + CAR_HEIGHT),
        (x + 20, y),
        (x + CAR_WIDTH - 20, y)
    ]

    for wx, wy in wheel_positions:
        # Учет поворота для позиции колес
        dx = wx - (x + CAR_WIDTH//2)
        dy = wy - (y + CAR_HEIGHT//2)
        rotated_x = (x + CAR_WIDTH//2) + dx * math.cos(angle) - dy * math.sin(angle)
        rotated_y = (y + CAR_HEIGHT//2) + dx * math.sin(angle) + dy * math.cos(angle)

        pygame.draw.circle(surface, BLACK, (int(rotated_x), int(rotated_y)), WHEEL_RADIUS, 2)

def draw_vector(surface, start, end, color, label=""):
    """Рисует вектор с меткой"""
    pygame.draw.line(surface, color, start, end, 2)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])

    # Стрелка
    arrow_size = 10
    pygame.draw.line(surface, color, end,
                    (end[0] - arrow_size * math.cos(angle - math.pi/6),
                     end[1] - arrow_size * math.sin(angle - math.pi/6)), 2)
    pygame.draw.line(surface, color, end,
                    (end[0] - arrow_size * math.cos(angle + math.pi/6),
                     end[1] - arrow_size * math.sin(angle + math.pi/6)), 2)

    if label:
        text = font.render(label, True, color)
        text_pos = (end[0] + 10, end[1] - 10)
        surface.blit(text, text_pos)

def draw_button(surface, rect, text, color, hover_color, text_color, action=None):
    """Рисует кнопку с возможностью нажатия"""
    mouse_pos = pygame.mouse.get_pos()
    clicked = False

    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(surface, hover_color, rect, border_radius=5)
        if pygame.mouse.get_pressed()[0]:
            clicked = True
    else:
        pygame.draw.rect(surface, color, rect, border_radius=5)

    pygame.draw.rect(surface, BLACK, rect, 2, border_radius=5)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)

    return clicked

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обновление параметров из слайдеров
    m1 = sliders[0].value
    m2 = sliders[1].value
    cargo_mass1 = sliders[2].value
    cargo_mass2 = 0  # Можно добавить слайдер для второго груза
    e = sliders[5].value
    mu = sliders[6].value

    total_m1 = m1 + cargo_mass1
    total_m2 = m2 + cargo_mass2

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Обработка слайдеров
        for slider in sliders:
            slider.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                paused = not paused
            elif event.key == K_v:
                show_vectors = not show_vectors
            elif event.key == K_r:
                reset_simulation()
            elif event.key == K_1:
                collision_type = "center"
                reset_simulation()
            elif event.key == K_2:
                collision_type = "offset"
                reset_simulation()
            elif event.key == K_3:
                collision_type = "glancing"
                reset_simulation()

    # Кнопки
    button_width = 120
    button_height = 30
    button_margin = 10

    buttons = [
        pygame.Rect(WIDTH - button_width - 20, 20, button_width, button_height),
        pygame.Rect(WIDTH - button_width - 20, 60, button_width, button_height),
        pygame.Rect(WIDTH - button_width - 20, 100, button_width, button_height),
        pygame.Rect(WIDTH - button_width - 20, 140, button_width, button_height)
    ]

    # Проверка нажатия кнопок
    if draw_button(screen, buttons[0], "Центральный удар", BLUE, (100, 100, 255), WHITE):
        collision_type = "center"
        reset_simulation()

    if draw_button(screen, buttons[1], "Смещенный удар", BLUE, (100, 100, 255), WHITE):
        collision_type = "offset"
        reset_simulation()

    if draw_button(screen, buttons[2], "Касательный удар", BLUE, (100, 100, 255), WHITE):
        collision_type = "glancing"
        reset_simulation()

    if draw_button(screen, buttons[3], "Сброс", RED, (255, 100, 100), WHITE):
        reset_simulation()

    if not paused:
        # Проверка столкновения
        if x1 + CAR_WIDTH >= x2 and v1 > v2:
            if collision_type == "center":
                # Центральный удар
                v1, v2 = calculate_collision(v1, v2, total_m1, total_m2, e)
            elif collision_type == "offset":
                # Смещенный удар (правый край первого в левый край второго)
                v1, v2 = calculate_collision(v1, v2, total_m1, total_m2, e,
                                            CAR_WIDTH/2, -CAR_WIDTH/2)
            elif collision_type == "glancing":
                # Касательный удар (правый край первого в правый край второго)
                v1, v2 = calculate_collision(v1, v2, total_m1, total_m2, e,
                                            CAR_WIDTH/2, CAR_WIDTH/2)

        # Применение трения
        if abs(v1) > 0.01:
            friction_force1 = mu * total_m1 * 9.81
            v1 -= friction_force1 * (1 if v1 > 0 else -1) / total_m1 * 0.1
        else:
            v1 = 0

        if abs(v2) > 0.01:
            friction_force2 = mu * total_m2 * 9.81
            v2 -= friction_force2 * (1 if v2 > 0 else -1) / total_m2 * 0.1
        else:
            v2 = 0

        # Применение углового трения
        angular_vel1 *= 0.98
        angular_vel2 *= 0.98

        # Обновление позиций и углов
        x1 += v1
        x2 += v2
        angle1 += angular_vel1
        angle2 += angular_vel2

        # Проверка границ
        if x1 < 0:
            x1 = 0
            v1 = -v1 * 0.5
        if x2 > WIDTH - CAR_WIDTH:
            x2 = WIDTH - CAR_WIDTH
            v2 = -v2 * 0.5

    # Отрисовка
    screen.fill(WHITE)

    # Дорога
    pygame.draw.rect(screen, DARK_GRAY, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.line(screen, YELLOW, (0, GROUND_Y + 5), (WIDTH, GROUND_Y + 5), 2)

    # Автомобили
    draw_car(screen, x1, y1, angle1, RED, damage1)
    draw_car(screen, x2, y2, angle2, BLUE, damage2)

    # Векторы
    if show_vectors:
        # Векторы скорости
        draw_vector(screen,
                   (x1 + CAR_WIDTH//2, y1 + CAR_HEIGHT//2),
                   (x1 + CAR_WIDTH//2 + v1 * 5, y1 + CAR_HEIGHT//2),
                   GREEN, f"v1: {v1:.2f} м/с")

        draw_vector(screen,
                   (x2 + CAR_WIDTH//2, y2 + CAR_HEIGHT//2),
                   (x2 + CAR_WIDTH//2 + v2 * 5, y2 + CAR_HEIGHT//2),
                   GREEN, f"v2: {v2:.2f} м/с")

        # Векторы импульса
        draw_vector(screen,
                   (x1 + CAR_WIDTH//2, y1 + CAR_HEIGHT//2 + 30),
                   (x1 + CAR_WIDTH//2 + v1 * total_m1 * 0.02, y1 + CAR_HEIGHT//2 + 30),
                   (255, 0, 255), f"p1: {v1 * total_m1:.1f} кг·м/с")

        draw_vector(screen,
                   (x2 + CAR_WIDTH//2, y2 + CAR_HEIGHT//2 + 30),
                   (x2 + CAR_WIDTH//2 + v2 * total_m2 * 0.02, y2 + CAR_HEIGHT//2 + 30),
                   (255, 0, 255), f"p2: {v2 * total_m2:.1f} кг·м/с")

    # Информация
    info_text = [
        f"Тип столкновения: {'Центральный' if collision_type == 'center' else 'Смещенный' if collision_type == 'offset' else 'Касательный'}",
        f"Суммарный импульс: {v1 * total_m1 + v2 * total_m2:.1f} кг·м/с (сохранение: {'ДА' if abs((v1 * total_m1 + v2 * total_m2) - (sliders[3].value * total_m1 + sliders[4].value * total_m2)) < 0.1 else 'НЕТ'})",
        f"Кинетическая энергия: {0.5 * total_m1 * v1**2 + 0.5 * total_m2 * v2**2:.1f} Дж",
        f"Повреждения: Красный авто: {damage1:.1f}, Синий авто: {damage2:.1f}",
        "Управление: Пробел - пауза, V - векторы, R - сброс, 1/2/3 - типы ударов"
    ]

    for i, text in enumerate(info_text):
        text_surface = font.render(text, True, BLACK)
        screen.blit(text_surface, (10, 10 + i * 20))

    # Слайдеры
    for slider in sliders:
        slider.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
