from copy import deepcopy
from queue import PriorityQueue  # Import PriorityQueue

DIRECTIONS = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
Matrix1 = [1, 2, 3, 4, 0, 0, 0, 0, 0]
Matrix2 = [0, 0, 0, 0, 5, 6, 7, 8, 0]
MATRIX = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class Node:
    def __init__(self, state, previous, g, h, dir):
        self.state = state
        self.previous = previous
        self.g = g  # cost from the starting position
        self.h = h  # cost to the end position (heuristic)
        self.dir = dir  # direction as a string

    # global cost
    def f(self):
        return self.g + self.h


def DB(a, b, costList, i):
    cost = 0
    for num in a:
        pos = getPos(b, num)
        row = pos // 3  # Assuming a 3x3 grid
        col = pos % 3   # Assuming a 3x3 grid
        cost += abs(row - a.index(num) // 3) + abs(col - a.index(num) % 3)
    cost = cost + costList[i]
    return cost


def MHD(a, b, file, file2):
    file.write(str(a) + '\n')
    cost = 0
    for num in a:
        pos = getPos(b, num)
        row = pos // 3  # Assuming a 3x3 grid
        col = pos % 3   # Assuming a 3x3 grid
        cost += abs(row - a.index(num) // 3) + abs(col - a.index(num) % 3)
    file2.write(str(cost) + '\n')
    return cost



# returns the node that have the lowest estimated cost (f)
def getBestNode(openSet):
    firstIter = True

    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()

    return bestNode


def getPos(state, elem):
    return state.index(elem)


def getAdjNode(node, MATRIX, file, file2):
    listNode = []
    emptyPos = getPos(node.state, 0)

    for dir in DIRECTIONS.keys():
        newRow, newCol = emptyPos // 3, emptyPos % 3  # Assuming a 3x3 grid

        if dir == "UP":
            newRow -= 1
        elif dir == "DOWN":
            newRow += 1
        elif dir == "LEFT":
            newCol -= 1
        elif dir == "RIGHT":
            newCol += 1

        newPos = newRow * 3 + newCol  # Convert back to flat list index

        if 0 <= newRow < 3 and 0 <= newCol < 3:
            newState = list(node.state)  # Convert to a list
            newState[emptyPos] = node.state[newPos]
            newState[newPos] = 0
            listNode.append(Node(newState, node.state, node.g + 1, MHD(newState, MATRIX, file, file2), dir))

    return listNode


def getAdjNodeBD(node, MATRIX, costList, maxi):
    listNode = []
    emptyPos = getPos(node.state, 0)
    grid_size = int(len(node.state) ** 0.5)  # Assuming a square grid

    for dir in DIRECTIONS.keys():
        new_pos = emptyPos + DIRECTIONS[dir]

        if 0 <= new_pos < len(node.state):
            new_state = list(node.state)  # Convert to a list
            new_state[emptyPos] = node.state[new_pos]
            new_state[new_pos] = 0

            listNode.append(Node(new_state, node.state, node.g + 1, DB(new_state, MATRIX, costList, maxi - 6), dir))

    return listNode


def buildPath(closedSet, MATRIX):
    node = closedSet[str(MATRIX)]
    path = []
    flat_matrix = [num for num in MATRIX]  # Convert MATRIX to flat list

    while node.dir:
        flat_state = [num for num in node.state]  # Convert state to flat list
        # Find the move direction by comparing the flat lists
        direction = DIRECTIONS.get(flat_state.index(0) - flat_matrix.index(0))
        path.append(direction)
        node = closedSet[str(node.previous)]

    return path[::-1]  # Reverse the path to get the correct order

def cost_calculate(state, cuttedboard, goal):
    cost = 0
    for number in cuttedboard:
        if number != 0:
            cost += abs(cuttedboard.index(number) % 3 - state.index(number) % 3) + abs(
                cuttedboard.index(number) // 3 - state.index(number) // 3
            )
    return cost

def generate_pattern_database(start_state, goal, txt):
    pdb_entries = {}  # Dictionary to store pattern database entries

    # Define a priority queue for A* search
    pq = PriorityQueue()
    start_state_tuple = tuple(start_state)
    initial_cost = cost_calculate(start_state_tuple, start_state, goal)
    pq.put((initial_cost, start_state_tuple))

    while not pq.empty():
        cost, current_state = pq.get()
        pdb_entries[current_state] = cost

        # Generate possible next states
        zero_index = current_state.index(0)
        row, col = zero_index // 3, zero_index % 3
        possible_moves = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
        ]

        for move_row, move_col in possible_moves:
            if 0 <= move_row < 3 and 0 <= move_col < 3:
                new_state = list(current_state)
                new_zero_index = move_row * 3 + move_col
                new_state[zero_index], new_state[new_zero_index] = (
                    new_state[new_zero_index],
                    new_state[zero_index],
                )
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in pdb_entries:
                    new_cost = cost_calculate(new_state_tuple, start_state, goal)
                    pq.put((new_cost, new_state_tuple))

    # Write the pattern database entries to a file
    with open(txt, "w") as file:
        for state, cost in pdb_entries.items():
            file.write(f"{state}, {cost}\n")


def juego(puzzle, MATRIX, nombre, pattern_database):
    file = open('DB - ' + nombre + '.txt', 'w')
    file2 = open('Cost - ' + nombre + '.txt', 'w')
    
    maxi = 0
    openSet = {str(puzzle): Node(puzzle, puzzle, 0, MHD(puzzle, MATRIX, file, file2), "")}
    closedSet = {}

    while len(openSet) > 0:
        examNode = getBestNode(openSet)
        closedSet[str(examNode.state)] = examNode

        if examNode.state == MATRIX:
            # build the final path once the algo finished
            print('Number of nodes expanded: ' + str(maxi))
            print('Path cost : ' + str(len(buildPath(closedSet, MATRIX))))

            file.close()
            file2.close()
            return buildPath(closedSet, MATRIX)[::-1]
        
        adj = getAdjNode(examNode, MATRIX, file, file2)
        
        # Update the closed set
        for node in adj:
            if str(node.state) in closedSet.keys() or str(node.state) in openSet.keys() and openSet[str(node.state)].f() < node.f():
                maxi += 1
                continue
            openSet[str(node.state)] = node
        
        # Remove the examined node from the openSet
        del openSet[str(examNode.state)]

    # If there is no solution, return the empty string
    return "No Solution"



def heurist_BD(puzzle, MATRIX, costList):
    maxi = 0
    openSet = {str(puzzle): Node(puzzle, puzzle, 0, DB(puzzle, MATRIX, costList, maxi), "")}
    closedSet = {}

    while len(openSet) > 0:
        examNode = getBestNode(openSet)
        closedSet[str(examNode.state)] = examNode
        if examNode.state == MATRIX:
            print('Number of nodes expanded: ' + str(maxi))
            print('Path cost : ' + str(len(buildPath(closedSet, MATRIX))))

            return buildPath(closedSet, MATRIX)[::-1]
        adj = getAdjNodeBD(examNode, MATRIX, costList, maxi)

        for node in adj:
            if str(node.state) in closedSet.keys() or str(node.state) in openSet.keys() and openSet[
                str(node.state)].f() < node.f():
                maxi += 1
                continue
            openSet[str(node.state)] = node
        del openSet[str(examNode.state)]

    return "No Solution"


def lectura_bd(nombre):
    file = open('Cost - ' + nombre + '.txt', 'r')
    costos = file.readlines()

    file.close()
    return costos


def suma_costos(costos1, costos2):
    sum_costos = []

    if len(costos1) <= len(costos2):
        minimo = len(costos1)
        max = len(costos2)
    else:
        minimo = len(costos2)
        max = len(costos1)

    for i in range(max):
        if i >= minimo:
            if minimo == len(costos2):
                sum_costos.append(int(costos1[i]))
            if minimo == len(costos1):
                sum_costos.append(int(costos2[i]))
        else:
            sum_costos.append(abs(int(costos1[i]) - int(costos2[i])))
    return sum_costos





        


