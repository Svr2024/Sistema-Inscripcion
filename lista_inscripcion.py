import tkinter as tk
from tkinter import ttk
from pila_materias import VentanaMaterias

class VentanaInscripcion(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de Inscripción")
        self.geometry("700x650")

        contenedor = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=contenedor.yview)
        self.frame_contenido = tk.Frame(contenedor)

        self.frame_contenido.bind(
            "<Configure>",
            lambda e: contenedor.configure(scrollregion=contenedor.bbox("all"))
        )

        contenedor.create_window((0, 0), window=self.frame_contenido, anchor="nw")
        contenedor.configure(yscrollcommand=scrollbar.set)

        # --------------------------
        # Turno
        # --------------------------
        frame_turno = tk.Frame(self.frame_contenido)
        frame_turno.pack(pady=10)
        tk.Label(frame_turno, text="Turno:").pack(side=tk.LEFT, padx=5)
        self.textturno = tk.Entry(frame_turno)
        self.textturno.pack(side=tk.LEFT)

        # --------------------------
        # Buscar
        # --------------------------
        frame_buscar = tk.Frame(self.frame_contenido)
        frame_buscar.pack(pady=5)
        tk.Label(frame_buscar, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entry_buscar = tk.Entry(frame_buscar)
        self.entry_buscar.pack(side=tk.LEFT)

        # --------------------------
        # Tabla principal 
        # --------------------------
        frame_tabla = tk.Frame(self.frame_contenido)
        frame_tabla.pack(fill="x", expand=True, padx=10)

        columnas = ("cedula", "nombre", "carrera", "prioridad", "estado" )
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=5)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)
        self.tabla.pack(fill="x", padx=30)

        # --------------------------
        # Campos de entrada
        # --------------------------
        frame_form = tk.Frame(self.frame_contenido)
        frame_form.pack(pady=10)

        etiquetas = ["Cédula", "Nombre", "Carrera", "Prioridad"]
        self.entradas = {}

        for i, campo in enumerate(etiquetas):
            tk.Label(frame_form, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(frame_form)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entradas[campo.lower()] = entry

        # --------------------------
        # Botón: Incluir materias
        # --------------------------
        btn_materias = tk.Button(self.frame_contenido, text="Incluir materias", command=self.abrir_ventana_materias)
        btn_materias.pack(pady=10)

        # --------------------------
        # Tabla de materias confirmadas
        # --------------------------
        frame_materias = tk.Frame(self.frame_contenido)
        frame_materias.pack(pady=5)

        scrollbar_materias = tk.Scrollbar(frame_materias, orient="vertical")
        self.tabla_materias_confirmadas = ttk.Treeview(
            frame_materias,
            columns=("materia", "uc"),
            show="headings",
            height=4,
            yscrollcommand=scrollbar_materias.set
        )
        scrollbar_materias.config(command=self.tabla_materias_confirmadas.yview)

        self.tabla_materias_confirmadas.heading("materia", text="Materia")
        self.tabla_materias_confirmadas.heading("uc", text="UC")
        self.tabla_materias_confirmadas.column("materia", width=200)
        self.tabla_materias_confirmadas.column("uc", width=50)

        self.tabla_materias_confirmadas.pack(side="left")
        scrollbar_materias.pack(side="right", fill="y")

        # --------------------------
        # Botón: Inscribir alumno
        # --------------------------
        btn_inscribir_alumno = tk.Button(self.frame_contenido, text="Inscribir")
        btn_inscribir_alumno.pack(pady=5)

        # --------------------------
        # Botón: Historial de Ingresados
        # --------------------------
        btn_ver_ingresados = tk.Button(self.frame_contenido, text="Ver ingresados")
        btn_ver_ingresados.pack(pady=6)

        # --------------------------
        # Scroll
        # --------------------------
        contenedor.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def abrir_ventana_materias(self):
        # Pasamos la referencia self para que la ventana materias pueda llamar actualizar_materias_confirmadas
        VentanaMaterias(self)

    def actualizar_materias_confirmadas(self, lista_materias):
        # Limpia tabla y actualiza con lista de materias recibidas
        self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())
        for materia in lista_materias:
            # Se asume que MATERIAS_CREDITOS está importado o definido globalmente
            from pila_materias import MATERIAS_CREDITOS  # Importa para obtener créditos
            uc = MATERIAS_CREDITOS.get(materia, 0)
            self.tabla_materias_confirmadas.insert("", "end", values=(materia, uc))
