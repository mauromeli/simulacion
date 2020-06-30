import csv
import numpy as np


# 11 sube sube
# 01 baja sube
# 10 sube baja
# 00 baja baja


def movement(previous_value, actual_value):
    if previous_value > actual_value:
        return '0'
    else:
        return '1'

def calculate_probability_matrix(states):
    return np.matrix([
        [states['00'] / (states['00'] + states['10']), states['10'] / (states['11'] + states['01'])],
        [states['01'] / (states['10'] + states['00']), states['11'] / (states['01'] + states['11'])]
    ])


states = { '11': 0, '10': 0, '01': 0, '00': 0 }


## De dos en dos
from itertools import islice
with open('./accion_a.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)
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

print(matrix)
print(matrix ** 1000)