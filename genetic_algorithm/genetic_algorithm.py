import tkinter as tk
from tkinter import ttk
import numpy as np


# Параметры генетического алгоритма
POPULATION_SIZE = 100
GENERATIONS = 1000
CROSSOVER_RATE = 0.7

# Функция пригодности (минимизация функции Розенброка)
def given_function(individual):
    x1, x2 = individual
    return 100 * (x2 - x1**2)**2 + (1 - x1)**2

# Инициализация популяции с учетом границ
def initialize_population(size, gene_min, gene_max):
    return np.random.rand(size, 2) * (gene_max - gene_min) + gene_min

# Отбор элитных особей
def select_elites(population, fitness_scores, elite_size):
    elite_indices = np.argsort(fitness_scores)[:elite_size]
    return population[elite_indices]

# Кроссовер двух родителей
def crossover(parent1, parent2, crossover_rate):
    if np.random.rand() < crossover_rate:
        return (parent1 + parent2) / 2
    else:
        return parent1

# Мутация особи с учетом границ
def mutate(individual, mutation_rate, gene_min, gene_max):
    if np.random.rand() < mutation_rate:
        individual += np.random.normal(0, 0.1, size=individual.shape)
        individual = np.clip(individual, gene_min, gene_max)
    return individual

# Генетический алгоритм
def genetic_algorithm_mod(population_size, generations, mutation_rate, gene_min, gene_max, elite_size):
    population = initialize_population(population_size, gene_min, gene_max)
    best_solution = None
    best_fitness = float('inf')
    generation_data = []

    for generation in range(generations):
        fitness_scores = np.array([given_function(ind) for ind in population])
        elites = select_elites(population, fitness_scores, elite_size)

        new_population = list(elites)
        while len(new_population) < population_size:
            parent_indices = np.random.choice(len(population), size=2, replace=False)
            parent1, parent2 = population[parent_indices]
            child = crossover(parent1, parent2, CROSSOVER_RATE)
            child = mutate(child, mutation_rate, gene_min, gene_max)
            new_population.append(child)

        population = np.array(new_population)
        current_best_fitness = np.min(fitness_scores)
        current_best_solution = population[np.argmin(fitness_scores)]
        generation_data.append((generation + 1, current_best_fitness, current_best_solution[0], current_best_solution[1]))

        if current_best_fitness < best_fitness:
            best_fitness = current_best_fitness
            best_solution = current_best_solution

    return best_solution, best_fitness, generation_data

# Функция для создания GUI
def create_gui():
    root = tk.Tk()
    root.title("Генетический алгоритм")

    # Лейблы и поля для ввода параметров
    frame_params = tk.Frame(root)
    frame_params.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

    tk.Label(frame_params, text="Функция:").grid(row=0, column=0, sticky="w")
    tk.Label(frame_params, text="100 * (x2 - x1**2)**2 + (1 - x1)**2").grid(row=0, column=1, columnspan=2, sticky="w")

    tk.Label(frame_params, text="Вероятность мутации, %:").grid(row=1, column=0, sticky="w")
    mutation_entry = tk.Entry(frame_params)
    mutation_entry.grid(row=1, column=1, sticky="w")
    mutation_entry.insert(0, "20")

    tk.Label(frame_params, text="Количество хромосом:").grid(row=2, column=0, sticky="w")
    population_entry = tk.Entry(frame_params)
    population_entry.grid(row=2, column=1, sticky="w")
    population_entry.insert(0, "50")

    tk.Label(frame_params, text="Минимальное значение гена:").grid(row=3, column=0, sticky="w")
    gene_min_entry = tk.Entry(frame_params)
    gene_min_entry.grid(row=3, column=1, sticky="w")
    gene_min_entry.insert(0, "-50")

    tk.Label(frame_params, text="Максимальное значение гена:").grid(row=4, column=0, sticky="w")
    gene_max_entry = tk.Entry(frame_params)
    gene_max_entry.grid(row=4, column=1, sticky="w")
    gene_max_entry.insert(0, "50")

    tk.Label(frame_params, text="Количество элитных особей:").grid(row=5, column=0, sticky="w")
    elite_entry = tk.Entry(frame_params)
    elite_entry.grid(row=5, column=1, sticky="w")
    elite_entry.insert(0, "20")

    # Количество поколений
    frame_controls = tk.Frame(root)
    frame_controls.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

    tk.Label(frame_controls, text="Количество поколений:").grid(row=0, column=0, sticky="w")
    generations_entry = tk.Entry(frame_controls, width=10)
    generations_entry.grid(row=0, column=1, sticky="w")
    generations_entry.insert(0, "1000")

    # Кнопки для добавления поколений
    def add_generations(amount):
        current = int(generations_entry.get())
        generations_entry.delete(0, tk.END)
        generations_entry.insert(0, str(current + amount))

    tk.Button(frame_controls, text="+10", command=lambda: add_generations(10)).grid(row=0, column=2, padx=5)
    tk.Button(frame_controls, text="+100", command=lambda: add_generations(100)).grid(row=0, column=3, padx=5)
    tk.Button(frame_controls, text="+1000", command=lambda: add_generations(1000)).grid(row=0, column=4, padx=5)

    # Таблица результатов
    frame_table = tk.Frame(root)
    frame_table.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")

    columns = ("Номер", "Результат", "Ген 1", "Ген 2")
    tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=20)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=100)

    scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both")

    # Результаты
    frame_results = tk.Frame(root)
    frame_results.grid(row=2, column=0, padx=10, pady=10, sticky="nw")

    result_label = tk.Label(frame_results, text="Лучшее решение:")
    result_label.grid(row=0, column=0, sticky="w")
    best_solution_label = tk.Label(frame_results, text="")
    best_solution_label.grid(row=0, column=1, sticky="w")

    fitness_label = tk.Label(frame_results, text="Значение функции:")
    fitness_label.grid(row=1, column=0, sticky="w")
    best_fitness_label = tk.Label(frame_results, text="")
    best_fitness_label.grid(row=1, column=1, sticky="w")

    def calculate_mod():
        mutation_rate = float(mutation_entry.get()) / 100
        population_size = int(population_entry.get())
        gene_min = float(gene_min_entry.get())
        gene_max = float(gene_max_entry.get())
        generations = int(generations_entry.get())
        elite_size = int(elite_entry.get())

        best_solution, best_fitness, generation_data = genetic_algorithm_mod(
            population_size, generations, mutation_rate, gene_min, gene_max, elite_size
        )

        best_solution_label.config(text=f"x1 = {best_solution[0]:.5f}, x2 = {best_solution[1]:.5f}")
        best_fitness_label.config(text=f"{best_fitness:.5f}")
        
        for i in tree.get_children():
            tree.delete(i)

        for generation, fitness, x1, x2 in generation_data:
            tree.insert("", "end", values=(generation, f"{fitness:.5f}", f"{x1:.5f}", f"{x2:.5f}"))

    def calculate_no_mod():
        mutation_rate = float(mutation_entry.get()) / 100
        population_size = int(population_entry.get())
        gene_min = float(gene_min_entry.get())
        gene_max = float(gene_max_entry.get())
        generations = int(generations_entry.get())
        #elite_size = int(elite_entry.get())

        best_solution, best_fitness, generation_data = genetic_algorithm_no_mod(
            population_size, generations, mutation_rate, gene_min, gene_max
        )

        best_solution_label.config(text=f"x1 = {best_solution[0]:.5f}, x2 = {best_solution[1]:.5f}")
        best_fitness_label.config(text=f"{best_fitness:.5f}")
        
        for i in tree.get_children():
            tree.delete(i)

        for generation, fitness, x1, x2 in generation_data:
            tree.insert("", "end", values=(generation, f"{fitness:.5f}", f"{x1:.5f}", f"{x2:.5f}"))
            
    calculate_button_mod = tk.Button(frame_controls, text="Рассчитать", command=calculate_mod)
    calculate_button_mod.grid(row=1, column=0, columnspan=2, pady=10)

    #calculate_button_def = tk.Button(frame_controls, text="Рассчитать без мод", command=calculate_no_mod)
    #calculate_button_def.grid(row=2, column=0, columnspan=2, pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    # Запуск GUI
    create_gui()