import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Глобальные переменные
positions, velocities, best_positions, best_values = None, None, None, None
global_best_position, global_best_value = None, float('inf')
current_iter = 0
num_particles = 30
max_iter = 100
bounds = np.array([-5, 5])
root = None  # Объявляем переменную root глобальной

def rosenbrock_function(x):
    a = 1
    b = 100
    return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

def initialize_swarm():
    global positions, velocities, best_positions, best_values
    positions = np.random.uniform(bounds[0], bounds[1], size=(num_particles, 2))
    velocities = np.random.uniform(-1, 1, size=(num_particles, 2))
    best_positions = np.copy(positions)
    best_values = np.array([float('inf')] * num_particles)

def update_velocity(position, velocity, best_position, global_best_position):
    w = float(w_entry.get())
    c1 = float(c1_entry.get())
    c2 = float(c2_entry.get())
    r1 = np.random.rand(2)
    r2 = np.random.rand(2)
    new_velocity = (w * velocity +
                    c1 * r1 * (best_position - position) +
                    c2 * r2 * (global_best_position - position))
    return new_velocity

def run_pso():
    global current_iter, global_best_position, global_best_value
    current_iter = 0
    global_best_position = np.copy(best_positions[0])
    global_best_value = float('inf')
    animate_pso()

def animate_pso():
    global current_iter, global_best_position, global_best_value
    
    if current_iter < max_iter:
        for i in range(num_particles):
            value = rosenbrock_function(positions[i])

            if value < best_values[i]:
                best_values[i] = value
                best_positions[i] = np.copy(positions[i])

            if value < global_best_value:
                global_best_value = value
                global_best_position = np.copy(positions[i])

            velocities[i] = update_velocity(positions[i], velocities[i], best_positions[i], global_best_position)
            positions[i] += velocities[i]
            positions[i] = np.clip(positions[i], bounds[0], bounds[1])

        # Обновление графика
        ax.clear()
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.scatter(positions[:, 0], positions[:, 1])
        ax.scatter(global_best_position[0], global_best_position[1], color='red')  # Отметка глобального минимума
        iteration_counter.config(text=f"Итерация: {current_iter + 1} / {max_iter}")
        canvas.draw()

        current_iter += 1
        root.after(50, animate_pso)  # Повторить через 50 мс
    else:
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Лучшее положение: {global_best_position}\nЛучшее значение: {global_best_value}\n")

def create_particles():
    global num_particles, max_iter
    num_particles = int(num_particles_entry.get())
    max_iter = int(max_iter_entry.get())
    initialize_swarm()
    ax.clear()
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.scatter(positions[:, 0], positions[:, 1])
    canvas.draw()

def create_gui():
    global w_entry, c1_entry, c2_entry, num_particles_entry, max_iter_entry, result_text, iteration_counter, ax, canvas, root
    
    root = tk.Tk()
    root.title("Particle Swarm Optimization")

    # Ввод коэффициентов
    tk.Label(root, text="Коэффициент текущей скорости (w):").grid(row=0, column=0)
    w_entry = tk.Entry(root)
    w_entry.grid(row=0, column=1)
    w_entry.insert(0, "0.5")

    tk.Label(root, text="Коэффициент собственного лучшего значения (c1):").grid(row=1, column=0)
    c1_entry = tk.Entry(root)
    c1_entry.grid(row=1, column=1)
    c1_entry.insert(0, "1.5")

    tk.Label(root, text="Коэффициент глобального лучшего значения (c2):").grid(row=2, column=0)
    c2_entry = tk.Entry(root)
    c2_entry.grid(row=2, column=1)
    c2_entry.insert(0, "1.5")

    tk.Label(root, text="Количество частиц:").grid(row=3, column=0)
    num_particles_entry = tk.Entry(root)
    num_particles_entry.grid(row=3, column=1)
    num_particles_entry.insert(0, "30")

    tk.Label(root, text="Количество итераций:").grid(row=4, column=0)
    max_iter_entry = tk.Entry(root)
    max_iter_entry.grid(row=4, column=1)
    max_iter_entry.insert(0, "100")

    create_button = tk.Button(root, text="Создать частицы", command=create_particles)
    create_button.grid(row=5, column=0, columnspan=2)

    calculate_button = tk.Button(root, text="Рассчитать", command=run_pso)
    calculate_button.grid(row=6, column=0, columnspan=2)

    result_label = tk.Label(root, text="Результаты:")
    result_label.grid(row=7, column=0, columnspan=2)

    result_text = tk.Text(root, height=5, width=40)
    result_text.grid(row=8, column=0, columnspan=2)

    iteration_counter = tk.Label(root, text="Итерация: 0 / 0")
    iteration_counter.grid(row=9, column=0, columnspan=2)

    # График
    figure, ax = plt.subplots(figsize=(5, 4))
    canvas = FigureCanvasTkAgg(figure, master=root)
    canvas.get_tk_widget().grid(row=0, column=2, rowspan=10)
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)

    root.mainloop()

if __name__ == "__main__":
    # Запуск GUI
    create_gui()
