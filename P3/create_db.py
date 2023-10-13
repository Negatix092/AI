#solving the 8-puzzle
from itertools import permutations

def cost_calculate(state,cuttedboard,goal):
    cost = 0
    for number in cuttedboard:
        if number != 0:
            #calculate and add the manhattan distance for this number in the puzzle state
            cost += abs(cuttedboard.index(number)%3 - state.index(number)%3) + abs(cuttedboard.index(number)//3 - state.index(number)//3)
    return cost

def generate_pattern_database(cuttedboard, goal, txt):
    
    # Extraemos todas las permutaciones posibles del patrón y calculamos el costo
    pdb_entries = []
    for s in set(permutations(cuttedboard)):
        cost = cost_calculate(s, cuttedboard, goal)
        pdb_entries.append(str(s) + ', ' + str(cost) + '\n')
    
    # Escribimos la PDB en un archivo
    with open(txt, 'w') as file:
        file.writelines(pdb_entries)
    

# Ejemplo de uso
goal1 = [1,2,3,4,0,0,0,0,0]
goal2 = [0,0,0,0,5,6,7,8,0]
generate_pattern_database([1,2,3,4,0,0,0,0,0], goal1, 'FirstHalf.txt')
generate_pattern_database([0,0,0,0,5,6,7,8,0], goal2, 'SecondHalf.txt')
