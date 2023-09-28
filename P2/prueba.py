import random
import heapq
import math
import sys
from collections import defaultdict, deque, Counter
from itertools import combinations


class Problem(object):
    """A problem to find a route between locations on a `Map`.
    Create a problem with RouteProblem(start, goal, map=Map(...)}).
    States are the vertexes in the Map graph; actions are destination states."""
    
    def __init__(self, initial=None, goal=None, graph=None, **kwds): 
        self.__dict__.update(initial=initial, goal=goal, graph=graph, **kwds) 

    def actions(self, state): 
        """The places neighboring `state`."""
        return self.map.neighbors[state]
    
    def result(self, state, action):
        """Go to the `action` place, if the map says that is possible."""
        return action if action in self.map.neighbors[state] else state
    
    def is_goal(self, state):        
        return state == self.goal
    
    def action_cost(self, s, action, s1):
        """The distance (cost) to go from s to s1."""
        return self.map.distances[s, s1]
    

class Node:
    "A Node in a search tree."
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.__dict__.update(state=state, parent=parent, action=action, path_cost=path_cost)

    def __repr__(self): return '{}'.format(self.state)
    def __len__(self): return 0 if self.parent is None else (1 + len(self.parent))
    def __lt__(self, other): return self.path_cost < other.path_cost
    
    
failure = Node('failure', path_cost=math.inf) # Indicates an algorithm couldn't find a solution.
cutoff  = Node('cutoff',  path_cost=math.inf) # Indicates iterative deepening search was cut off.
    
    
def expand(problem, node):
    e = 0
    "Expand a node, generating the children nodes."
    s = node.state
    for action in problem.actions(s):
        s1 = problem.result(s, action)
        cost = node.path_cost + problem.action_cost(s, action, s1)
        yield Node(s1, node, action, cost)
        e += 1#counting the number of nodes expanded
        

def path_actions(node):
    "The sequence of actions to get to this node."
    if node.parent is None:
        return []  
    return path_actions(node.parent) + [node.action]


def path_states(node):
    "The sequence of states to get to this node."
    if node in (cutoff, failure, None): 
        return []
    return path_states(node.parent) + [node.state]


#This dictionary is created to store the heuristic distances
heuristic_distances = {
    'Ellensburg': 516.03,'Pendleton': 472.53,'Spokane': 362.93,'Bonners Ferry': 303.57,
    'Missoula': 232.19,'West Glacier': 191.21,'Helena': 174.65,'Butte': 221.04,
    'Great Falls': 104.1,'Havre': 0
}

class PriorityQueue:
    #Modified, from previous homework, in order to implement the A* search. 
    """A queue in which the item with minimum f(item) is always popped first."""

    def __init__(self, items=(), key=lambda x: x): 
        self.key = key
        self.items = [] # a heap of (score, item) pairs
        for item in items:
            self.add(item, key(item))
         
    #now the f_value is considered for inserting nodes in the priority queue
    def add(self, item, f_value):
        """Add item to the queue with a given f_value."""
        score = self.key(item)
        pair = (score, item)
        heapq.heappush(self.items, pair)

    def pop(self):
        """Pop and return the item with min f(item) value."""
        if not self.items:
            return None
        score, item = heapq.heappop(self.items)
        return item
    
    def top(self): 
        if not self.items:
            return None
        return self.items[0][1]
    
    def printPriorityQueue(self):
        items = [item[1].state for item in self.items if item[1] is not None]
        print(f'Frontier: {items}')

    def __len__(self): return len(self.items)


def best_first_search(problem, f):
    "Search nodes with minimum f(node) value first."
    node = Node(problem.initial)
    frontier = PriorityQueue([node], key=f)
    reached = {problem.initial: node}
    while frontier:
        node = frontier.pop()
        if problem.is_goal(node.state):
            return node
        for child in expand(problem, node):
            s = child.state
            if s not in reached or child.path_cost < reached[s].path_cost:
                reached[s] = child
                #Now we calculate h(node) using heuristic_distances dictionary
                h_value = heuristic_distances[s]
                #And we calculate f(node) = g(node) + h(node)
                f_value = child.path_cost + h_value
                frontier.add(child, f_value)

        

        #print information about expanding the current node
        print("\n")
        print(f"Current position: {node.state} with a cost of {node.path_cost} miles")
        frontier.printPriorityQueue()
        print(f"Reached: {list(reached.values())}")
        print("\nNumber of nodes expanded so far: ", len(reached)-1)#-1 because the initial node is not expanded, Ellenburg
    return failure

def g(n): return n.path_cost

def uniform_cost_search(problem):
    "Search nodes with minimum path cost first."
    return best_first_search(problem, f=g)

#We define the A* search function
def astar_search(problem, h):
    def f(node):
        return g(node) + h[node.state] #the heuristic is the distance to the goal

    return best_first_search(problem, f)

class Map:
    """A map of places in a 2D world: a graph with vertexes and links between them. 
    In `Map(links, locations)`, `links` can be either [(v1, v2)...] pairs, 
    or a {(v1, v2): distance...} dict. Optional `locations` can be {v1: (x, y)} 
    If `directed=False` then for every (v1, v2) link, we add a (v2, v1) link."""

    def __init__(self, links, locations=None, directed=False):
        if not hasattr(links, 'items'): # Distances are 1 by default
            links = {link: 1 for link in links}
        if not directed:
            for (v1, v2) in list(links):
                links[v2, v1] = links[v1, v2]
        self.distances = links
        self.neighbors = multimap(links)
        self.locations = locations or defaultdict(lambda: (0, 0))

def multimap(pairs) -> dict:
    "Given (key, val) pairs, make a dict of {key: [val,...]}."
    result = defaultdict(list)
    for key, val in pairs:
        result[key].append(val)
    return result

deber1 = Map(
    {('Ellensburg', 'Spokane'): 175, ('Ellensburg', 'Pendleton'): 168, ('Pendleton', 'Spokane'): 200, ('Pendleton', 'Missoula'): 356, ('Spokane', 'Bonners Ferry'): 112, ('Spokane', 'Missoula'): 199, ('Bonners Ferry', 'Missoula'): 249, 
     ('Bonners Ferry', 'West Glacier'): 176, ('Missoula', 'West Glacier'): 151, ('Missoula', 'Helena'): 111, ('Missoula', 'Butte'): 119, ('Butte', 'Helena'): 65, ('West Glacier', 'Helena'): 243, ('Helena', 'Great Falls'): 91,
      ('West Glacier', 'Great Falls'): 211, ('Great Falls', 'Havre'): 115, ('West Glacier', 'Havre'): 231})

d1 = Problem('Ellensburg', 'Havre', map=deber1)


#route = uniform_cost_search(d1)

#the new route is calculated using the A* search
route = astar_search(d1, h=heuristic_distances)

if route:
    total_cost = 0
    print("\n")
    print("Optimal Route usign A* search:\n")
    for i in range (len(path_states(route))-1):
        parent = path_states(route)[i]
        child = path_states(route)[i+1]
        cost_to_child = None
        for neighbor, cost in deber1.distances.items():
            if parent == neighbor[0] and child == neighbor[1]:
                cost_to_child = cost
                break
        total_cost += cost_to_child
        print(parent, "to", child, "with cost: ", cost_to_child, " miles")

    print("\nTotal cost: ", total_cost, " miles")
else:
    print("No route found")