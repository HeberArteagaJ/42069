from gurobipy import GRB, Model, quicksum
from random import randint, seed, uniform
from time import time

import parametros as par
from carga_datos import carga_datos, carga_disponibles, carga_paciente, carga_jornadas
from guardado_datos import guardar_variables, registro_tiempos, registro_medicos

# ARCHIVOS
#filename_pacientes = par.Paths['pacientes']
#filename_medicos = par.Paths['medicos']
filename_pacientes = par.Test['pacientes']
filename_medicos = par.Test['medicos']

seed(42069)
model = Model("Recalendarización Operaciones Electivas")

# Comprobación de Output
check_p = time()

# SETS
P = range(1, par.Indices['n_P'] + 1)  # Pacientes [Int]
M = range(1, par.Indices['M'] + 1)  # Médicos [Int]
A = range(1, par.Indices['A'] + 1)  # Personal médico [List]
D = range(1, par.Indices['D'] + 1)  # Días [Int]
T = range(1, par.Indices['T'] + 1)  # Tiempo (en bloques de 15 min) [Int]

# Tiempo prioritario - Subconjunto de T [Int] (en min)
T_PRI = range(par.Indices['T_PRI_min'], par.Indices['T_PRI_max'] + 1)

# Tiempo de Índices
check_a = time()
t_indices = check_a-check_p
check_p = check_a

# Instancias - Clase Paciente
Pacientes = [carga_paciente(filename_pacientes, p)
             for p in P]

# Comprobación de Output
print("Pacientes - Ok")
check_a = time()
print(check_a-check_p)
t_clases_pacientes = check_a-check_p
print()
check_p = check_a


# PARAMETERS
# Parámetros Numéricos
DUR = {p: randint(par.Parametros['DUR']['min'],
                  par.Parametros['DUR']['max']) for p in P}
LIM = {(m, d): par.Parametros['LIM'] for m in M for d in D}

PAB = {d: par.Indices['S'] for d in D}

CI = {p: par.Parametros['CI'] for p in P}
CM = {m: par.Parametros['CM'] for m in M}

PON = {m: par.Parametros['PON'] for m in M}

CA = par.PM['COSTOS_A']
REQ = {(p, a): randint(par.PM['CANT_REQ'][a]['min'],
                       par.PM['CANT_REQ'][a]['min']) for p in P for a in A}
PER = {(a, d, t): randint(
    par.PM['CANT_PER_MIN'], par.PM['CANT_PER'][a]) for a in A for d in D for t in T}

# Comprobación de Output
print("Parametros - Ok")
check_a = time()
print(check_a-check_p)
t_parametros = check_a-check_p
print()
check_p = check_a

# Parámetros Binarios
JOR = carga_jornadas(M, D, T, filename_medicos)

# Comprobación de Output
print("JOR - Ok")
check_a = time()
print(check_a-check_p)
t_jornadas = check_a-check_p
print()
check_p = check_a


# VARIABLES
# Variable binaria, 1 si empieza la operacion, 0 e.c.o.c
x = model.addVars(P, M, D, T, vtype=GRB.BINARY, name="x")
# Variable binaria, 1 si esta en curso la operacion, 0 e.c.o.c
y = model.addVars(P, M, D, T, vtype=GRB.BINARY, name="y")
# Variable que indica el numero de personal ilibre de cada especialidad
lib = model.addVars(A, D, T, vtype=GRB.INTEGER, lb=0, name="l")

# Comprobación de Output
print("Variables - Ok")
check_a = time()
print(check_a-check_p)
t_variables = check_a-check_p
print()
check_p = check_a

model.update()


# FUNCIÓN OBJETIVO
costo_medico = quicksum(JOR[m, d, t] * y[p, m, d, t] * CM[m]
                        for p in P for m in M for d in D for t in T)
costo_medico_extra = quicksum(
    (1 - JOR[m, d, t]) * y[p, m, d, t] * CM[m] * PON[m] for p in P for m in M for d in D for t in T)
costo_personal = quicksum(y[p, m, d, t] * REQ[p, a] * CA[a]
                          for p in P for m in M for a in A for d in D for t in T)
costo_insumos = quicksum(x[p, m, d, t] * CI[p]
                         for p in P for m in M for d in D for t in T)


model.setObjective(costo_medico + costo_medico_extra +
                   costo_personal + costo_insumos, GRB.MINIMIZE)

# Comprobación de Output
print("FO - Ok")
check_a = time()
print(check_a-check_p)
t_FO = check_a-check_p
print()
check_restr_i = check_a


# RESTRICCIONES
# Restricción 1
# Un médico solo puede operar a un paciente a la vez.
model.addConstrs((quicksum(y[p, m, d, t]
                           for p in P) <= 1 for m in M for d in D for t in T))

# Comprobación de Output
print("Restricción 1 - Ok")
check_a = time()
print(check_a-check_restr_i)
print()
check_p = check_a


# Restricción 2
# Todos los pacientes deben ser operados.
model.addConstrs((quicksum(quicksum(
    quicksum(x[p, m, d, t] for m in M) for d in D) for t in T) == 1 for p in P))

# Comprobación de Output
print("Restricción 2 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 3
# Un paciente solo se puede operar con un médico a la vez.
model.addConstrs((quicksum(y[p, m, d, t]
                           for m in M) <= 1 for p in P for d in D for t in T))

# Comprobación de Output
print("Restricción 3 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 4
# Solo si el paciente está disponible se podría efectuar la operación.
for p in P:
    for m in M:
        for d in D:
            for t in T:
                DISP = 0
                if [m, d, t] in Pacientes[p - 1].disponible:
                    DISP = 1

                model.addConstr(DISP >= x[p, m, d, t])

# Comprobación de Output
print("Restricción 4 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 5
# Solo si el médico está disponible se podría efectuar la operación.
model.addConstrs((JOR[m, d, t] >= quicksum(x[p, m, d, t] for p in P)
                 for m in M for d in D for t in T))

# Comprobación de Output
print("Restricción 5 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 6
# Solo se puede realizar la operación si están los insumos necesarios.
for p in P:
    for m in M:
        for d in D:
            for t in T:
                INS = 0
                if d in Pacientes[p - 1]. insumos:
                    INS = 1

                model.addConstr(INS >= x[p, m, d, t])

# Comprobación de Output
print("Restricción 6 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 7
# La cantidad de operaciones que se pueden realizar en un tiempo t cada día está restringida por la cantidad de pabellones disponibles dicho día.
model.addConstrs((PAB[d] >= quicksum(y[p, m, d, t]
                 for p in P for m in M) for d in D for t in T))

# Comprobación de Output
print("Restricción 7 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 8
# Solo se puede realizar la operación del paciente si tiene los examenes al día.
# Pacientes[p - 1].examenes
for p in P:
    for m in M:
        for d in D:
            for t in T:
                EX = 0
                if d in Pacientes[p - 1].examenes:
                    EX = 1

                model.addConstr(EX >= x[p, m, d, t])

# Comprobación de Output
print("Restricción 8 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 9
# Si una operación ya comenzó, se debe desarrollar en el tiempo establecido. REVISAR!!!
for p in P:
    for m in M:
        for d in D:
            for t in range(1, len(T) - DUR[p] + (+ 1 + 1)):
                model.addConstr(DUR[p] * x[p, m, d, t] <= quicksum(y[p, m, d, k]
                                for k in range(t, t + DUR[p] + (-1 + 1))))

# Comprobación de Output
print("Restricción 9 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 10
# Si una operación está en curso entonces debe haber empezado en algún momento anterior.
for p in P:
    for m in M:
        for d in D:
            for t in range(DUR[p] + (1), len(T) + 1):
                model.addConstr(y[p, m, d, t] == quicksum(
                    x[p, m, d, k] for k in range(t - DUR[p], t + 1)))

# Comprobación de Output
print("Restricción 10 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 11
# No se pueden realizar cirugías más allá de un tiempo límite (considerando horas extras).
"""for p in P:
    for m in M:
        for d in D:
            for t in T:
                model.addConstr(x[p, m, d, t] * DUR[p] <= quicksum(JOR[m, d, k]
                                for k in T) + LIM[m, d] - quicksum(JOR[m, d, k] for k in range(1, t + 1)))"""

for p in P:
    for m in M:
        for d in D:
            for t in T:
                model.addConstr(x[p, m, d, t] * DUR[p] <= len(T) - t)

# Comprobación de Output
print("Restricción 11 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 12
# Definición de la variable LIBadt (pabellones libres).
model.addConstrs((lib[a, d, t] >= PER[a, d, t] - quicksum((y[p, m, d, t] * REQ[p, a])
                 for p in P) for m in M for a in A for d in D for t in T))

# Comprobación de Output
print("Restricción 12 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 13
# Si hay personal médico suficiente, se puede hacer la operación.
model.addConstrs((lib[a, d, t] >= REQ[p, a] * x[p, m, d, t]
                 for p in P for m in M for a in A for d in D for t in T))

# Comprobación de Output
print("Restricción 13 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a

# Restricción 14
# Si dos pacientes están disponibles en la misma hora con el mismo médico se atiende al que esté primero en la lista.
for p in P:
    for j in range(1, len(P) - p + 1):
        for m in M:
            for d in D:
                for t in T:

                    DISPp = 0
                    DISPj = 0

                    if [m, d, t] in Pacientes[p - 1].disponible:
                        DISPp = 1

                    if [m, d, t] in Pacientes[p - 1 + j].disponible:
                        DISPj = 1

                    model.addConstr(
                        1 - (DISPp * x[p, m, d, t]) >= DISPj * x[(p + j), m, d, t])

# Comprobación de Output
print("Restricción 14 - Ok")
check_a = time()
print(check_a-check_p)
print()
check_p = check_a


# Restricción 15
# Si dos pacientes, uno con prioridad y uno normal, estñan disponibles a la misma hora (durante las primeras horas de la mañana) se la asigna la hora al prioritario.
for p in P:
    for j in P:
        if Pacientes[j - 1].prioridad == True:
            if j != p:
                for m in M:
                    for d in D:
                        for t in T_PRI:

                            DISPj = 0
                            DISPp = 0

                            if [m, d, t] in Pacientes[j - 1].disponible:
                                DISPj = 1

                            if [m, d, t] in Pacientes[p - 1].disponible:
                                DISPp = 1

                            model.addConstr(
                                1 - (DISPj * x[j, m, d, t]) >= DISPp * x[p, m, d, t])

# Comprobación de Output
print("Restricción 15 - Ok")
check_restr_f = time()
print(check_restr_f-check_p)
print()
check_p = check_restr_f

# Tiempo de Restricciones
t_restricciones = check_restr_f-check_restr_i

model.optimize()


# SOLUCIÓN
model.printAttr("X")

lista_datos = []
lista_datos.append(["Tiempo de Ejecución (s)", model.runtime])
lista_datos.append(["Valor de la Función Objetivo", model.objVal])
lista_datos.append(["Nodos utilizados", model.NodeCount])

guardar_variables(model.getVars(), Pacientes, P, M, D, lista_datos)


# Registro de tiempos
lista_tiempos = []
lista_tiempos.append(["Índices", t_indices])
lista_tiempos.append(["Clase - Pacientes", t_clases_pacientes])
lista_tiempos.append(["Jornadas", t_jornadas])
lista_tiempos.append(["Parámetros", t_parametros])
lista_tiempos.append(["Función Objetivo", t_FO])
lista_tiempos.append(["Variables", t_variables])
lista_tiempos.append(["Restricciones", t_restricciones])

registro_tiempos(lista_tiempos)


# HACER: Calcular horas en operación de cada médico
#y = model.addVars(P, M, D, T, vtype=GRB.BINARY, name="y")

print()
lista_medicos = []
for m in M:

    sum_y = 0
    for p in P:
        for d in D:
            for t in T:
                sum_y += y[p, m, d, t].x

                """if m == 1:
                    print(f"y[{p}, {m}, {d}, {t}] = {y[p, m, d, t].x}")"""

    """if m == 1:
        print(f"M = 1, {sum_y}")"""

    lista_medicos.append([m, int(sum_y)])

registro_medicos(lista_medicos)
