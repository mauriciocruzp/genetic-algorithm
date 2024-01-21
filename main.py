import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from genetic_algorithm import optimize


def plot_graphs(expression, initial_resolution, generations, a, b, initial_population, max_population, crossover_probability,
                  mutation_probability, minimize):
    statistics, population = optimize(expression, initial_resolution, generations, a, b, initial_population, max_population,
                                               crossover_probability,
                                               mutation_probability, minimize)
    statistics = np.array(statistics)

    population = np.array(population)

    for widget in frame_plot.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 4))
    plt.grid(True)
    ax.set_title("Aptitud del fitness")
    ax.set_xlabel("Generación")
    ax.set_ylabel("Fitness")

    generations = generations + 1

    generations = np.arange(0, generations, 1)
    best = np.array([])
    worst = np.array([])
    average = np.array([])

    for i in range(len(statistics)):
        best = np.append(best, statistics[i]["best"]["f(x)"])
        worst = np.append(worst, statistics[i]["worst"]["f(x)"])
        average = np.append(average, statistics[i]["average"])

    ax.plot(generations, best, label="Mejor")
    ax.plot(generations, worst, label="Peor")
    ax.plot(generations, average, label="Promedio")

    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)


    fig, ax = plt.subplots(figsize=(6, 4))
    plt.grid(True)
    ax.set_title("Población final")
    ax.set_xlabel("x")
    ax.set_ylabel("Fitness")

    x = np.array([])
    y = np.array([])

    for i in range(len(population)):
        if a <= population[i]["x"] <= b:
            x = np.append(x, population[i]["x"])
            y = np.append(y, population[i]["f(x)"])

    ax.scatter(x, y, label="Puntos")

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)


window = tk.Tk()
window.title("Algoritmo Genético")
window.geometry("1200x700")
window.resizable(False, False)

parameter_frame = tk.Frame(window)
parameter_frame.pack(side=tk.TOP, padx=10)

frame1 = tk.LabelFrame(parameter_frame, text="Parámetros")
frame1.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

func_label = tk.Label(frame1, text="Funcion:")
func_label.grid(row=0, column=0, sticky="w")
func_entry = tk.Entry(frame1)
func_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

resolution_label = tk.Label(frame1, text="Resolucion inicial:")
resolution_label.grid(row=1, column=0, sticky="w")
resolution_entry = tk.Entry(frame1)
resolution_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

generations_label = tk.Label(frame1, text="Generaciones:")
generations_label.grid(row=2, column=0, sticky="w")
generations_entry = tk.Entry(frame1)
generations_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

interval_a_label = tk.Label(frame1, text="Min. intervalo:")
interval_a_label.grid(row=0, column=2, sticky="w")
interval_a_entry = tk.Entry(frame1)
interval_a_entry.grid(row=0, column=3, padx=10, sticky="w")

interval_b_label = tk.Label(frame1, text="Max. intervalo:")
interval_b_label.grid(row=1, column=2, sticky="w")
interval_b_entry = tk.Entry(frame1)
interval_b_entry.grid(row=1, column=3, padx=10, sticky="w")

initial_population_label = tk.Label(frame1, text="Poblacion inicial:")
initial_population_label.grid(row=2, column=2, sticky="w")
initial_population_entry = tk.Entry(frame1)
initial_population_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

max_population_label = tk.Label(frame1, text="Poblacion maxima:")
max_population_label.grid(row=0, column=4, sticky="w")
max_population_entry = tk.Entry(frame1)
max_population_entry.grid(row=0, column=5, padx=10, pady=10, sticky="w")

crossover_prob_label = tk.Label(frame1, text="Prob. de cruza:")
crossover_prob_label.grid(row=1, column=4, sticky="w")
crossover_prob_entry = tk.Entry(frame1)
crossover_prob_entry.grid(row=1, column=5, padx=10, pady=10, sticky="w")

mutation_prob_label = tk.Label(frame1, text="Prob. de mutación:")
mutation_prob_label.grid(row=2, column=4, sticky="w")
mutation_prob_entry = tk.Entry(frame1)
mutation_prob_entry.grid(row=2, column=5, padx=10, pady=10, sticky="w")

method = tk.StringVar()
method.set("Maximizar")
method_menu = tk.OptionMenu(frame1, method, "Maximizar", "Minimizar")
method_menu.grid(row=0, column=7, padx=10, sticky="w")


def execute():
    func = str(func_entry.get())
    resolution = float(resolution_entry.get())
    generations = int(generations_entry.get())
    a = float(interval_a_entry.get())
    b = float(interval_b_entry.get())
    initial_population = int(initial_population_entry.get())
    max_population = int(max_population_entry.get())
    crossover_probability = float(crossover_prob_entry.get())
    individual_mutation_probability = float(mutation_prob_entry.get())
    minimize = method.get() == "Minimizar"

    plot_graphs(func, resolution, generations, a, b, initial_population, max_population, crossover_probability,
                  individual_mutation_probability, minimize)


execute_button = tk.Button(frame1, text="Ejecutar", command=execute)
execute_button.grid(row=2, column=7, padx=10, pady=10, sticky="w")

right_frame = tk.Frame(window)
right_frame.pack(side=tk.BOTTOM, padx=10)

frame_plot = tk.Frame(right_frame)
frame_plot.pack()

window.mainloop()
