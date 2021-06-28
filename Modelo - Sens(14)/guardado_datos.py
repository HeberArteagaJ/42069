from openpyxl import load_workbook, Workbook
from random import randint

import parametros as par
from paciente import Paciente
from creacion_datos import generacion_examenes, generacion_insumos, generación_disponibles, generacion_jornadas


#filename = par.Paths['resultados']
filename = par.Test['resultados']


def guardar_variables(variables, Pacientes, P, M, D, lista_datos):

    n_prioritarios = 0
    for paciente in Pacientes:
        if paciente.prioridad == True:
            n_prioritarios += 1

    with open(filename, "w", encoding="UTF8") as archive:

        # Titulos
        titles = "Elemento,Valor\n"
        archive.write(titles)
        archive.truncate()

        # Parámetros de interés
        text = f"Pacientes Totales,{len(P)}\n\
Pacientes Prioritarios,{n_prioritarios}\n\
Médicos Totales,{len(M)}\n\
Días Totales,{len(D)}\n\n"
        archive.write(text)

        # Lista de datos
        for data in lista_datos:
            text = f"{data[0]},{data[1]}\n"
            archive.write(text)

        archive.write("\n")

        # Solución Óptima
        for variable in variables:
            if variable.x != 0:
                name = variable.varName.replace(",", "|")
                text = f"{name},{variable.x}\n"
                archive.write(text)


if __name__ == "__main__":
    pass
