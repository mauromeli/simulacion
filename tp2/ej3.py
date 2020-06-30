import csv
import numpy as np
import sympy as sy

def movement(previous_value, actual_value):
    if previous_value > actual_value:
        return '0'
    else:
        return '1'

def calculate_probability_matrix(states):
    return np.matrix([
        [states['00'] / (states['00'] + states['01']), states['01'] / (states['01'] + states['00'])],
        [states['10'] / (states['10'] + states['11']), states['11'] / (states['10'] + states['11'])]
    ])



def stock_analysis(file_path):
    states = { '11': 0, '10': 0, '01': 0, '00': 0 }
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        first_row = next(reader)
        previous_row = next(reader)
        previous_movement = movement(first_row[1], previous_row[1])
        for row in reader:
            actual_movement = movement(previous_row[1], row[1])
            total_movement = previous_movement + actual_movement
            states[total_movement] += 1

            previous_total_movement = total_movement
            previous_row = row
            previous_movement = actual_movement


    matrix = calculate_probability_matrix(states)

    print('Los movimientos totales fueron: ')
    print(states)
    print('La matriz de transición de estados es: ')
    print(matrix)

    print(matrix ** 10000)

    pi0, pi1 = sy.symbols('pi0 pi1')

    print("Los tiempos que va a pasar en cada estado son: ")
    print(sy.solve((matrix[0,0] * pi0 + matrix[0,1] * pi1 - pi0, matrix[1,0] * pi0 + matrix[1,1] * pi1 - pi1, pi0+pi1-1), pi0, pi1))


stock_analysis('./tp2/accion_c.csv')
