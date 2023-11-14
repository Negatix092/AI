import random
import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools, algorithms
from geopy.distance import geodesic


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

def create_route():
    route = list(range(len(cities)))
    random.shuffle(route)
    return route


def evaluate(individual):
    distance = 0
    city_names = list(cities.keys())
    for i in range(len(individual) - 1):
        city1 = city_names[individual[i]]
        city2 = city_names[individual[i+1]]
        distance += geodesic(cities[city1], cities[city2]).kilometers
    return distance,


def mutShuffleIndexes(individual, indpb):
    size = len(individual)
    for i in range(size):
        if random.random() < indpb:
            swap_indx = random.randint(0, size - 1)
            individual[i], individual[swap_indx] = individual[swap_indx], individual[i]
    return individual,


creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_route)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(cities))
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("evaluate", evaluate)


def main():
    random.seed(42)
    
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(30)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.1, ngen=200, stats=stats, halloffame=hof)
    
    return pop, stats, hof

def plot_route(route):
    city_names = list(cities.keys())
    x = [cities[city_names[i]][1] for i in route]
    y = [cities[city_names[i]][0] for i in route]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, color='red')
    plt.plot(x, y, linestyle='-')
    for i, (lat, lon) in enumerate(cities.values()):
        plt.text(lon, lat, city_names[i]+ " (" + str(route[i]) +")")
    plt.show()

def print_route(route):
    city_names = list(cities.keys())
    route_names = [city_names[i] for i in route]
    print(" -> ".join(route_names))


if __name__ == "__main__":
    _, _, hof = main()
    best_route = hof[0]
    plot_route(best_route)
    print_route(best_route)
    

