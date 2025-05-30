class Estudiante:
    def __init__(self, cedula, nombre, carrera, prioridad,materias=[], estado="pendiente"):
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
    
    def to_dict(self):
        return {
            'cedula': self.cedula,
            'nombre': self.nombre,
            'carrera': self.carrera,
            'prioridad': self.prioridad,
            'materias': self.materias,
            'estado': self.estado
        }
