from random import choice


class Paciente:
    # def __init__(self, numero, prioridad, examenes, insumos, duracion, personal, costo_insumo):
    def __init__(self, numero, prioridad, examenes, insumos, lista_disponibles):
        self.numero = numero
        self.prioridad = prioridad
        self.examenes = examenes
        self.insumos = insumos
        self.disponible = lista_disponibles

    def __str__(self):
        """text = f"Paciente: {self.numero}\n\
    Duración: {self.duracion}\n\
    Personal: {self.personal}\n\
    Costos Insums: {self.costo_insumo}\n"""

        text = f"Paciente: {self.numero}\n\
    Prioridad: {self.prioridad}\n\
    Exámenes: {self.examenes}\n\
    Insumos: {self.insumos}\n\
    Disponible: {self.disponible}"

        return text
