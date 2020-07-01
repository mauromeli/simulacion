import csv
import numpy as np
import sympy as sy
from decimal import Decimal as dec

def stock_analysis(file_path):
    file = open(file_path, 'r')
    reader = csv.reader(file)
    prev_value = 0
    aumento = -1
    disminuyo = 0
    seMantuvoIgual = 0
    total_values = 0

    for row in reader:

        if(dec(row[1]) > prev_value):
            aumento += 1
        else:
            if(dec(row[0]) < prev_value):
                disminuyo += 1
            else:
                seMantuvoIgual += 1

        prev_value = dec(row[1])
        total_values += 1

    probAumentar = aumento/total_values
    probDisminuir = disminuyo / total_values
    probMantenerseIgual = seMantuvoIgual/total_values

    print("aumento: ", aumento)
    print("disminuyo: ", disminuyo)
    print("se mantuvo igual: ", seMantuvoIgual)
    print("total de datos:",total_values)
    print("\n")

    print("Prob de aumentar =", probAumentar)
    print("Prob de disminuir =", probDisminuir)
    print("Prob de mantener el precio:", probMantenerseIgual)
    print("verificacion de probabilidades suman 1:", (aumento + disminuyo + seMantuvoIgual)/total_values)

    #CALCULO PROBABILIDADES CONDICIONALES

    probAumentarTalQueAumento = 1 - (probMantenerseIgual + probDisminuir)
    probMantenerseIgualTalQueSeMantuvoIgual = 1 - (probAumentar + probDisminuir)
    probDisminuirTalQueDisminuyo = 1 - (probAumentar + probMantenerseIgual)

    print("\n")
    print("Prob de aumentar tal que aumento =", probAumentarTalQueAumento)
    print("Prob de disminuir tal que disminuyo =", probDisminuirTalQueDisminuyo)
    print("Prob de mantener el precio tal que lo mantuvo:", probMantenerseIgualTalQueSeMantuvoIgual)

    #ARMO LA MATRIZ DE TRANSICIONES
    matriz_aux = [[probMantenerseIgualTalQueSeMantuvoIgual, probAumentar, probDisminuir],
              [probMantenerseIgual, probAumentarTalQueAumento, probDisminuir],
              [probMantenerseIgual, probAumentar, probDisminuirTalQueDisminuyo]]

    matriz = np.array(matriz_aux)
    print(matriz)

stock_analysis('accion_a.csv')