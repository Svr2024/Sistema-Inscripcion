import json
from Estudiante import Estudiante

class Db_json:

    def guardar_estudiantes_json(estudiantes, archivo):
        # Convertir cada estudiante a diccionario
        estudiantes_dict = [est.to_dict() for est in estudiantes]
        
        
        # Escribir en el archivo JSON
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(estudiantes_dict, f, indent=4, ensure_ascii=False)

    def cargar_estudiantes_json(archivo):
    
        with open(archivo, 'r', encoding='utf-8') as f:
            estudiantes_dict = json.load(f)
    
        return [Estudiante(est['cedula'], est['nombre'], est['carrera'], est['prioridad'], est['materias'], est['estado']) 
            for est in estudiantes_dict]