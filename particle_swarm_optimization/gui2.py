import numpy as np
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PSOApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Particle Swarm Optimization")
        
        # Ввод коэффициентов
        tk.Label(master, text="Коэффициент текущей скорости (w):").grid(row=0, column=0)
        self.w_entry = tk.Entry(master)
        self.w_entry.grid(row=0, column=1)
        self.w_entry.insert(0, "0.5")

        tk.Label(master, text="Коэффициент собственного лучшего значения (c1):").grid(row=1, column=0)
        self.c1_entry = tk.Entry(master)
        self.c1_entry.grid(row=1, column=1)
        self.c1_entry.insert(0, "1.5")

        tk.Label(master, text="Коэффициент глобального лучшего значения (c2):").grid(row=2, column=0)
        self.c2_entry = tk.Entry(master)
        self.c2_entry.grid(row=2, column=1)
        self.c2_entry.insert(0, "1.5")

        tk.Label(master, text="Количество частиц:").grid(row=3, column=0)
        self.num_particles_entry = tk.Entry(master)
        self.num_particles_entry.grid(row=3, column=1)
        self.num_particles_entry.insert(0, "30")

        tk.Label(master, text="Количество итераций:").grid(row=4, column=0)
        self.max_iter_entry = tk.Entry(master)
        self.max_iter_entry.grid(row=4, column=1)
        self.max_iter_entry.insert(0, "100")

        self.create_button = tk.Button(master, text="Создать частицы", command=self.create_particles)
        self.create_button.grid(row=5, column=0, columnspan=2)

        self.calculate_button = tk.Button(master, text="Рассчитать", command=self.run_pso)
        self.calculate_button.grid(row=6, column=0, columnspan=2)

        self.result_label = tk.Label(master, text="Результаты:")
        self.result_label.grid(row=7, column=0, columnspan=2)

        self.result_text = tk.Text(master, height=5, width=40)
        self.result_text.grid(row=8, column=0, columnspan=2)

        # График
        self.figure, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.canvas.get_tk_widget().grid(row=0, column=2, rowspan=9)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

    def create_particles(self):
        self.bounds = np.array([-5, 5])
        self.num_particles = int(self.num_particles_entry.get())
        self.max_iter = int(self.max_iter_entry.get())
        self.positions, self.velocities, self.best_positions, self.best_values = self.initialize_swarm()
        self.global_best_position = np.copy(self.best_positions[0])
        self.global_best_value = float('inf')
        self.current_iter = 0  # Начальная итерация
        self.ax.clear()
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.scatter(self.positions[:, 0], self.positions[:, 1])
        self.canvas.draw()

    def initialize_swarm(self):
        positions = np.random.uniform(self.bounds[0], self.bounds[1], size=(self.num_particles, 2))
        velocities = np.random.uniform(-1, 1, size=(self.num_particles, 2))
        best_positions = np.copy(positions)
        best_values = np.array([float('inf')] * self.num_particles)
        return positions, velocities, best_positions, best_values

    def rosenbrock_function(self, x):
        a = 1
        b = 100
        return (a - x[0])**2 + b * (x[1] - x[0]**2)**2

    def update_velocity(self, position, velocity, best_position, global_best_position):
        w = float(self.w_entry.get())
        c1 = float(self.c1_entry.get())
        c2 = float(self.c2_entry.get())
        r1 = np.random.rand(2)
        r2 = np.random.rand(2)
        new_velocity = (w * velocity +
                        c1 * r1 * (best_position - position) +
                        c2 * r2 * (global_best_position - position))
        return new_velocity

    def run_pso(self):
        self.current_iter = 0  # Сброс текущей итерации
        self.global_best_position = np.copy(self.best_positions[0])
        self.global_best_value = float('inf')
        self.animate_pso()

    def animate_pso(self):
        if self.current_iter < self.max_iter:
            for i in range(self.num_particles):
                value = self.rosenbrock_function(self.positions[i])

                if value < self.best_values[i]:
                    self.best_values[i] = value
                    self.best_positions[i] = np.copy(self.positions[i])

                if value < self.global_best_value:
                    self.global_best_value = value
                    self.global_best_position = np.copy(self.positions[i])

                self.velocities[i] = self.update_velocity(self.positions[i], self.velocities[i], self.best_positions[i], self.global_best_position)
                self.positions[i] += self.velocities[i]
                self.positions[i] = np.clip(self.positions[i], self.bounds[0], self.bounds[1])

            # Обновление графика
            self.ax.clear()
            self.ax.set_xlim(-5, 5)
            self.ax.set_ylim(-5, 5)
            self.ax.scatter(self.positions[:, 0], self.positions[:, 1])
            self.ax.scatter(self.global_best_position[0], self.global_best_position[1], color='red')  # Отметка глобального минимума
            self.canvas.draw()

            self.current_iter += 1
            self.master.after(100, self.animate_pso)  # Повторить через 100 мс
        else:
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Лучшее положение: {self.global_best_position}\nЛучшее значение: {self.global_best_value}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = PSOApp(root)
    root.mainloop()
