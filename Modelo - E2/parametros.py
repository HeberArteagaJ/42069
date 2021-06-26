from carga_datos import carga_parametros

# PATHS
Paths = {
    'pacientes': 'Datos Pacientes.xlsx',
    'medicos': 'Datos Medicos.xlsx',
    'parametros': 'Parametros.xlsx',
}

# CONJUNTOS
Indices = {
    'n_P': 10,
    'M': 15,  # int(carga_parametros(Paths['parametros'], 'C2')),
    'A': 3,  # Enfermero, TENS, anestesistas
    'S': int(carga_parametros(Paths['parametros'], 'C11')),
    'D': 30,
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
    'PON': carga_parametros(Paths['parametros'], 'C14')
}


# Personal Médico
PM = {
    'CANT_PER': {
        1: int(carga_parametros(Paths['parametros'], 'C3')),
        2: int(carga_parametros(Paths['parametros'], 'C4')),
        3: int(carga_parametros(Paths['parametros'], 'C5'))
    },
    'CANT_PER_MIN': 10,
    'COSTOS_A': {
        1: int(carga_parametros(Paths['parametros'], 'C7')),
        2: int(carga_parametros(Paths['parametros'], 'C8')),
        3: int(carga_parametros(Paths['parametros'], 'C9'))
    },
    'CANT_REQ': {
        1: {
            'min': int(carga_parametros(Paths['parametros'], 'C17')),
            'max': int(carga_parametros(Paths['parametros'], 'D17'))
        },
        2: {
            'min': int(carga_parametros(Paths['parametros'], 'C18')),
            'max': int(carga_parametros(Paths['parametros'], 'D18'))
        },
        3: {
            'min': int(carga_parametros(Paths['parametros'], 'C19')),
            'max': int(carga_parametros(Paths['parametros'], 'D19'))
        }
    }
}
