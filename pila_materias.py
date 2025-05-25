import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Diccionario de materias y sus créditos
MATERIAS_CREDITOS = {
    "Calculo I": 4,
    "Calculo II": 4,
    "Calculo III": 4,
    "Calculo IV": 4,
    "Programacion I": 3,
    "Programacion II": 3,
    "Programacion III": 3,
    "Estadistica I": 4,
    "Estadistica II": 4,
    "Estadistica Matematica": 4,
    "Teoria de la Administracion I": 4,
    "Tecnicas de la Administracion II": 4,
    "Laboratorio I": 2,
    "Laboratorio II": 2,
    "Programacion Numerica": 2,
    "Programacion No Numerica I": 3,
    "Programacion No Numerica II": 4,
}

# Listas de grupos excluyentes 
grupos_excluyentes = [
    ["Calculo I", "Calculo II", "Calculo III", "Calculo IV"],
    ["Programacion I", "Programacion II", "Programacion III"],
    ["Estadistica I", "Estadistica II", "Estadistica Matematica"],
    ["Teoria de la Administracion I", "Tecnicas de la Administracion II"],
    ["Laboratorio I", "Laboratorio II"],
    ["Programacion No Numerica I", "Programacion No Numerica II"]
]

def VentanaMaterias():
    ventana = tk.Toplevel()
    ventana.title("Inclusión de Materias")
    ventana.geometry("650x400")

    
    frame_entrada = tk.Frame(ventana)
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Materia:").pack(side=tk.LEFT)
    entrada_materia = tk.Entry(frame_entrada, width=40)
    entrada_materia.pack(side=tk.LEFT, padx=5)

    
    frame_tablas = tk.Frame(ventana)
    frame_tablas.pack(pady=10, fill="both", expand=True)

    # Tabla de materias disponibles
    tabla_materias = ttk.Treeview(frame_tablas, columns=("materia", "uc"), show="headings", height=10)
    tabla_materias.heading("materia", text="Materia")
    tabla_materias.heading("uc", text="UC")
    tabla_materias.column("materia", width=200)
    tabla_materias.column("uc", width=50)
    tabla_materias.pack(side="left", padx=10)

    # Llenar la tabla con las materias disponibles
    for materia, uc in MATERIAS_CREDITOS.items():
        tabla_materias.insert("", "end", values=(materia, uc))

    # Tabla de materias seleccionadas
    tabla_seleccionadas = ttk.Treeview(frame_tablas, columns=("materia", "uc"), show="headings", height=10)
    tabla_seleccionadas.heading("materia", text="Materia Seleccionada")
    tabla_seleccionadas.heading("uc", text="UC")
    tabla_seleccionadas.column("materia", width=200)
    tabla_seleccionadas.column("uc", width=50)
    tabla_seleccionadas.pack(side="right", padx=10)

    materias_agregadas = set()

    
    # Botón para agregar la materia
    tk.Button(ventana, text="Agregar").pack()


