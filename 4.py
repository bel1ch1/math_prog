import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt

def plot_function():
    try:
        # Получаем функцию из текстового поля
        func_str = function_entry.get()

        # Создаем массив значений x
        x = np.linspace(-10, 10, 400)

        # Вычисляем значения y на основе введенной функции
        y = eval(func_str)

        # Создаем график
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label=func_str)
        plt.title('График функции')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.grid()
        plt.legend()
        plt.show()

    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось построить график: {e}")

# Создаем основное окно
root = tk.Tk()
root.title("Калькулятор функций")

# Создаем элементы интерфейса
function_label = tk.Label(root, text="Введите функцию (например, np.sin(x)):")
function_label.pack()

function_entry = tk.Entry(root, width=50)
function_entry.pack()

plot_button = tk.Button(root, text="Построить график", command=plot_function)
plot_button.pack()

# Запускаем главный цикл
root.mainloop()
