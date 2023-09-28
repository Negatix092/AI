# -*- coding: utf-8 -*-
from copy import deepcopy

DIRECTIONS = {"UP": [-1, 0], "DOWN": [1, 0], "LEFT": [0, -1], "RIGHT": [0, 1]}
Matrix1 = [[1, 2, 3], [4, -1, -1], [-1, -1, 0]]
Matrix2 = [[-1, -1, -1], [-1, 5, 6], [7, 8, 0]]
MATRIX = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]


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


# heuristic DB
def DB(a, b, costList, i):
    cost = 0
    for row in range(len(a)):
        for col in range(len(a[0])):
            pos = getPos(b, a[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])

    cost = cost + costList[i]
    return cost

# the heuristic used is the manhattan distance
def MHD(a, b, file, file2):
    file.write(str(a) + '\n')

    cost = 0
    for row in range(len(a)):
        for col in range(len(a[0])):
            pos = getPos(b, a[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
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


# get position of an element in an array
def getPos(state, elem):
    for row in range(len(state)):
        if elem in state[row]:
            return (row, state[row].index(elem))


# returns all the adjacent nodes that are valid positions
def getAdjNode(node, MATRIX, file, file2):
    listNode = []
    emptyPos = getPos(node.state, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.state) and 0 <= newPos[1] < len(node.state[0]):
            newState = deepcopy(node.state)
            newState[emptyPos[0]][emptyPos[1]] = node.state[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode += [Node(newState, node.state, node.g + 1, MHD(newState, MATRIX, file, file2), dir)]
    # print(emptyPos)
    return listNode


def getAdjNodeBD(node, MATRIX, costList, maxi):
    listNode = []
    emptyPos = getPos(node.state, 0)

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.state) and 0 <= newPos[1] < len(node.state[0]):
            newState = deepcopy(node.state)
            newState[emptyPos[0]][emptyPos[1]] = node.state[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode += [Node(newState, node.state, node.g + 1, DB(newState, MATRIX, costList, maxi - 6), dir)]

    # print(emptyPos)
    return listNode


# build the resulting path from the closedSet
def buildPath(closedSet, MATRIX):
    node = closedSet[str(MATRIX)]
    # path = ""
    path = []
    while node.dir:
        # path = node.dir + path
        path.append(node.dir)
        node = closedSet[str(node.previous)]

    return path


# implementation of the A* algorithm for best first path
def juego(puzzle, MATRIX, nombre):
    file = open('DB - ' + nombre + '.txt', 'w')
    file2 = open('Cost - ' + nombre + '.txt', 'w')
    # add the start node
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


        # update the closed set
        for node in adj:
            # print('adj', node.state)
            if str(node.state) in closedSet.keys() or str(node.state) in openSet.keys() and openSet[
                str(node.state)].f() < node.f():
                maxi += 1
                continue

            openSet[str(node.state)] = node

        # remove the examined node from the openSet
        del openSet[str(examNode.state)]

    # if there is no solution return the empty string
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


if __name__ == '__main__':
    lista = []
    cos1 = []
    cos2 = []

    print('Complete board state:  (4, 5, 1, 6, 8, 7, 3, 2, 0)')
    print('Matrix 1: ')
    juego([[4, -1, 1],
           [-1, -1, -1],
           [3, 2, 0]], Matrix1, '1 - (4, 5, 1, 6, 8, 7, 3, 2, 0)')

    print()
    print('Matrix 2: ')
    juego([[-1, 5, -1],
           [6, 8, 7],
           [-1, -1, 0]], Matrix2, '2 - (4, 5, 1, 6, 8, 7, 3, 2, 0)')

    print()
    print('Manhattan Heuristic: ')
    print(juego([[4, 5, 1],
                 [6, 8, 7],
                 [3, 2, 0]], MATRIX, '3 - (4, 5, 1, 6, 8, 7, 3, 2, 0)'))
    print()
    print('DB Heuristic: ')
    cos1 = lectura_bd('1 - (4, 5, 1, 6, 8, 7, 3, 2, 0)')
    cos2 = lectura_bd('2 - (4, 5, 1, 6, 8, 7, 3, 2, 0)')

    lista = suma_costos(cos1, cos2)
    print(heurist_BD([[4, 5, 1],
                      [6, 8, 7],
                      [3, 2, 0]], MATRIX, lista))

    print('\n------------------------------------')
    print('Complete board state:   (2, 3, 5, 1, 4, 7, 0, 8, 6)')
    print('Matrix 1: ')
    juego([[2, 3, -1],
           [1, 4, -1],
           [0, -1, -1]], Matrix1, '1 - (2, 3, 5, 1, 4, 7, 0, 8, 6)')

    print()
    print('Matrix 2: ')
    juego([[-1, -1, 5],
           [-1, -1, 7],
           [0, 8, 6]], Matrix2, '2 - (2, 3, 5, 1, 4, 7, 0, 8, 6)')

    print()
    print('Manhattan Heuristic: ')
    print(juego([[2, 3, 5],
                 [1, 4, 7],
                 [0, 8, 6]], MATRIX, '3 - (2, 3, 5, 1, 4, 7, 0, 8, 6)'))
    print()
    print('DB Heuristic: ')
    cos1 = lectura_bd('1 - (2, 3, 5, 1, 4, 7, 0, 8, 6)')
    cos2 = lectura_bd('2 - (2, 3, 5, 1, 4, 7, 0, 8, 6)')

    lista = suma_costos(cos1, cos2)
    print(heurist_BD([[2, 3, 5],
                      [1, 4, 7],
                      [0, 8, 6]], MATRIX, lista))

    print('\n------------------------------------')
    print('Complete board state:   (2, 0, 3, 1, 7, 4, 5, 8, 6')
    print('Matrix 1: ')
    juego([[2, 0, 3],
           [1, -1, 4],
           [-1, -1, -1]], Matrix1, '1 - (2, 0, 3, 1, 7, 4, 5, 8, 6)')

    print()
    print('Matrix 2: ')
    juego([[-1, 0, -1],
           [-1, 7, -1],
           [5, 8, 6]], Matrix2, '2 - (2, 0, 3, 1, 7, 4, 5, 8, 6)')

    print()
    print('Manhattan Heuristic: ')
    print(juego([[2, 0, 3],
                 [1, 7, 4],
                 [5, 8, 6]], MATRIX, '3 - (2, 0, 3, 1, 7, 4, 5, 8, 6)'))
    print()
    print('DB Heuristic: ')
    cos1 = lectura_bd('1 - (2, 0, 3, 1, 7, 4, 5, 8, 6)')
    cos2 = lectura_bd('2 - (2, 0, 3, 1, 7, 4, 5, 8, 6)')

    lista = suma_costos(cos1, cos2)
    print(heurist_BD([[2, 0, 3],
                      [1, 7, 4],
                      [5, 8, 6]], MATRIX, lista))

    print('\n------------------------------------')
    print('Complete board state:   (6, 5, 1, 4, 2, 3, 0, 8, 7)')
    print('Matrix 1: ')
    juego([[-1, -1, 1],
           [4, 2, 3],
           [0, -1, -1]], Matrix1, '1 - (6, 5, 1, 4, 2, 3, 0, 8, 7)')

    print()
    print('Matrix 2: ')
    juego([[6, 5, -1],
           [-1, -1, -1],
           [0, 8, 7]], Matrix2, '2 - (6, 5, 1, 4, 2, 3, 0, 8, 7)')

    print()
    print('Manhattan Heuristic: ')
    print(juego([[6, 5, 1],
                 [4, 2, 3],
                 [0, 8, 7]], MATRIX, '3 - (6, 5, 1, 4, 2, 3, 0, 8, 7)'))
    print()
    print('DB Heuristic: ')
    cos1 = lectura_bd('1 - (6, 5, 1, 4, 2, 3, 0, 8, 7)')
    cos2 = lectura_bd('2 - (6, 5, 1, 4, 2, 3, 0, 8, 7)')

    lista = suma_costos(cos1, cos2)
    print(heurist_BD([[6, 5, 1],
                      [4, 2, 3],
                      [0, 8, 7]], MATRIX, lista))
