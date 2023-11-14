import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from geopy.distance import geodesic
from pyproj import Proj, transform

cities = {
    "Seattle": (47.608013, -122.335167),
    "Boise": (43.616616, -116.200886),
    "Everett": (47.967306, -122.201399),
    "Pendleton": (45.672075, -118.788597),
    "Biggs": (45.669846, -120.832841),
    "Portland": (45.520247, -122.674194),
    "Twin Falls": (42.570446, -114.460255),
    "Bend": (44.058173, -121.315310),
    "Spokane": (47.657193, -117.423510),
    "Grant Pass": (42.441561, -123.339336),
    "Burns": (43.586126, -119.054413),
    "Eugene": (44.050505, -123.095051),
    "Lakeview": (42.188772, -120.345792),
    "Missoula": (46.870105, -113.995267)
}

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(cities)), len(cities))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def calculate_distance(individual):
    total_distance = 0
    for i in range(len(individual) - 1):
        city1 = cities[list(cities.keys())[individual[i]]]
        city2 = cities[list(cities.keys())[individual[i + 1]]]
        distance = geodesic(city1, city2).kilometers
        total_distance += distance
    return total_distance,

toolbox.register("evaluate", calculate_distance)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / len(cities))
toolbox.register("select", tools.selTournament, tournsize=2)

random.seed(42)

# Create the initial population
population = toolbox.population(n=300)

initial_fitness = [toolbox.evaluate(ind) for ind in population]

best_initial_idx = np.argmin(initial_fitness)
best_initial_individual = population[best_initial_idx]

print("GENERATION 0")
print("******************")
print("INITIAL RANDOM PATH AND DISTANCE:")
print(" ==> ".join([list(cities.keys())[idx] for idx in best_initial_individual]), end=" ==> ")
print(list(cities.keys())[best_initial_individual[0]])
print(f"Fitness value: {initial_fitness[best_initial_idx]}")
print("******************")

hof = tools.HallOfFame(5)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min)
stats.register("avg", np.mean)

# Iterate through generations
for generation in range(200):
    print(f"**GENERATION**: {generation}")
    print("******************")

    fitness_values = [toolbox.evaluate(ind) for ind in population]

    best_idx = np.argmin(fitness_values)
    best_individual = population[best_idx]

    print("Best Path and Distance:")
    print(" ==> ".join([list(cities.keys())[idx] for idx in best_individual]), end=" ==> ")
    print(list(cities.keys())[best_individual[0]])
    print(f"Fitness value: {fitness_values[best_idx]}")
    print("******************")

    pop, _ = algorithms.eaMuPlusLambda(
        population,
        toolbox,
        mu=300,
        lambda_=300,
        cxpb=0.90,
        mutpb=0.1,
        ngen=1,
        stats=None,
        halloffame=hof,
        verbose=False,
    )

    population = pop  # Update the population for the next generation

# After the evolution process is complete, check if the Hall of Fame is not empty
if hof.items:
    best_individual_hof = hof[0]
    best_fitness_hof = toolbox.evaluate(best_individual_hof)

    print("******************")
    print("FINAL PATH AND DISTANCE:")
    print(" ==> ".join([list(cities.keys())[idx] for idx in best_individual_hof]), end=" ==> ")
    print(list(cities.keys())[best_individual_hof[0]])
    print(f"Fitness value: {best_fitness_hof}")
    print("******************")
else:
    print("The Hall of Fame is empty. No best individual found.")



# Hall of Fame para la versión sin elitismo
hof_no_elitism = tools.HallOfFame(5)

# Estadísticas
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)

# Algoritmo genético sin elitismo
random.seed(42)
population_no_elitism = toolbox.population(n=300)
result_no_elitism, log_no_elitism = algorithms.eaSimple(population_no_elitism, toolbox, cxpb=0.90, mutpb=0.1, ngen=200, 
                                                       stats=stats, halloffame=hof_no_elitism, verbose=False)

# Extraer la mejor ruta de la versión sin elitismo
best_route_no_elitism = indices_to_cities(hof_no_elitism[0])




# Hall of Fame para la versión con elitismo
hof_elitism = tools.HallOfFame(30)

# Algoritmo genético con elitismo
random.seed(42)
population_elitism = toolbox.population(n=300)
result_elitism, log_elitism = algorithms.eaSimple(population_elitism, toolbox, cxpb=0.90, mutpb=0.1, ngen=200, 
                                                  stats=stats, halloffame=hof_elitism, verbose=False)

# Extraer la mejor ruta de la versión con elitismo
best_route_elitism = indices_to_cities(hof_elitism[0])
