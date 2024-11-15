import numpy as np
import matplotlib.pyplot as plt

# Параметры спирали
num_points = 1000  # Количество точек
theta = np.linspace(0, 4 * np.pi, num_points)  # Угол
r = theta  # Радиус (линейная спираль)

# Координаты точек
x = r * np.cos(theta)
y = r * np.sin(theta)

# Создание графика
plt.figure(figsize=(8, 8))
plt.plot(x, y, color='blue')
plt.title('Спираль')
plt.xlabel('X')
plt.ylabel('Y')
plt.axis('equal')  # Сохранение пропорций
plt.grid()
plt.show()
