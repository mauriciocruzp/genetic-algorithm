import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from genetic_algorithm import optimize

window = tk.Tk() #ventana principal
window.title("Algoritmo Genético")
window.geometry("1200x700")
window.resizable(False, False)

top_frame = tk.Frame(window) #frame superior, contiene el frame de los parámetros
top_frame.pack(side=tk.TOP, padx=10)

parameters_frame = tk.LabelFrame(top_frame, text="Parámetros") #frame de los parámetros
parameters_frame.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

expression_label = tk.Label(parameters_frame, text="Funcion:")
expression_label.grid(row=0, column=0, sticky="w")
expression_entry = tk.Entry(parameters_frame) # entrada de la función
expression_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

resolution_label = tk.Label(parameters_frame, text="Resolucion inicial:")
resolution_label.grid(row=1, column=0, sticky="w")
resolution_entry = tk.Entry(parameters_frame) # entrada de la resolución
resolution_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

generations_label = tk.Label(parameters_frame, text="Generaciones:")
generations_label.grid(row=2, column=0, sticky="w")
generations_entry = tk.Entry(parameters_frame)  # entrada de las generaciones
generations_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

min_interval_label = tk.Label(parameters_frame, text="Min. intervalo:")
min_interval_label.grid(row=0, column=2, sticky="w")
min_interval_entry = tk.Entry(parameters_frame) # entrada del intervalo mínimo
min_interval_entry.grid(row=0, column=3, padx=10, sticky="w")

max_interval_label = tk.Label(parameters_frame, text="Max. intervalo:")
max_interval_label.grid(row=1, column=2, sticky="w")
max_interval_entry = tk.Entry(parameters_frame) # entrada del intervalo máximo
max_interval_entry.grid(row=1, column=3, padx=10, sticky="w")

initial_population_label = tk.Label(parameters_frame, text="Poblacion inicial:")
initial_population_label.grid(row=2, column=2, sticky="w")
initial_population_entry = tk.Entry(parameters_frame) # entrada de la población inicial
initial_population_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

max_population_label = tk.Label(parameters_frame, text="Poblacion maxima:")
max_population_label.grid(row=0, column=4, sticky="w")
max_population_entry = tk.Entry(parameters_frame) # entrada de la población máxima
max_population_entry.grid(row=0, column=5, padx=10, pady=10, sticky="w")

crossover_prob_label = tk.Label(parameters_frame, text="Prob. de cruza:")
crossover_prob_label.grid(row=1, column=4, sticky="w")
crossover_prob_entry = tk.Entry(parameters_frame) # entrada de la probabilidad de cruza
crossover_prob_entry.grid(row=1, column=5, padx=10, pady=10, sticky="w")

mutation_prob_label = tk.Label(parameters_frame, text="Prob. de mutación:")
mutation_prob_label.grid(row=2, column=4, sticky="w")
mutation_prob_entry = tk.Entry(parameters_frame) # entrada de la probabilidad de mutación
mutation_prob_entry.grid(row=2, column=5, padx=10, pady=10, sticky="w")

maximize = tk.StringVar()
maximize.set("Maximizar")
max_menu = tk.OptionMenu(parameters_frame, maximize, "Maximizar", "Minimizar") # menú de maximizar o minimizar
max_menu.grid(row=0, column=7, padx=10, sticky="w")


def print_graphs(
    expression,
    initial_resolution,
    generations_number,
    max_range,
    min_range,
    initial_population,
    max_population,
    crossover_probability,
    mutation_probability,
    minimize,
): # función que imprime las gráficas
    statistics, population = optimize(
        expression,
        initial_resolution,
        generations_number,
        max_range,
        min_range,
        initial_population,
        max_population,
        crossover_probability,
        mutation_probability,
        minimize,
    ) # se obtienen las estadísticas y la población
    statistics = np.array(statistics) # se convierten a numpy arrays

    population = np.array(population)

    for widget in frame_plot.winfo_children(): # se eliminan los widgets de la gráfica
        widget.destroy()

    # grafica de la aptitud del fitness
    fig, ax = plt.subplots(figsize=(6, 4))
    plt.grid(True)
    ax.set_title("Aptitud del fitness")
    ax.set_xlabel("Generación")
    ax.set_ylabel("Fitness")

    generations_number = generations_number + 1

    generations_number = np.arange(0, generations_number, 1)
    best = np.array([])
    worst = np.array([])
    average = np.array([])

    for i in range(len(statistics)): # se obtienen los mejores, peores y promedios de cada generación
        best = np.append(best, statistics[i]["best"]["f(x)"])
        worst = np.append(worst, statistics[i]["worst"]["f(x)"])
        average = np.append(average, statistics[i]["average"])

    ax.plot(generations_number, best, label="Mejor") # se grafican
    ax.plot(generations_number, worst, label="Peor")
    ax.plot(generations_number, average, label="Promedio")

    ax.legend() # se agrega la leyenda

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # grafica de la población final
    fig, ax = plt.subplots(figsize=(6, 4))
    plt.grid(True)
    ax.set_title("Población final")
    ax.set_xlabel("x")
    ax.set_ylabel("Fitness")

    x = np.array([])
    y = np.array([])

    for i in range(len(population)):
        if max_range <= population[i]["x"] <= min_range:
            x = np.append(x, population[i]["x"])
            y = np.append(y, population[i]["f(x)"])

    ax.scatter(x, y, label="Puntos")

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)


def execute_algorithm():
    expression = str(expression_entry.get()) # se obtienen los parámetros
    initial_resolution = float(resolution_entry.get())
    generations_number = int(generations_entry.get())
    min_range = float(min_interval_entry.get())
    max_range = float(max_interval_entry.get())
    initial_population = int(initial_population_entry.get())
    max_population = int(max_population_entry.get())
    crossover_probability = float(crossover_prob_entry.get())
    individual_mutation_probability = float(mutation_prob_entry.get())
    minimize = maximize.get() == "Minimizar"

    print_graphs(
        expression,
        initial_resolution,
        generations_number,
        min_range,
        max_range,
        initial_population,
        max_population,
        crossover_probability,
        individual_mutation_probability,
        minimize,
    )


execute_button = tk.Button(parameters_frame, text="Ejecutar", command=execute_algorithm) # botón de ejecutar
execute_button.grid(row=2, column=7, padx=10, pady=10, sticky="w")

bottom_frame = tk.Frame(window) # frame inferior, contiene el frame de las gráficas
bottom_frame.pack(side=tk.BOTTOM, padx=10)

frame_plot = tk.Frame(bottom_frame)
frame_plot.pack()

window.mainloop() # se ejecuta la ventana
