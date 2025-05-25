import tkinter as tk
from tkinter import ttk
from pila_materias import VentanaMaterias

def VentanaInscripcion():
    ventana = tk.Toplevel()
    ventana.title("Lista de Inscripción")
    ventana.geometry("700x650")

    contenedor = tk.Canvas(ventana)
    scrollbar = tk.Scrollbar(ventana, orient="vertical", command=contenedor.yview)
    frame_contenido = tk.Frame(contenedor)

    frame_contenido.bind(
        "<Configure>",
        lambda e: contenedor.configure(scrollregion=contenedor.bbox("all"))
    )

    contenedor.create_window((0, 0), window=frame_contenido, anchor="nw")
    contenedor.configure(yscrollcommand=scrollbar.set)

    # --------------------------
    # Turno
    # --------------------------
    frame_turno = tk.Frame(frame_contenido)
    frame_turno.pack(pady=10)
    tk.Label(frame_turno, text="Turno:").pack(side=tk.LEFT, padx=5)
    textturno = tk.Entry(frame_turno)
    textturno.pack(side=tk.LEFT)

    # --------------------------
    # Buscar
    # --------------------------
    frame_buscar = tk.Frame(frame_contenido)
    frame_buscar.pack(pady=5)
    tk.Label(frame_buscar, text="Buscar:").pack(side=tk.LEFT, padx=5)
    entry_buscar = tk.Entry(frame_buscar)
    entry_buscar.pack(side=tk.LEFT)

    # --------------------------
    # Tabla principal 
    # --------------------------
    frame_tabla = tk.Frame(frame_contenido)
    frame_tabla.pack(fill="x", expand=True, padx=10)

    columnas = ("cedula", "nombre", "carrera", "prioridad", "estado" )
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=5)
    for col in columnas:
        tabla.heading(col, text=col.capitalize())
        tabla.column(col, width=150)
    tabla.pack(fill="x", padx=30)

    # --------------------------
    # Campos de entrada
    # --------------------------
    frame_form = tk.Frame(frame_contenido)
    frame_form.pack(pady=10)

    etiquetas = ["Cédula", "Nombre", "Carrera", "Prioridad"]
    entradas = {}

    for i, campo in enumerate(etiquetas):
        tk.Label(frame_form, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        entry = tk.Entry(frame_form)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entradas[campo.lower()] = entry

    # --------------------------
    # Botón: Incluir materias
    # --------------------------
    btn_materias = tk.Button(frame_contenido, text="Incluir materias", command=VentanaMaterias)
    btn_materias.pack(pady=10)

    # --------------------------
    # Tabla de materias
    # --------------------------
    frame_materias = tk.Frame(frame_contenido)
    frame_materias.pack(pady=5)

    scrollbar_materias = tk.Scrollbar(frame_materias, orient="vertical")
    tabla_materias = ttk.Treeview(
        frame_materias,
        columns=("materia", "uc"),
        show="headings",
        height=4,
        yscrollcommand=scrollbar_materias.set
    )
    scrollbar_materias.config(command=tabla_materias.yview)

    tabla_materias.heading("materia", text="Materia")
    tabla_materias.heading("uc", text="UC")
    tabla_materias.column("materia", width=200)
    tabla_materias.column("uc", width=50)

    tabla_materias.pack(side="left")
    scrollbar_materias.pack(side="right", fill="y")

    # --------------------------
    # Botón: Inscribir alumno
    # --------------------------
    btn_inscribir_alumno = tk.Button(frame_contenido, text="Inscribir")
    btn_inscribir_alumno.pack(pady=5)
    
     # --------------------------
    # Botón: Historial de Ingresados
    # --------------------------
    btn_inscribir_alumno = tk.Button(frame_contenido, text="Ver ingresados")
    btn_inscribir_alumno.pack(pady=6)

    # --------------------------
    # scroll
    # --------------------------
    contenedor.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
