class Estudiante:
    def __init__(self, cedula, nombre, carrera, prioridad,materias, estado="pendiente"):
        self.cedula = cedula
        self.nombre = nombre
        self.carrera = carrera
        self.prioridad = prioridad
        self.materias = materias
        
        self.estado = estado

    def get_info(self):
        return f"{self.cedula} - {self.nombre} - {self.carrera} - Prioridad: {self.prioridad} - Estado: {self.estado}"

    def __str__(self):
        return self.get_info()
