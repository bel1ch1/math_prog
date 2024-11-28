import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Генерируем рандомные данные
np.random.seed(0)
data = np.random.rand(10, 10)

# Создаем тепловую карту
sns.heatmap(data, annot=False, cmap="YlGnBu", square=True)

# Отображаем график
plt.show()
