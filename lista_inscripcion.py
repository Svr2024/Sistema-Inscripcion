from pila_materias import Pila  
import tkinter as tk
from tkinter import ttk
from pila_materias import VentanaMaterias
from Lista import Lista
from dbJson import Db_json

# Helper to center a window on the screen
def center_window(win, width=None, height=None):
    win.update_idletasks()
    if width is None or height is None:
        win_width = win.winfo_width()
        win_height = win.winfo_height()
        if win_width == 1 or win_height == 1:  # Not yet drawn
            win_width = win.winfo_reqwidth()
            win_height = win.winfo_reqheight()
    else:
        win_width = width
        win_height = height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (win_width // 2)
    y = (screen_height // 2) - (win_height // 2)
    win.geometry(f"{win_width}x{win_height}+{x}+{y}")

class VentanaInscripcion(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de Inscripción")
        self.geometry("850x650")
        self.pila_cambios = Pila()
        center_window(self, 850, 650)

        contenedor = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=contenedor.yview)
        self.frame_contenido = tk.Frame(contenedor)
        
        # --------------------------
        # Botón Atrás
        # --------------------------
        def regresar_a_principal():
            self.destroy()
            if self.master:
                self.master.deiconify()
        frame_atras = tk.Frame(self.frame_contenido)
        frame_atras.pack(anchor="w", pady=(5, 0), padx=5)
        btn_atras = tk.Button(frame_atras, text="← Atrás", command=regresar_a_principal)
        btn_atras.pack(side=tk.LEFT)

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
        self.actualizar_turno()

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
        frame_tabla.pack(fill="both", expand=True, padx=10)

        scrollbar_tabla = tk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar_tabla.pack(side="right", fill="y")

        columnas = ("cedula", "nombre", "carrera", "prioridad", "estado")
        self.tabla = ttk.Treeview(
            frame_tabla,
            columns=columnas,
            show="headings",
            height=8,
            yscrollcommand=scrollbar_tabla.set
            )
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar_tabla.config(command=self.tabla.yview)
        
        # Cargar datos desde archivo estudiante.json
        self.cargar_datos_desde_archivo()
        
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.autocompletar_desde_tabla(self.tabla))
        

        # --------------------------
        # Campos de entrada
        # --------------------------
        frame_form = tk.Frame(self.frame_contenido)
        frame_form.pack(pady=10)

        etiquetas = ["Cedula", "Nombre", "Carrera", "Prioridad"]
        self.entradas = {}

        for i, campo in enumerate(etiquetas):
            tk.Label(frame_form, text=campo).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = tk.Entry(frame_form)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entradas[campo.lower()] = entry
            
        # Actualizar textboxs con el primer registro
        self.actualizar_campos_desde_archivo()


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
        # Botones Principales
        # --------------------------
        frame_botones = tk.Frame(self.frame_contenido)
        frame_botones.pack(pady=5)

        btn_inscribir_alumno = tk.Button(frame_botones, text="Inscribir", command=self.inscribir_alumno)
        btn_inscribir_alumno.pack(side=tk.LEFT, padx=5)

        btn_cancelar = tk.Button(frame_botones, text="Cancelar inscripción", command=self.cancelar_inscripcion)
        btn_cancelar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar registro")
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(frame_botones, text="Limpiar campos", command=self.limpiar_campos)
        btn_limpiar.pack(side=tk.LEFT, padx=5)

        # --------------------------
        # Botón: Historial de Ingresados
        # --------------------------
        btn_ver_ingresados = tk.Button(self.frame_contenido, text="Ver ingresados", command=self.abrir_ventana_ingresados)
        btn_ver_ingresados.pack(pady=6)

        # --------------------------
        # Scroll
        # --------------------------
        contenedor.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.lista_inscritos = Lista()
        self.lista_tickets = Lista() 
        
        self.autocompletar_desde_tabla(self.tabla)
        self.entry_buscar.bind("<KeyRelease>", self.buscar_por_cedula)
    
    def buscar_por_cedula(self, event=None):
        texto = self.entry_buscar.get().strip()
        if not texto:
            self.cargar_datos_desde_archivo()
            return

        texto = texto.lower()
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        try:
            estudiantes = Db_json.cargar_estudiantes_json("estudiantes.json")

            busqueda = list(filter( lambda estudiante: texto in estudiante.cedula , estudiantes))

            for estudiante in busqueda:
                self.tabla.insert("", "end", values=(estudiante.cedula, estudiante.nombre, estudiante.carrera, estudiante.prioridad, estudiante.estado))

        except Exception as e:
            print(f"Error al filtrar por cédula: {e}")

    def abrir_ventana_ingresados(self):
    # Crear una nueva ventana para mostrar los inscritos
        ventana_ingresados = tk.Toplevel(self)
        ventana_ingresados.title("Lista de Ingresados")
        ventana_ingresados.geometry("600x400")
    
    # Crear un Treeview para mostrar los inscritos
        columnas = ("cedula", "nombre", "carrera", "prioridad")
        tabla_inscritos = ttk.Treeview(ventana_ingresados, columns=columnas, show="headings")

        for col in columnas:
            tabla_inscritos.heading(col, text=col.capitalize())
            tabla_inscritos.column(col, width=100)

        tabla_inscritos.pack(fill="both", expand=True)

    # Botón para cerrar la ventana
        btn_cerrar = tk.Button(ventana_ingresados, text="Cerrar", command=ventana_ingresados.destroy)
        btn_cerrar.pack(pady=10)

    # Obtener las carreras registradas
        carreras_registradas = set()
        p = self.lista_inscritos.Primero
        while p is not None:
            carreras_registradas.add(p.info.carrera)
            p = p.prox

        lista_carreras = sorted(carreras_registradas)
        lista_carreras.insert(0, "Todas las carreras")

        kfccombobox_filtro = ttk.Combobox(ventana_ingresados, values=lista_carreras, state="readonly")
        kfccombobox_filtro.pack(pady=5)
        kfccombobox_filtro.set("Todas las carreras")

        kfccombobox_filtro.bind("<<ComboboxSelected>>", lambda e: self.filtrar_estudiantes_por_carrera(tabla_inscritos, kfccombobox_filtro.get()))

        self.filtrar_estudiantes_por_carrera(tabla_inscritos, "Todas las carreras")

    def obtener_inscritos(self):
        inscritos = []
        p = self.lista_inscritos.Primero
        while p is not None:
            if p.info.estado.lower() == "inscrito":
                inscritos.append((p.info.cedula, p.info.nombre, p.info.carrera, p.info.prioridad))
            p = p.prox
        return inscritos

    def filtrar_estudiantes_por_carrera(self, tabla_inscritos, carrera_seleccionada):
        # Limpiar la tabla antes de insertar nuevos datos
        for item in tabla_inscritos.get_children():
            tabla_inscritos.delete(item)

        p = self.lista_inscritos.Primero
        while p is not None:
            if carrera_seleccionada == "Todas las carreras" or p.info.carrera == carrera_seleccionada:
                tabla_inscritos.insert("", "end", values=(p.info.cedula, p.info.nombre, p.info.carrera, p.info.prioridad))
            p = p.prox

    def abrir_ventana_materias(self):
        
        VentanaMaterias(self)

    def actualizar_materias_confirmadas(self, lista_materias):
        # Limpia tabla y actualiza con lista de materias recibidas
        self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())
        for materia in lista_materias:
    
            from pila_materias import MATERIAS_CREDITOS  
            uc = MATERIAS_CREDITOS.get(materia, 0)
            self.tabla_materias_confirmadas.insert("", "end", values=(materia, uc))

    def cargar_datos_desde_archivo(self, archivo="estudiantes.json"):
        try:
            pendientes = []
            inscritos = []

            estudiantes = Db_json.cargar_estudiantes_json(archivo)
            
            inscritos = list(filter(lambda estudiante: estudiante.estado.lower() == "inscrito", estudiantes))
            
            pendientes = list(filter(lambda estudiante: estudiante.estado.lower() != "inscrito", estudiantes))
            

            for item in self.tabla.get_children():
                self.tabla.delete(item)

            # Insertar primero pendientes, luego inscritos
            for reg in pendientes + inscritos:
                self.tabla.insert("", "end", values=[reg.cedula,reg.nombre, reg.carrera, reg.prioridad, reg.estado])

        except FileNotFoundError:
            print(f"No se encontró el archivo {archivo}")
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")


    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
        self.entry_buscar.delete(0, tk.END)
        self.tabla.selection_set('')
        self.cargar_datos_desde_archivo()
        self.autocompletar_desde_tabla(self.tabla)


    def autocompletar_desde_tabla(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            print(selected[0])
            for key, value in zip(self.entradas.keys(), item["values"]):
                self.entradas[key].delete(0, tk.END)
                self.entradas[key].insert(0, value)
        else:  
            self.actualizar_campos_desde_archivo()

    # Actualizar turno
    def actualizar_turno(self, archivo="estudiantes.json"):
        try:
            estudiantes = Db_json.cargar_estudiantes_json(archivo)
            
            pendientes = list(filter(lambda estudiante: estudiante.estado == "pendiente", estudiantes))
            
            if pendientes:
                estudiante = pendientes[0]
                self.textturno.config(state="normal")
                self.textturno.delete(0, tk.END)
                self.textturno.insert(0, estudiante.cedula)
                self.textturno.config(state="readonly")
            else:
                self.textturno.config(state="normal")
                self.textturno.delete(0, tk.END)
                self.textturno.insert(0, "Sin pendientes")
                self.textturno.config(state="readonly")
        except FileNotFoundError:
            print(f"No se encontró el archivo {archivo}")
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

        
    def actualizar_campos_desde_archivo(self, archivo="estudiantes.json"):
        try:
            estudiantes = Db_json.cargar_estudiantes_json(archivo)
            
            pendientes = list(filter(lambda estudiante: estudiante.estado == "pendiente", estudiantes))
            
            if pendientes:
                estudiante = pendientes[0]
                self.entradas["cedula"].delete(0, tk.END)
                self.entradas["cedula"].insert(0, estudiante.cedula)

                self.entradas["nombre"].delete(0, tk.END)
                self.entradas["nombre"].insert(0, estudiante.nombre)

                self.entradas["carrera"].delete(0, tk.END)
                self.entradas["carrera"].insert(0, estudiante.carrera)

                self.entradas["prioridad"].delete(0, tk.END)
                self.entradas["prioridad"].insert(0, estudiante.prioridad)
                
        except FileNotFoundError:
            print(f"No se encontró el archivo {archivo}")
        except Exception as e:
            print(f"Error leyendo {archivo}: {e}")

    def inscribir_alumno(self):
        cedula = self.entradas["cedula"].get().strip()
        nombre = self.entradas["nombre"].get().strip()
        carrera = self.entradas["carrera"].get().strip()
        prioridad = self.entradas["prioridad"].get().strip()

        if not all([cedula, nombre, carrera, prioridad]):
            tk.messagebox.showerror("Error", "Todos los campos deben estar llenos.")
            return

    # Obtener materias confirmadas
        materias = []
        for item in self.tabla_materias_confirmadas.get_children():
            materia = self.tabla_materias_confirmadas.item(item, "values")[0]
            materias.append(materia)

    #  ojito no permitir inscripción sin materias
        if not materias:
            tk.messagebox.showerror("Error", "Debe confirmar al menos una materia para poder inscribir al estudiante.")
            return

        try:
            estudiantes = Db_json.cargar_estudiantes_json("estudiantes.json")
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "No se encontró el archivo estudiantes.json.")
            return

        estudiante_encontrado = None
        for estudiante in estudiantes:
            if estudiante.cedula == cedula:
                estudiante_encontrado = estudiante
                continue

        if not estudiante_encontrado:
            tk.messagebox.showerror("Error", f"No existe un ticket para la cédula {cedula}.")
            return

        estudiante_encontrado.estado = "Inscrito"
        estudiante_encontrado.materias = materias
        
        estudiantes_guardar = list()
        for estudiante in estudiantes:
            if estudiante.cedula == estudiante_encontrado.cedula:
                estudiantes_guardar.append(estudiante_encontrado)
            else:
                estudiantes_guardar.append(estudiante)


    # Registrar en la lista 
        if not self.lista_inscritos.Llena():
            if self.lista_inscritos.Vacia():
                self.lista_inscritos.InsComienzo(estudiante_encontrado)
            else:
                p = self.lista_inscritos.Primero
                while p.prox is not None:
                    p = p.prox
                self.lista_inscritos.InsDespues(p, estudiante_encontrado)
        else:
            tk.messagebox.showerror("Error", "No se pudo inscribir al estudiante, lista llena.")
            return

        try:
            Db_json.guardar_estudiantes_json(estudiantes_guardar, "estudiantes.json")

            tk.messagebox.showinfo("Éxito", f"Estudiante {estudiante_encontrado.nombre} inscrito correctamente.")

            self.tabla.delete(*self.tabla.get_children())
            self.cargar_datos_desde_archivo()
            self.actualizar_turno()
            self.actualizar_campos_desde_archivo()
            self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())

        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")


    def cancelar_inscripcion(self):
        cedula = self.entradas["cedula"].get().strip()

        if not cedula:
            tk.messagebox.showerror("Error", "No hay estudiante seleccionado para cancelar.")
            return

        try:
            estudiantes = Db_json.cargar_estudiantes_json("estudiantes.json")
        except FileNotFoundError:
            tk.messagebox.showerror("Error", "No se encontró el archivo estudiantes.json.")
            return

        pendientes = []
        inscritos = []
        estudiante_cancelado = None
        es_pendiente = False

        # Separar los registros y encontrar el que se va a cancelar
        for estudiante in estudiantes:
            # Buscar el estudiante a cancelar
            if estudiante.cedula == cedula:
                
                if estudiante.estado.lower() == "inscrito":
                    # Crear nuevo registro con estado pendiente
                    estudiante.estado = "pendiente"
                elif estudiante.estado.lower() == "pendiente":
                    es_pendiente = True
                
                estudiante_cancelado = estudiante
            elif estudiante.estado.lower() == "pendiente":
                pendientes.append(estudiante)
            elif estudiante.estado.lower() == "inscrito":
                inscritos.append(estudiante)

        if estudiante_cancelado is None:
            tk.messagebox.showerror("Error", f"No se encontró un estudiante con cédula {cedula}.")
            return

        # Si el estudiante ya era pendiente, lo quitamos de la lista de pendientes
        if es_pendiente:
            pendientes = [p for p in pendientes if not p.cedula == cedula]

        # Reconstruir el archivo:
        # 1. Pendientes originales (excepto el cancelado si era pendiente)
        # 2. Estudiante cancelado (al final de pendientes)
        # 3. Inscritos originales
        estudiantes_actualizados = pendientes + [estudiante_cancelado] + inscritos

        try:
            Db_json.guardar_estudiantes_json(estudiantes_actualizados, "estudiantes.json")

            if es_pendiente:
                tk.messagebox.showinfo("Éxito",
                                        "Estudiante pendiente reprogramado. Se ha movido al final de la lista de pendientes.")
            else:
                tk.messagebox.showinfo("Éxito",
                                        "Inscripción cancelada. El estudiante ha sido movido al final de la lista de pendientes.")

            # Actualizar la interfaz
            self.tabla.delete(*self.tabla.get_children())
            self.cargar_datos_desde_archivo()
            self.actualizar_turno()
            self.actualizar_campos_desde_archivo()
            self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())

        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")