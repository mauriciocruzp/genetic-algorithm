import random
import math


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


def evaluate_function(x):
    return (x ** 3) * (math.sin(x)) + (x ** 2) * (math.cos(x))


def calculate_x(a, index, new_resolution):
    return a + (index * new_resolution)


def generate_initial_population(initial_population, bits_number, a, new_resolution):
    population = []
    for i in range(initial_population):
        individual_number = ""
        for j in range(bits_number):
            individual_number = individual_number + str(random.randint(0, 1))

        index = calculate_index(individual_number)
        x = calculate_x(a, index, new_resolution)
        fx = evaluate_function(x)

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
    crossover_point = 2

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


def get_statistics(population, min):
    best_individual = population[0]
    worst_individual = population[0]
    sum = 0

    for individual in population:
        if min:
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


def prune_population(population, max_population):
    population.sort(key=lambda x: x["f(x)"])
    population = population[:max_population]
    return population


def genetic_algorithm():
    a = -4
    b = 4
    resolution = 0.05
    initial_population = 3

    range_a = b - a
    points = (range_a / resolution) + 1

    min = True
    statistics = []
    statistics_history = []
    generations = 20

    max_population = 6

    bits_number = calculate_bits(points)
    new_resolution = range_a / (2 ** bits_number - 1)
    population = generate_initial_population(initial_population, bits_number, a, new_resolution)
    print(population)
    prev_population = population

    crossover_probability = 0.8
    individual_mutation_probability = 0.7
    gen_mutation_probability = 0.25

    statistics = get_statistics(population, min)
    statistics_history.append(statistics)

    for i in range(generations):
        pairs = select_couple(prev_population, crossover_probability)

        children = crossover_pairs(pairs)

        mutated_children = mutate_children(children, individual_mutation_probability, gen_mutation_probability)

        new_individuals = []
        for individual in mutated_children:
            index = calculate_index(individual)
            x = calculate_x(a, index, new_resolution)
            fx = evaluate_function(x)

            new_individuals.append({"number": individual, "index": index, "x": x, "f(x)": fx})

        new_individuals.extend(prev_population)
        print(new_individuals)

        statistics = get_statistics(new_individuals, min)
        statistics_history.append(statistics)
        prev_population = prune_population(new_individuals, max_population)

    return statistics_history
