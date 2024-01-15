import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from algorithm import genetic_algorithm


def execute():
    plot_function(custom_function)


def plot_function(custom_function):
    statistics = genetic_algorithm()
    statistics = np.array(statistics)

    try:
        x_values = np.linspace(-10, 10)
        y_values = [custom_function(x) for x in x_values]

        # Limpia la figura anterior
        for widget in frame_plot.winfo_children():
            widget.destroy()

        # Crea una nueva figura y la muestra en el área designada
        fig, ax = plt.subplots(figsize=(6, 4))
        plt.grid(True)
        ax.set_title("Gráfica de la función")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

        generations = np.arange(0, 21, 1)
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
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    except Exception as e:
        print("Error al graficar la función:", e)


def custom_function(x):
    return x**3 * np.sin(x) + x**2 * np.cos(x)


window = tk.Tk()
window.title("Algoritmo Genético")
window.geometry("1200x700")
window.resizable(False, False)

left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=10)

frame1 = tk.LabelFrame(left_frame, text="Parámetros")
frame1.grid(row=0, column=0, padx=20, pady=30, sticky="ew")

# label_func = tk.Label(left_frame, text="Funcion:")
# label_func.pack(anchor="w")
# entry_func = tk.Entry(left_frame, width=50)
# entry_func.pack(anchor="w")

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

execute_button = tk.Button(frame1, text="Ejecutar", command=execute)
execute_button.grid(row=11, column=0, padx=10, pady=10, sticky="w")

# Sección de la derecha para la gráfica
right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, padx=10)

frame_plot = tk.Frame(right_frame)
frame_plot.pack()

window.mainloop()
