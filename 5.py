import numpy as np

import matplotlib.pyplot as plt

num_particles = 100

x = np.zeros(num_particles)
y = np.zeros(num_particles)

velocities = np.random.rand(num_particles, 2) * 2 - 1

time_steps = 100
dt = 0.1

plt.figure()
plt.scatter(x, y, color='blue', label='Initial Position')

for t in range(time_steps):
    x += velocities[:, 0] * dt
    y += velocities[:, 1] * dt
    plt.scatter(x, y, color='red', alpha=0.1)

plt.title('Particle Dispersion from Center')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.show()
