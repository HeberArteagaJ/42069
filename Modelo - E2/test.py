from random import randint, choices, choice
import os
from openpyxl import load_workbook


"""test = choices(population=[True, False], weights=[0.7, 0.4])
for i in range(10):
    test = choices(population=[True, False], weights=[0.7, 0.4])
    print(test)
    if test == [True]:
        print("OK")"""


"""dias = range(10 + 1)
bloques = range(6 + 1)

consultas_min = int(len(dias))
consultas_max = int(len(dias) * (len(bloques) / 3))
rango_dias = choice(range(consultas_min, consultas_max + 1))

print(consultas_min)
print(consultas_max)
print(range(consultas_min, consultas_max + 1))
print(rango_dias)"""


filename = os.path.join("Test", "Parametros.xlsx")

workbook = load_workbook(filename)

hoja = workbook['Parametros']
print(hoja['A2'].value)
