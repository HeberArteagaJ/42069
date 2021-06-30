from carga_datos import carga_parametros
import os

# PATHS & FOLDERS
Folders = {
    'base_datos': 'Base de Datos',
    'parametros': 'Parametros',
    'resultados': 'Resultados',
    'tiempos': 'Tiempos',
    'test': 'Test',
    'E2': 'Datos - E2'
}

Paths = {
    'pacientes': os.path.join(Folders['base_datos'], "Datos Pacientes.xlsx"),
    'medicos': os.path.join(Folders['base_datos'], "Datos Medicos.xlsx"),
    'parametros': os.path.join(Folders['base_datos'], "Parametros.xlsx"),
    'resultados': os.path.join(Folders['resultados'], "ResultadosR3.csv"),
    'tiempos': os.path.join(Folders['resultados'], "TiemposR3.csv"),
    'trabajo_medicos': os.path.join(Folders['resultados'], "Trabajo MedicosR3.csv")
}

Test = {
    'pacientes': os.path.join(Folders['test'], "Datos Pacientes.xlsx"),
    'medicos': os.path.join(Folders['test'], "Datos Medicos.xlsx"),
    'parametros': os.path.join(Folders['test'], "Parametros.xlsx"),
    'resultados': os.path.join(Folders['test'], "ResultadosR1.csv"),
    'tiempos': os.path.join(Folders['test'], "TiemposR1.csv"),
    'trabajo_medicos': os.path.join(Folders['test'], "Trabajo MedicosR1.csv")
}

PathsE2 = {
    'pacientes': os.path.join(Folders['E2'], Folders['base_datos'], "Datos Pacientes.xlsx"),
    'medicos': os.path.join(Folders['E2'], Folders['base_datos'], "Datos Medicos.xlsx"),
    'parametros': os.path.join(Folders['E2'], Folders['parametros'], "Parametros.xlsx"),
    'resultados': os.path.join(Folders['E2'], Folders['resultados'], "Resultados.csv")
}
# CONJUNTOS
Indices = {
    'n_P': 30,
    'M': 15,  # int(carga_parametros(Paths['parametros'], 'C2')),
    'A': 4,  # Médicos, Enfermero, TENS, anestesistas
    'S': int(carga_parametros(Paths['parametros'], 'C11')),
    'D': 10,
    'T': 96,
    'T_PRI_min': 32,
    'T_PRI_max': 48
}

# MISC
# PROB_PRIORITARIO = 0.2  # Probabilidad entre 0 y 1 de que el paciente sea prioritario
MIN_EX = 2
MAX_EX = 4

EX_T = 0.7
EX_F = 0.3

INS_T = 0.7
INS_F = 0.3

Pacientes = {
    'disp_min': 32,
    'disp_max': 80,
    'n_DISP_min': Indices['D'],
    'n_DISP_max': int(Indices['D'] * (Indices['T'] / 3))
}

# JORNADAS
Jornadas = {
    'Jornada': int(carga_parametros(Paths['parametros'], 'C12')),
    'Entrada_min': 33,
    'Entrada_max': 43
}


# PARÁMETROS
Parametros = {
    'DUR': {
        'min': int(carga_parametros(Paths['parametros'], 'C16')),
        'max': int(carga_parametros(Paths['parametros'], 'D16'))
    },
    'LIM': int(carga_parametros(Paths['parametros'], 'C13')),
    'CI': int(carga_parametros(Paths['parametros'], 'C10')),
    'CM': carga_parametros(Paths['parametros'], 'C6'),
    'PON': carga_parametros(Paths['parametros'], 'C14'),
    'POR': 0.8
}


# Personal Médico
PM = {
    'CANT_PER': {
        1: int(Indices['M']),
        2: int(carga_parametros(Paths['parametros'], 'C3')),
        3: int(carga_parametros(Paths['parametros'], 'C4')),
        4: int(carga_parametros(Paths['parametros'], 'C5'))
    },
    'CANT_PER_MIN': 10,
    'COSTOS_A': {
        1: int(Parametros['CM']),
        2: int(carga_parametros(Paths['parametros'], 'C7')),
        3: int(carga_parametros(Paths['parametros'], 'C8')),
        4: int(carga_parametros(Paths['parametros'], 'C9'))
    },
    'CANT_REQ': {
        1: {
            'min': 0,
            'max': 2
        },
        2: {
            'min': int(carga_parametros(Paths['parametros'], 'C17')),
            'max': int(carga_parametros(Paths['parametros'], 'D17'))
        },
        3: {
            'min': int(carga_parametros(Paths['parametros'], 'C18')),
            'max': int(carga_parametros(Paths['parametros'], 'D18'))
        },
        4: {
            'min': int(carga_parametros(Paths['parametros'], 'C19')),
            'max': int(carga_parametros(Paths['parametros'], 'D19'))
        }
    }
}
