import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from eaSimple import eaSimpleWithLogbook
# Ciudades y sus coordenadas (latitud, longitud)
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

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

# Lista de nombres de ciudades
city_names = list(cities.keys())

def distance(city1, city2):
    # Convertir la distancia a kilómetros (asumiendo que las coordenadas están en grados)
    # El factor de 111.32 es una aproximación de cuántos km hay en un grado
    lat1, lon1 = city1
    lat2, lon2 = city2
    return 111.32 * np.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2)

def evaluate(individual):
    # Mapear los índices numéricos a los nombres de las ciudades
    route = [city_names[i] for i in individual]
    return sum(distance(cities[route[i-1]], cities[route[i]]) for i in range(len(route))), 

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(len(cities)), len(cities))
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
indpb = 1.0/len(cities) # Probabilidad de mutación por índice
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=indpb)
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("evaluate", evaluate)

population = toolbox.population(n=300) # Población de 300 individuos
hof = tools.HallOfFame(5)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean)
stats.register("min", np.min)
stats.register("max", np.max)


population, logbook = eaSimpleWithLogbook(population, toolbox, 0.90, 0.1, 200, stats=stats, halloffame=hof)

for gen, record in enumerate(logbook):
    best_in_gen = record['min']
    
    # Using a small threshold for floating-point comparison
    epsilon = 1e-9
    matching_individuals = [ind for ind in population if abs(ind.fitness.values[0] - best_in_gen) < epsilon]

    # Check if any individual matches the criteria
    if matching_individuals:
        best_route_indices = matching_individuals[0]
        best_route = [city_names[i] for i in best_route_indices]
        print(f"Mejor ruta de la generación {gen + 1}: {best_route}")
    else:
        print(f"No matching individual found in generation {gen + 1}.")



# Visualizar la mejor ruta
plt.figure(figsize=(10, 6))
for i in range(-1, len(best_route)-1):
    city1 = cities[best_route[i]]
    city2 = cities[best_route[i+1]]
    plt.plot([city1[1], city2[1]], [city1[0], city2[0]], 'b-')
    plt.scatter(city1[1], city1[0], marker='o')
    plt.text(city1[1], city1[0], best_route[i])
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Mejor Ruta')
plt.grid(True)
plt.show()
