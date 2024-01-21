import random
import sympy as sp
import random


def calculate_bits_number(points_number):
    return int(points_number).bit_length()


def calculate_int(individual):
    int_number = 0
    for i in range(len(individual)):
        int_number += int(individual[i]) * (2 ** (len(individual) - i - 1))
    return int_number


def evaluate(func, value):
    x = sp.symbols('x')
    expression = sp.sympify(func)
    result = expression.subs(x, value)
    return result


def calculate_x(a, index, new_resolution):
    return a + (index * new_resolution)


def initialisation(initial_population, bits_number, a, new_resolution, func):
    population = []
    for _ in range(initial_population):
        individual_number = ""
        for _ in range(bits_number):
            individual_number = individual_number + str(random.randint(0, 1))

        index = calculate_int(individual_number)
        x = calculate_x(a, index, new_resolution)
        fx = evaluate(func, x)

        individual = {"number": individual_number, "index": index, "x": x, "f(x)": fx}
        population.append(individual)

    return population


def get_eligible(population, probability):
    return [individual for individual in population if random.random() <= probability]


def generate_pairs(population, crossover_probability):
    eligible_individuals = get_eligible(population, crossover_probability)
    pairs = []

    for individual in eligible_individuals:
        random_index = random.randint(0, len(eligible_individuals) - 1)
        pairs.append((eligible_individuals[random_index], individual))

    return pairs


def crossover(pairs):
    crossover_point = 3
    new_individuals = []

    for pair in pairs:
        new_individual1 = pair[0]["number"][:crossover_point] + pair[1]["number"][crossover_point:]
        new_individual2 = pair[1]["number"][:crossover_point] + pair[0]["number"][crossover_point:]
        new_individuals.extend([new_individual1, new_individual2])
    return new_individuals


def exchange_bits(individual):
    individual_list = list(individual)
    index1 = random.randint(0, len(individual_list) - 1)
    index2 = random.randint(0, len(individual_list) - 1)

    individual_list[index1], individual_list[index2] = individual_list[index2], individual_list[index1]

    mutated_individual = ''.join(individual_list)

    return mutated_individual


def mutation(individuals, individual_mutation_probability):
    for i in range(len(individuals)):
        if random.random() <= individual_mutation_probability:
            individuals[i] = exchange_bits(individuals[i])
    return individuals


def get_statistics(population, minimize):
    key = "f(x)"
    best_individual = min(population, key=lambda x: x[key]) if minimize else max(population, key=lambda x: x[key])
    worst_individual = max(population, key=lambda x: x[key]) if minimize else min(population, key=lambda x: x[key])
    total_fitness = sum(individual[key] for individual in population)
    return {"best": best_individual, "worst": worst_individual, "average": total_fitness / len(population)}


def prunning(population, max_population, minimize):
    temporal_population = []
    for individual in population:
        if individual not in temporal_population:
            temporal_population.append(individual)

    sorted_population = sorted(temporal_population, key=lambda x: x["f(x)"], reverse= not minimize)
    best_individual = sorted_population[0]
    remaining_population = sorted_population[1:]

    while len(remaining_population) > max_population - 1:
        index = random.randint(0, len(remaining_population) - 1)
        if remaining_population[index] != best_individual:
            del remaining_population[index]

    return [best_individual] + remaining_population


def optimize(expression, initial_resolution, generations_number, min_range, max_range, initial_population, max_population,
                      crossover_probability, mutation_probability, minimize):

    range_number = max_range - min_range
    points_number = (range_number / initial_resolution) + 1
    bits_number = calculate_bits_number(points_number)
    resolution = range_number / ((2 ** bits_number) - 1)

    population = initialisation(initial_population, bits_number, min_range, resolution, expression)

    statistics = []
    statistics.append(get_statistics(population, minimize))

    for _ in range(generations_number):
        pairs = generate_pairs(population, crossover_probability)
        new_individuals = crossover(pairs)
        mutated_individuals = mutation(new_individuals, mutation_probability)

        new_individuals = []
        for individual in mutated_individuals:
            index = calculate_int(individual)
            x = calculate_x(min_range, index, resolution)
            fx = evaluate(expression, x)

            new_individuals.append({"number": individual, "index": index, "x": x, "f(x)": fx})

        population.extend(new_individuals)
        statistics.append(get_statistics(population, minimize))
        population = prunning(population, max_population, minimize)
    print(population)

    return statistics, population
