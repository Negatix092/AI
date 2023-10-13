from copy import deepcopy

DIRECTIONS = {"ARRIBA": [-1, 0], "ABAJO": [1, 0], "IZQUIERDA": [0, -1], "DERECHA": [0, 1]}
Matrix1 = [1, 2, 3, 4, -1, -1, -1, -1, 0]
Matrix2 = [-1, -1, -1, -1, 5, 6, 7, 8, 0]
MATRIZ = [1, 2, 3, 4, 5, 6, 7, 8, 0]


class Nodo:
    def __init__(self, estado, anterior, g, h, dir):
        self.estado = estado
        self.anterior = anterior
        self.g = g  # costo desde la posición de inicio
        self.h = h  # costo hasta la posición final (heurística)
        self.dir = dir  # dirección como cadena

    # costo global
    def f(self):
        return self.g + self.h


# heurística DB
def DB(a, b, costos, i):
    costo = 0
    for fila in range(3):
        for col in range(3):
            pos = getPos(b, a[3 * fila + col])
            if pos is not None:
                # Calcular la diferencia en filas y columnas
                diff_fila = abs(fila - pos[0])
                diff_col = abs(col - pos[1])
                # Aplicar pesos a las diferencias
                peso = 1
                if a[3 * fila + col] != 0:  # Sin peso adicional para la posición vacía
                    peso = 2
                costo += peso * (diff_fila + diff_col)

    if 0 <= i < len(costos):
        costo = costo + costos[i]

    return costo


# la heurística utilizada es la distancia de Manhattan
def MHD(a, b, archivo1, archivo2):
    archivo1.write(str(a) + '\n')

    costo = 0
    for fila in range(3):
        for col in range(3):
            pos = getPos(b, a[3 * fila + col])
            costo += abs(fila - pos[0]) + abs(col - pos[1])
    archivo2.write(str(costo) + '\n')

    return costo


# devuelve el nodo que tiene el costo estimado más bajo (f)
def getMejorNodo(openSet):
    primeraIteracion = True
    mejorF = None
    mejorNodo = None

    for nodo in openSet.values():
        if primeraIteracion or nodo.f() < mejorF:
            primeraIteracion = False
            mejorNodo = nodo
            mejorF = mejorNodo.f()

    return mejorNodo


# obtener la posición de un elemento en una lista plana
def getPos(estado, elem):
    if elem in estado:
        return estado.index(elem) // 3, estado.index(elem) % 3
    return None


# devuelve todos los nodos adyacentes que son posiciones válidas
def getNodosAdyacentes(nodo, MATRIZ, archivo1, archivo2, conjuntoExpandido):
    listaNodos = []
    posVacia = getPos(nodo.estado, 0)

    for dir in DIRECTIONS.keys():
        nuevaPos = (posVacia[0] + DIRECTIONS[dir][0], posVacia[1] + DIRECTIONS[dir][1])
        if 0 <= nuevaPos[0] < 3 and 0 <= nuevaPos[1] < 3:
            nuevoEstado = deepcopy(nodo.estado)
            indice_vacio = nuevoEstado.index(0)
            nuevo_indice_vacio = 3 * nuevaPos[0] + nuevaPos[1]
            nuevoEstado[indice_vacio], nuevoEstado[nuevo_indice_vacio] = nuevoEstado[nuevo_indice_vacio], nuevoEstado[indice_vacio]
            estado_nodo_str = str(nuevoEstado)
            if estado_nodo_str not in conjuntoExpandido:  # Comprobar si el nodo ya ha sido expandido
                listaNodos.append(Nodo(nuevoEstado, nodo.estado, nodo.g + 1, MHD(nuevoEstado, MATRIZ, archivo1, archivo2), dir))

    return listaNodos


def getNodosAdyacentesBD(nodo, MATRIZ, costos, maxi):
    listaNodos = []
    posVacia = getPos(nodo.estado, 0)

    for dir in DIRECTIONS.keys():
        nuevaPos = (posVacia[0] + DIRECTIONS[dir][0], posVacia[1] + DIRECTIONS[dir][1])
        if 0 <= nuevaPos[0] < 3 and 0 <= nuevaPos[1] < 3:
            nuevoEstado = deepcopy(nodo.estado)
            indice_vacio = nuevoEstado.index(0)
            nuevo_indice_vacio = 3 * nuevaPos[0] + nuevaPos[1]
            nuevoEstado[indice_vacio], nuevoEstado[nuevo_indice_vacio] = nuevoEstado[nuevo_indice_vacio], nuevoEstado[indice_vacio]
            listaNodos += [Nodo(nuevoEstado, nodo.estado, nodo.g + 1, DB(nuevoEstado, MATRIZ, costos, maxi - 6), dir)]

    return listaNodos


# construye el camino resultante a partir del conjunto cerrado
def construirCamino(conjuntoCerrado, MATRIZ):
    nodo = conjuntoCerrado[str(MATRIZ)]
    camino = []

    while nodo.dir:
        camino.append(nodo.dir)
        nodo = conjuntoCerrado[str(nodo.anterior)]

    return camino


# implementación del algoritmo A* para la mejor ruta
def juego(puzzle, MATRIZ, nombre):

    archivo1 = open('base de datos: ' + nombre + '.txt', 'w')
    archivo2 = open('costos: ' + nombre + '.txt', 'w')
    # agregar el nodo de inicio
    maxi = 0
    openSet = {str(puzzle): Nodo(puzzle, puzzle, 0, MHD(puzzle, MATRIZ, archivo1, archivo2), "")}
    conjuntoCerrado = {}
    conjuntoExpandido = set()  # Inicializar conjuntoExpandido aquí

    while len(openSet) > 0:
        nodoExaminado = getMejorNodo(openSet)
        del openSet[str(nodoExaminado.estado)]  # Eliminar el nodo examinado del conjunto abierto
        conjuntoCerrado[str(nodoExaminado.estado)] = nodoExaminado
        conjuntoExpandido.add(str(nodoExaminado.estado))  # Agregar el estado a conjuntoExpandido

        if nodoExaminado.estado == MATRIZ:
            # construir el camino final una vez que termine el algoritmo
            print('Número de nodos expandidos: ' + str(len(conjuntoExpandido)))  # Imprimir el tamaño de conjuntoExpandido
            print('Costo del camino: ' + str(len(construirCamino(conjuntoCerrado, MATRIZ))))

            archivo1.close()
            archivo2.close()
            return construirCamino(conjuntoCerrado, MATRIZ)[::-1]

        nodos_adyacentes = getNodosAdyacentes(nodoExaminado, MATRIZ, archivo1, archivo2, conjuntoExpandido)

        # Actualizar conjuntoCerrado y conjuntoExpandido
        for nodo in nodos_adyacentes:
            estado_nodo_str = str(nodo.estado)
            if estado_nodo_str in conjuntoCerrado.keys() or estado_nodo_str in conjuntoExpandido:
                maxi += 1
                continue

            openSet[estado_nodo_str] = nodo

    # Si no hay solución, devuelve una cadena vacía
    return "Sin solución"


def heurist_BD(puzzle, MATRIZ, costos):
    maxi = 0
    openSet = {str(puzzle): Nodo(puzzle, puzzle, 0, DB(puzzle, MATRIZ, costos, maxi), "")}
    conjuntoCerrado = {}
    conjuntoExpandido = set()  # Inicializar conjuntoExpandido aquí

    while len(openSet) > 0:
        nodoExaminado = getMejorNodo(openSet)
        del openSet[str(nodoExaminado.estado)]  # Eliminar el nodo examinado del conjunto abierto
        conjuntoCerrado[str(nodoExaminado.estado)] = nodoExaminado
        conjuntoExpandido.add(str(nodoExaminado.estado))  # Agregar el estado a conjuntoExpandido

        if nodoExaminado.estado == MATRIZ:
            print('Número de nodos expandidos: ' + str(len(conjuntoExpandido)))  # Imprimir el tamaño de conjuntoExpandido
            print('Costo del camino: ' + str(len(construirCamino(conjuntoCerrado, MATRIZ))))

            return construirCamino(conjuntoCerrado, MATRIZ)[::-1]

        nodos_adyacentes = getNodosAdyacentesBD(nodoExaminado, MATRIZ, costos, maxi)

        # Actualizar conjuntoCerrado y conjuntoExpandido
        for nodo in nodos_adyacentes:
            estado_nodo_str = str(nodo.estado)
            if estado_nodo_str in conjuntoCerrado.keys() or estado_nodo_str in conjuntoExpandido:
                maxi += 1
                continue

            openSet[estado_nodo_str] = nodo

    # Si no hay solución, devuelve una cadena vacía
    return "Sin solución"


def lectura_bd(nombre):
    archivo = open('Cost - ' + nombre + '.txt', 'r')
    costos = archivo.readlines()

    archivo.close()
    return costos


def suma_costos(costos1, costos2):
    sum_costos = []

    if len(costos1) <= len(costos2):
        minimo = len(costos1)
        maximo = len(costos2)
    else:
        minimo = len(costos2)
        maximo = len(costos1)

    for i in range(maximo):
        if i >= minimo:
            if minimo == len(costos2):
                sum_costos.append(int(costos1[i]))
            if minimo == len(costos1):
                sum_costos.append(int(costos2[i]))
        else:
            sum_costos.append(abs(int(costos1[i]) - int(costos2[i])))
    return sum_costos


def es_solucionable(tablero):
    tablero_plano = [casilla for casilla in tablero if casilla != 0]
    inversiones = 0

    for i in range(len(tablero_plano)):
        for j in range(i + 1, len(tablero_plano)):
            if tablero_plano[i] > tablero_plano[j]:
                inversiones += 1

    return inversiones % 2 == 0


if __name__ == '__main__':
    lista = []
    cos1 = []
    cos2 = []

    print('Estado completo del tablero:   (3, 1, 0, 8, 4, 2, 5, 6, 7)')

    if es_solucionable(MATRIZ):
        print('Tablero 1: ')
        juego([3, 1, 0, -1, 4, 2, -1, -1, -1], Matrix1, '1 - (3, 1, 0, 8, 4, 2, 5, 6, 7)')

        print()
        print('Tablero 2: ')
        juego([-1, -1, 0, 8, -1, -1, 5, 6, 7], Matrix2, '2 - (3, 1, 0, 8, 4, 2, 5, 6, 7)')

        print()
        print('Heurística de Manhattan: ')
        print(juego([3, 1, 0, 8, 4, 2, 5, 6, 7], MATRIZ, '3 - (3, 1, 0, 8, 4, 2, 5, 6, 7)'))
        print()
        print('Heurística DB: ')
        cos1 = lectura_bd('1 - (3, 1, 0, 8, 4, 2, 5, 6, 7)')
        cos2 = lectura_bd('2 - (3, 1, 0, 8, 4, 2, 5, 6, 7)')

        lista = suma_costos(cos1, cos2)
        print(heurist_BD([3, 1, 0, 8, 4, 2, 5, 6, 7], MATRIZ, lista))
    else:
        print("El estado completo del tablero no es solucionable.")


