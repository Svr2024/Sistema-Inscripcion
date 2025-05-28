import tkinter as tk
from tkinter import ttk
from pila_materias import VentanaMaterias
from Lista import Lista,Nodo
from Estudiante import Estudiante

class VentanaInscripcion(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Lista de Inscripción")
        self.geometry("850x650")

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
        frame_tabla.pack(fill="x", expand=True, padx=10)

        columnas = ("cedula", "nombre", "carrera", "prioridad", "estado" )
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=5)
        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=150)
        self.tabla.pack(fill="x", padx=30)
        
        self.tabla.bind("<<TreeviewSelect>>", lambda e: self.autocompletar_desde_tabla(self.tabla))
         # Cargar datos desde archivo tickets.txt
        self.cargar_datos_desde_archivo()

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

        btn_cancelar = tk.Button(frame_botones, text="Cancelar inscripción")
        btn_cancelar.pack(side=tk.LEFT, padx=5)

        btn_eliminar = tk.Button(frame_botones, text="Eliminar registro")
        btn_eliminar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = tk.Button(frame_botones, text="Limpiar campos", command=self.limpiar_campos)
        btn_limpiar.pack(side=tk.LEFT, padx=5)

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
        
        self.lista_inscritos = Lista()
        self.lista_tickets = Lista() 
        
        self.autocompletar_desde_tabla(self.tabla)


    def abrir_ventana_materias(self):
        
        VentanaMaterias(self)

    def actualizar_materias_confirmadas(self, lista_materias):
        # Limpia tabla y actualiza con lista de materias recibidas
        self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())
        for materia in lista_materias:
    
            from pila_materias import MATERIAS_CREDITOS  
            uc = MATERIAS_CREDITOS.get(materia, 0)
            self.tabla_materias_confirmadas.insert("", "end", values=(materia, uc))
    def cargar_datos_desde_archivo(self, archivo="tickets.txt"):
     try:
        pendientes = []
        inscritos = []

        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue

                partes = linea.split(" - ")
                if len(partes) < 4:
                    continue

                cedula = partes[0].strip()
                nombre = partes[1].strip()
                carrera = partes[2].strip()
                prioridad = partes[3].replace("Prioridad:", "").strip()

                estado = "Desconocido"
                for parte in partes:
                    if "Estado:" in parte:
                        estado = parte.replace("Estado:", "").strip()
                        break

                registro = (cedula, nombre, carrera, prioridad, estado)

                if estado.lower() == "inscrito":
                    inscritos.append(registro)
                else:
                    pendientes.append(registro)

        
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # Insertar primero pendientes, luego inscritos
        for reg in pendientes + inscritos:
            self.tabla.insert("", "end", values=reg)

     except FileNotFoundError:
          print(f"No se encontró el archivo {archivo}")
     except Exception as e:
         print(f"Error leyendo {archivo}: {e}")
         

    def limpiar_campos(self):
        for entry in self.entradas.values():
            entry.delete(0, tk.END)
        self.tabla.selection_set('')
        self.autocompletar_desde_tabla(self.tabla)
         
    def autocompletar_desde_tabla(self, tree):
        selected = tree.selection()
        if selected:
            item = tree.item(selected[0])
            for key, value in zip(self.entradas.keys(), item["values"]):
                self.entradas[key].delete(0, tk.END)
                self.entradas[key].insert(0, value)
        else:
            item = tree.item('I001')
            for key, value in zip(self.entradas.keys(), item["values"]):
                self.entradas[key].delete(0, tk.END)
                self.entradas[key].insert(0, value)
            
    # Actualizar turno
    def actualizar_turno(self, archivo="tickets.txt"):
     try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(" - ")
                if len(partes) < 4:
                    continue

                cedula = partes[0].strip()

                estado = "Desconocido"
                for parte in partes:
                    if "Estado:" in parte:
                        estado = parte.replace("Estado:", "").strip()
                        break

                if estado.lower() != "inscrito":
                    self.textturno.config(state="normal")
                    self.textturno.delete(0, tk.END)
                    self.textturno.insert(0, cedula)
                    self.textturno.config(state="readonly")
                    break  # Solo el primer pendiente
            else:
                # Si no hay pendientes, se borra el campo porque ya se atendieron  todos
                self.textturno.config(state="normal")
                self.textturno.delete(0, tk.END)
                self.textturno.insert(0, "Sin pendientes")
                self.textturno.config(state="readonly")
     except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
     except Exception as e:
        print(f"Error leyendo {archivo}: {e}")

        
    def actualizar_campos_desde_archivo(self, archivo="tickets.txt"):
     try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(" - ")
                if len(partes) < 4:
                    continue

                cedula = partes[0].strip()
                nombre = partes[1].strip()
                carrera = partes[2].strip()
                prioridad = partes[3].replace("Prioridad:", "").strip()

                estado = "Desconocido"
                for parte in partes:
                    if "Estado:" in parte:
                        estado = parte.replace("Estado:", "").strip()
                        break

                # Solo llenamos campos si el estado es Pendiente
                if estado.lower() != "inscrito":
                    self.entradas["cedula"].delete(0, tk.END)
                    self.entradas["cedula"].insert(0, cedula)

                    self.entradas["nombre"].delete(0, tk.END)
                    self.entradas["nombre"].insert(0, nombre)

                    self.entradas["carrera"].delete(0, tk.END)
                    self.entradas["carrera"].insert(0, carrera)

                    self.entradas["prioridad"].delete(0, tk.END)
                    self.entradas["prioridad"].insert(0, prioridad)
                    break  # Solo el primer PENDIENTE
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
        with open("tickets.txt", "r", encoding="utf-8") as f:
            lineas = f.readlines()
      except FileNotFoundError:
        tk.messagebox.showerror("Error", "No se encontró el archivo tickets.txt.")
        return

      encontrado = False
      nuevas_lineas = []
      for linea in lineas:
        partes = linea.strip().split(" - ")
        if partes and partes[0].strip() == cedula:
            encontrado = True
            continue
        nuevas_lineas.append(linea)

      if not encontrado:
        tk.messagebox.showerror("Error", f"No existe un ticket para la cédula {cedula}.")
        return

      estudiante = Estudiante(cedula, nombre, carrera, prioridad, materias, estado="Inscrito")

    # Registrar en la lista 
      if not self.lista_inscritos.Llena():
        if self.lista_inscritos.Vacia():
            self.lista_inscritos.InsComienzo(estudiante)
        else:
            p = self.lista_inscritos.Primero
            while p.prox is not None:
                p = p.prox
            self.lista_inscritos.InsDespues(p, estudiante)
      else:
        tk.messagebox.showerror("Error", "No se pudo inscribir al estudiante, lista llena.")
        return

      nueva_linea = f"{estudiante.cedula} - {estudiante.nombre} - {estudiante.carrera} - Prioridad: {estudiante.prioridad} - Materias : {estudiante.materias} - Estado: Inscrito\n"
      nuevas_lineas.append(nueva_linea)

      try:
        with open("tickets.txt", "w", encoding="utf-8") as f:
            f.writelines(nuevas_lineas)

        tk.messagebox.showinfo("Éxito", f"Estudiante {estudiante.nombre} inscrito correctamente.")

        self.tabla.delete(*self.tabla.get_children())
        self.cargar_datos_desde_archivo()
        self.actualizar_turno()
        self.actualizar_campos_desde_archivo()
        self.tabla_materias_confirmadas.delete(*self.tabla_materias_confirmadas.get_children())

      except Exception as e:
        tk.messagebox.showerror("Error", f"No se pudo actualizar el archivo: {e}")
  