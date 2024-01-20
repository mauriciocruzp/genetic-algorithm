import random
import sympy as sp


def calculate_bits(points):
    bits = 0
    while 2 ** bits <= points:
        bits += 1
    return bits


def calculate_index(individual):
    index = 0
    for i in range(len(individual)):
        index += int(individual[i]) * (2 ** (len(individual) - i - 1))
    return index


def evaluate_function(func, value):
    x = sp.symbols('x')

    try:
        expression = sp.sympify(func)

        result = expression.subs(x, value)
        return result
    except sp.SympifyError:
        print("Error al analizar la expresión.")


def calculate_x(a, index, new_resolution):
    return a + (index * new_resolution)


def generate_initial_population(initial_population, bits_number, a, new_resolution, func):
    population = []
    for i in range(initial_population):
        individual_number = ""
        for j in range(bits_number):
            individual_number = individual_number + str(random.randint(0, 1))

        index = calculate_index(individual_number)
        x = calculate_x(a, index, new_resolution)
        fx = evaluate_function(func, x)

        individual = {"number": individual_number, "index": index, "x": x, "f(x)": fx}
        population.append(individual)

    return population


def get_eligible(population, probability):
    eligible = []
    for i in range(population.__len__()):
        if random.random() <= probability:
            eligible.append(population[i])
    return eligible


def select_couple(population, crossover_probability):
    eligible_individuals = get_eligible(population, crossover_probability)
    pairs = []

    for individual in eligible_individuals:
        random_index = random.randint(0, len(eligible_individuals) - 1)
        pairs.append((eligible_individuals[random_index], individual))

    return pairs


def crossover(individual1, individual2):
    crossover_point = 3

    individual1 = individual1["number"]
    individual2 = individual2["number"]
    new_individual1 = individual1[:crossover_point] + individual2[crossover_point:]
    new_individual2 = individual2[:crossover_point] + individual1[crossover_point:]
    return [new_individual1, new_individual2]


def crossover_pairs(pairs):
    new_individuals = []

    for pair in pairs:
        childs = crossover(pair[0], pair[1])
        new_individuals.extend(childs)
    return new_individuals


def mutate_gen(child, gen_mutation_probability):
    for i in range(len(child)):
        random_flag = random.random()
        if random_flag <= gen_mutation_probability:
            child = child[:i] + str(1 - int(child[i])) + child[i + 1:]
    return child


def mutate_children(children, individual_mutation_probability, gen_mutation_probability):
    for i in range(len(children)):
        if random.random() <= individual_mutation_probability:
            mutated_child = mutate_gen(children[i], gen_mutation_probability)
            children[i] = mutated_child
    return children


def get_statistics(population, minimize):
    best_individual = population[0]
    worst_individual = population[0]
    sum = 0

    for individual in population:
        if minimize:
            if individual["f(x)"] < best_individual["f(x)"]:
                best_individual = individual
            if individual["f(x)"] > worst_individual["f(x)"]:
                worst_individual = individual
        else:
            if individual["f(x)"] > best_individual["f(x)"]:
                best_individual = individual
            if individual["f(x)"] < worst_individual["f(x)"]:
                worst_individual = individual

        sum += individual["f(x)"]

    return {"best": best_individual, "worst": worst_individual, "average": sum / len(population)}


def prune_population(population, max_population, minimize):
    temporal_population = []
    for individual in population:
        if individual not in temporal_population:
            temporal_population.append(individual)

    if minimize:
        temporal_population.sort(key=lambda x: x["f(x)"])
    else:
        temporal_population.sort(key=lambda x: x["f(x)"], reverse=True)

    population = temporal_population[:max_population]
    return population


def genetic_algorithm(func, initial_resolution, generations, a, b, initial_population, max_population,
                      crossover_probability, individual_mutation_probability, gen_mutation_probability, minimize):

    range_a = b - a
    points = (range_a / initial_resolution) + 1

    bits_number = calculate_bits(points)
    new_resolution = range_a / (2 ** bits_number - 1)
    statistics_history = []

    population = generate_initial_population(initial_population, bits_number, a, new_resolution, func)
    print(population)

    statistics = get_statistics(population, minimize)
    statistics_history.append(statistics)

    for i in range(generations):
        pairs = select_couple(population, crossover_probability)

        children = crossover_pairs(pairs)

        mutated_children = mutate_children(children, individual_mutation_probability, gen_mutation_probability)

        new_individuals = []
        for individual in mutated_children:
            index = calculate_index(individual)
            x = calculate_x(a, index, new_resolution)
            fx = evaluate_function(func, x)

            new_individuals.append({"number": individual, "index": index, "x": x, "f(x)": fx})

        new_individuals.extend(population)

        statistics = get_statistics(new_individuals, minimize)
        statistics_history.append(statistics)
        population = prune_population(new_individuals, max_population, minimize)
    print(population)

    return statistics_history, population
