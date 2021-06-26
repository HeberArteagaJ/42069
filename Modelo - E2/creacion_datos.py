from random import randint, choice, choices
from operator import itemgetter

import parametros as par


def generacion_examenes(pacientes, dias, dias_examenes):
    examenes_pacientes = []
    for paciente in pacientes:

        examenes_validos = []

        print("Empieza - Exámenes")
        ind = 0
        for dia in dias:
            if ind > 0:
                examenes_validos.append(dia)
                print("Se agrega fecha")
                ind -= 1
            else:
                cond = choices(population=[True, False], weights=[
                               par.EX_T, par.EX_F])

                print(f"Cond = {cond}")

                if cond == [True]:
                    examenes_validos.append(dia)
                    print("Se agrega fecha")
                    ind = choice(dias_examenes)

        examenes_pacientes.append((paciente, examenes_validos))

    print(examenes_pacientes)
    return examenes_pacientes


def generacion_insumos(pacientes, dias):
    insumos_pacientes = []
    for paciente in pacientes:

        insumos_validos = []
        for dia in dias:
            cond = choices(population=[True, False],
                           weights=[par.INS_T, par.INS_F])

            if cond == [True]:
                insumos_validos.append(dia)

        insumos_pacientes.append((paciente, insumos_validos))

    return insumos_pacientes


def generación_disponibles(pacientes, medicos, dias, bloques):  # MODIFICAR

    lista_disponibles = []

    for paciente in pacientes:

        disponibles_paciente = []

        """consultas_min = int(len(dias))  # Cambiar a Parámetros
        consultas_max = int(len(dias) * (len(bloques) / 3)
                            )  # Cambiar a Parámetros"""

        consultas_min = par.Pacientes['n_DISP_min']
        consultas_max = par.Pacientes['n_DISP_max']
        rango_dias = choice(range(consultas_min, consultas_max + 1))

        for _ in range(rango_dias):  # Crear mejor algoritmo; Probar
            medico = choice(medicos)
            dia = choice(dias)
            bloque = choice(bloques)

            data = [medico, dia, bloque]

            while data in disponibles_paciente:
                medico = choice(medicos)
                dia = choice(dias)
                bloque = choice(bloques)

                data = [medico, dia, bloque]

            disponibles_paciente.append(data)

        # Orden de la lista
        disponibles_paciente = sorted(
            disponibles_paciente, key=itemgetter(0, 1, 2))

        lista_disponibles.append((paciente, disponibles_paciente))

    return lista_disponibles


def generacion_jornadas(medicos, dias):

    lista_jornadas = []

    for medico in medicos:

        jornadas_medico = []

        for dia in dias:
            rango_entrada = range(
                par.Jornadas['Entrada_min'], par.Jornadas['Entrada_max'] + 1)
            hora_entrada = choice(rango_entrada)
            hora_salida = hora_entrada + par.Jornadas['Jornada']

            jornadas_medico.append([dia, hora_entrada, hora_salida])

        # Orden de la lista
        jornadas_medico = sorted(jornadas_medico, key=itemgetter(0, 1, 2))

        lista_jornadas.append((medico, jornadas_medico))

    return lista_jornadas


if __name__ == "__main__":
    pass
