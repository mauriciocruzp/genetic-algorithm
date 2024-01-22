import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import genetic_algorithm
import sympy as sp
import os
import moviepy.editor as mpy
from natsort import natsorted
from tkvideo import tkvideo

def evaluate_function(func, values):
    x = sp.symbols("x")
    results = np.array([])
    for value in values:
        expression = sp.sympify(func)
        result = expression.subs(x, value)
        results = np.append(results, result)

    return results


def generate_video():
    images = natsorted([os.path.join("graphs", fn) for fn in os.listdir("graphs") if fn.endswith((".png", ".jpg", ".jpeg"))])
    video = mpy.ImageSequenceClip(images, fps=1)
    video.write_videofile("video.mp4")


def plot_function(
    func,
    resolution,
    generations,
    a,
    b,
    initial_population,
    max_population,
    crossover_probability,
    individual_mutation_probability,
    gen_mutation_probability,
    minimize,
):
    statistics, population = genetic_algorithm(
        func,
        resolution,
        generations,
        a,
        b,
        initial_population,
        max_population,
        crossover_probability,
        individual_mutation_probability,
        gen_mutation_probability,
        minimize,
    )
    statistics = np.array(statistics)

    population = np.array(population)

    for widget in frame_plot.winfo_children():
        widget.destroy()

    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.grid(True)
        ax.set_title("Aptitud")
        ax.set_xlabel("Generación")
        ax.set_ylabel("Fitness")

        generations = np.arange(0, generations + 1, 1)
        best = np.array([])
        worst = np.array([])
        average = np.array([])

        for i in range(len(statistics)):
            best = np.append(best, statistics[i]["best"]["f(x)"])
            worst = np.append(worst, statistics[i]["worst"]["f(x)"])
            average = np.append(average, statistics[i]["average"])

        ax.plot(generations, best, label="Mejor", color="blue")
        ax.plot(generations, average, label="Promedio", color="green")
        ax.plot(generations, worst, label="Peor", color="red")

        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        print("Error al graficar la función:", e)

    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.grid(True)
        ax.set_title("Población")
        ax.set_xlabel("x")
        ax.set_ylabel("Fitness")

        x = np.array([])
        y = np.array([])

        max_fitness = max(population, key=lambda x: x["f(x)"])["f(x)"]
        min_fitness = min(population, key=lambda x: x["f(x)"])["f(x)"]

        max_x = np.array([])
        max_y = np.array([])
        min_x = np.array([])
        min_y = np.array([])

        x_graph = np.arange(a, b, 0.01)

        population = sorted(population, key=lambda x: x["x"])

        for i in range(len(population)):
            if a <= population[i]["x"] <= b:
                if population[i]["f(x)"] == max_fitness:
                    max_x = np.append(max_x, population[i]["x"])
                    max_y = np.append(max_y, population[i]["f(x)"])
                elif population[i]["f(x)"] == min_fitness:
                    min_x = np.append(min_x, population[i]["x"])
                    min_y = np.append(min_y, population[i]["f(x)"])
                x = np.append(x, population[i]["x"])
                y = np.append(y, population[i]["f(x)"])

        sin_x = evaluate_function(func, x_graph)

        if minimize:
            ax.scatter(min_x, min_y, label="Mejor individuo", color="blue", zorder=3)
            ax.scatter(x, y, label="Individuos", zorder=2, color="green")
            ax.scatter(max_x, max_y, label="Peor individuo", color="red", zorder=3)
        else:
            ax.scatter(max_x, max_y, label="Mejor individuo", color="blue", zorder=3)
            ax.scatter(x, y, label="Individuos", zorder=2, color="green")
            ax.scatter(min_x, min_y, label="Peor individuo", color="red", zorder=3)
        ax.plot(x_graph, sin_x, color="black", zorder=1)
        ax.set_ylim([float(min_y[0]) - 0.05, float(max_y[0]) + 0.05])
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        print("Error al graficar la población:", e)


window = tk.Tk()
window.title("Algoritmo Genético")
window.geometry("1200x720")
window.resizable(False, False)

left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=10)

frame1 = tk.LabelFrame(left_frame, text="Parámetros")
frame1.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

func_label = tk.Label(frame1, text="Funcion:")
func_label.grid(row=0, column=0, sticky="w")
func_entry = tk.Entry(frame1)
func_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

resolution_label = tk.Label(frame1, text="Resolucion inicial:")
resolution_label.grid(row=1, column=0, sticky="w")
resolution_entry = tk.Entry(frame1)
resolution_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

generations_label = tk.Label(frame1, text="Numero de generaciones:")
generations_label.grid(row=2, column=0, sticky="w")
generations_entry = tk.Entry(frame1)
generations_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

interval_label = tk.Label(frame1, text="Intervalo:")
interval_label.grid(row=3, column=0, sticky="w")

interval_a_entry = tk.Entry(frame1)
interval_a_entry.grid(row=3, column=1, padx=10, sticky="w")

interval_b_entry = tk.Entry(frame1)
interval_b_entry.grid(row=4, column=1, padx=10, sticky="w")

initial_population_label = tk.Label(frame1, text="Poblacion inicial:")
initial_population_label.grid(row=5, column=0, sticky="w")
initial_population_entry = tk.Entry(frame1)
initial_population_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w")

max_population_label = tk.Label(frame1, text="Poblacion maxima:")
max_population_label.grid(row=6, column=0, sticky="w")
max_population_entry = tk.Entry(frame1)
max_population_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w")

crossover_prob_label = tk.Label(frame1, text="Probabilidad de cruza:")
crossover_prob_label.grid(row=7, column=0, sticky="w")
crossover_prob_entry = tk.Entry(frame1)
crossover_prob_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")

mutation_prob_label = tk.Label(frame1, text="Probabilidad de mutación:")
mutation_prob_label.grid(row=8, column=0, sticky="w")
mutation_prob_entry = tk.Entry(frame1)
mutation_prob_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")

mutation_per_gene_prob_label = tk.Label(
    frame1, text="Probabilidad de mutación por Gen:"
)
mutation_per_gene_prob_label.grid(row=9, column=0, sticky="w")
mutation_per_gene_prob_entry = tk.Entry(frame1)
mutation_per_gene_prob_entry.grid(row=9, column=1, padx=10, pady=10, sticky="w")

method_label = tk.Label(frame1, text="Metodo:")
method_label.grid(row=10, column=0, sticky="w")
method = tk.StringVar()
method.set("Minimizar")
method_menu = tk.OptionMenu(frame1, method, "Minimizar", "Maximizar")
method_menu.grid(row=10, column=1, padx=10, sticky="w")


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
    gen_mutation_probability = float(mutation_per_gene_prob_entry.get())
    minimize = method.get() == "Minimizar"

    # func = "sin(x)"
    # resolution = 0.05
    # generations = 20
    # a = -5
    # b = 5
    # initial_population = 4
    # max_population = 10
    # crossover_probability = 0.5
    # individual_mutation_probability = 0.5
    # gen_mutation_probability = 0.5
    # minimize = False

    plot_function(
        func,
        resolution,
        generations,
        a,
        b,
        initial_population,
        max_population,
        crossover_probability,
        individual_mutation_probability,
        gen_mutation_probability,
        minimize,
    )

    generate_video()


execute_button = tk.Button(frame1, text="Ejecutar", command=execute)
execute_button.grid(row=11, column=0, padx=10, pady=10, sticky="w")

right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, padx=10)

frame_plot = tk.Frame(right_frame)
frame_plot.pack()

window.mainloop()
