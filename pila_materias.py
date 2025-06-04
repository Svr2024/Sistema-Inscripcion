import tkinter as tk
from tkinter import ttk, messagebox
from Pila import Pila  


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

# Grupos de materias excluyentes
grupos_excluyentes = [
    ["Calculo I", "Calculo II", "Calculo III", "Calculo IV"],
    ["Programacion I", "Programacion II", "Programacion III"],
    ["Estadistica I", "Estadistica II", "Estadistica Matematica"],
    ["Teoria de la Administracion I", "Tecnicas de la Administracion II"],
    ["Laboratorio I", "Laboratorio II"],
    ["Programacion No Numerica I", "Programacion No Numerica II"]
]

# Límite de créditos permitidos
MAX_CREDITOS = 16

# --- Copied center_window helper here to avoid circular import ---
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


def VentanaMaterias(ventana_inscripcion=None):
    ventana = tk.Toplevel()
    ventana.title("Inclusión de Materias")
    ventana.configure(bg="white")
    ventana.geometry("750x450")
    center_window(ventana, 750, 450)

    # --------------------------
    # Botón Atrás
    # --------------------------
    def regresar_a_principal():
        ventana.destroy()
        if ventana_inscripcion:
            ventana_inscripcion.deiconify()
    frame_atras = tk.Frame(ventana, bg="white")
    frame_atras.pack(anchor="w", pady=(5, 0), padx=5)
    btn_atras = tk.Button(frame_atras, text="← Atrás", command=regresar_a_principal, bg="#183386", fg="white")
    btn_atras.pack(side=tk.LEFT)

    pila_materias = Pila()  # Crear pila para materias seleccionadas

    frame_entrada = tk.Frame(ventana, bg="white")
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Materia:", bg="white").pack(side=tk.LEFT)
    entrada_materia = tk.Entry(frame_entrada, width=40, bg="#183386", fg="white")
    entrada_materia.pack(side=tk.LEFT, padx=5)

    # Botón Agregar
    boton_agregar = tk.Button(frame_entrada, text="Agregar", bg="#183386", fg="white")
    boton_agregar.pack(side=tk.LEFT, padx=10)

    frame_tablas = tk.Frame(ventana, bg="white")
    frame_tablas.pack(pady=10, fill="both", expand=True)
    
    # === Filtro de búsqueda de materias disponibles ===
    frame_busqueda = tk.Frame(frame_tablas, bg="white")
    frame_busqueda.pack(side="left", fill="x", padx=10)

    tk.Label(frame_busqueda, text="Buscar Materia Disponible:", bg="white").pack(anchor="w")
    entrada_busqueda = tk.Entry(frame_busqueda, width=30, bg="#183386", fg="white")
    entrada_busqueda.pack(anchor="w", pady=(0, 5))
    

    # Scroll para tabla de materias disponibles
    scrollbar_materias = tk.Scrollbar(frame_busqueda, bg="white")
    scrollbar_materias.pack(side="right", fill="y")
    style = ttk.Style()
    style.theme_use("default")

    style.configure("Treeview.Heading", background="#003366", foreground="#FFFFFF", font=('Arial', 10, 'bold'))
    style.configure("Treeview", background="#E6EDFF", foreground="#000000", fieldbackground="#FFFFFF", font=('Arial', 10))
    style.map("Treeview", background=[('selected', '#cce5ff')], foreground=[('selected', '#000000')])
      
    tabla_materias = ttk.Treeview(frame_busqueda, columns=("materia", "uc"), show="headings", height=10, yscrollcommand=scrollbar_materias.set)
    tabla_materias.heading("materia", text="Materia")
    tabla_materias.heading("uc", text="UC")
    tabla_materias.column("materia", width=200)
    tabla_materias.column("uc", width=50)
    tabla_materias.pack(side="left", fill="y")
    
    scrollbar_materias.config(command=tabla_materias.yview)

    # Scroll para tabla de materias seleccionadas
    frame_seleccionadas = tk.Frame(frame_tablas, bg="white")
    frame_seleccionadas.pack(side="right", padx=10)

    # Etiqueta para mostrar el total de UC seleccionadas
    # Se crea una StringVar para que la etiqueta se actualice dinámicamente
    total_uc_var = tk.StringVar(value=f"Total UC: 0 / {MAX_CREDITOS}")
    tk.Label(frame_seleccionadas, textvariable=total_uc_var, bg="white", font=("Arial", 10, "bold")).pack(pady=5)


    scrollbar_seleccionadas = tk.Scrollbar(frame_seleccionadas)
    scrollbar_seleccionadas.pack(side="right", fill="y")

    tabla_seleccionadas = ttk.Treeview(frame_seleccionadas, columns=("materia", "uc"), show="headings", height=10, yscrollcommand=scrollbar_seleccionadas.set)
    tabla_seleccionadas.heading("materia", text="Materia Seleccionada")
    tabla_seleccionadas.heading("uc", text="UC")
    tabla_seleccionadas.column("materia", width=200)
    tabla_seleccionadas.column("uc", width=50)
    tabla_seleccionadas.pack(side="left", fill="y")

    scrollbar_seleccionadas.config(command=tabla_seleccionadas.yview)

    # Botón para remover la última materia seleccionada
    def remover_ultima_materia_seleccionada():
        if pila_materias.Vacia():
            messagebox.showwarning("Advertencia", "No hay materias seleccionadas para remover.")
            return

        # Remover de la pila
        materia_removida = pila_materias.Remover()
        if materia_removida:
            # Remover de la tabla (el último elemento insertado)
            # Los children se obtienen en el orden de inserción
            children_ids = tabla_seleccionadas.get_children()
            if children_ids:
                last_item_id = children_ids[-1]
                tabla_seleccionadas.delete(last_item_id)
                actualizar_total_uc() # Actualizar el total de UC
                messagebox.showinfo("Removida", f"Materia '{materia_removida}' removida.")
            else:
                # Esto no debería ocurrir si la pila no está vacía, pero es una protección
                messagebox.showerror("Error", "Error al remover de la tabla.")
        else:
            messagebox.showerror("Error", "No se pudo remover la materia de la pila.")

    btn_remover_ultima = tk.Button(ventana, text="Remover Última Materia Seleccionada", command=remover_ultima_materia_seleccionada, bg="#D32F2F", fg="white")
    btn_remover_ultima.pack(pady=9)


    # Llenar tabla de materias disponibles
    for materia, uc in MATERIAS_CREDITOS.items():
        tabla_materias.insert("", "end", values=(materia, uc))
        
    # Diccionario normalizado para búsqueda insensible a mayúsculas/minúsculas
    materias_normalizadas = {materia.lower(): materia for materia in MATERIAS_CREDITOS}
    
    def obtener_creditos_totales():
        total = 0
        for item in tabla_seleccionadas.get_children():
            # Usar un try-except para evitar errores si los valores no son números
            try:
                uc = int(tabla_seleccionadas.item(item, "values")[1])
                total += uc
            except (ValueError, IndexError):
                pass # Manejar casos donde 'uc' no es un número o no existe
        return total

    def actualizar_total_uc():
        current_total = obtener_creditos_totales()
        total_uc_var.set(f"Total UC: {current_total} / {MAX_CREDITOS}")

    def esta_en_grupo_excluyente(nueva_materia):
        for grupo in grupos_excluyentes:
            if nueva_materia in grupo:
                for item in tabla_seleccionadas.get_children():
                    materia = tabla_seleccionadas.item(item, "values")[0]
                    if materia in grupo:
                        return True
        return False

    def agregar_materia():
        # Normalizar el texto ingresado para evitar problemas de mayúsculas/minúsculas o espacios
        materia_input = entrada_materia.get().strip()
        
        if not materia_input: # Simplificado para campo vacío
            messagebox.showwarning("Advertencia", "Ingrese al menos una materia.")
            return

        # Buscar la materia en el diccionario normalizado
        materia_encontrada = materias_normalizadas.get(materia_input.lower())

        # Validar si la materia existe en el diccionario
        if not materia_encontrada:
            messagebox.showerror("Error", f"La materia '{materia_input}' no existe, por favor verifique en la tabla de Materias su existencia.")
            return

        # Usar la materia encontrada (con el formato correcto) para las validaciones posteriores
        materia = materia_encontrada
        
        # Verificar si ya está en la pila (materias seleccionadas)
        if materia in pila_materias.obtener_contenido():
            messagebox.showinfo("Duplicado", "Esta materia ya fue agregada.")
            return
            
        if esta_en_grupo_excluyente(materia):
            messagebox.showwarning("Conflicto", f"La materia '{materia}' pertenece a un grupo excluyente y ya tienes una materia de ese grupo inscrita.")
            return
            
        uc = MATERIAS_CREDITOS[materia]
        creditos_actuales = obtener_creditos_totales()
        if creditos_actuales + uc > MAX_CREDITOS:
            messagebox.showerror("Límite", f"Agregar '{materia}' excede el límite de {MAX_CREDITOS} UC.")
            return

        # Agregar a pila y tabla seleccionada
        pila_materias.Insertar(materia)
        tabla_seleccionadas.insert("", "end", values=(materia, uc))
        entrada_materia.delete(0, tk.END)
        actualizar_total_uc() # Actualizar el total de UC

    boton_agregar.config(command=agregar_materia)

    def confirmar_materias():
        if ventana_inscripcion is None:
            messagebox.showwarning("Error", "No se proporcionó referencia a ventana de inscripción.")
            return
        # Obtener lista de materias de la pila 
        materias = pila_materias.obtener_contenido()
        if not materias:
            messagebox.showinfo("Información", "No hay materias para confirmar.")
            return
        # Pasando a la ventana de Inscripcion 
        try:
            ventana_inscripcion.actualizar_materias_confirmadas(materias)
            messagebox.showinfo("Éxito", "Materias confirmadas y pasadas a inscripción.")
            ventana.destroy()  
        except AttributeError:
            messagebox.showerror("Error", "Ha ocurrido un error inesperado al pasar las materias. Asegúrese de que la ventana de inscripción tiene el método 'actualizar_materias_confirmadas'.")

    # Botón Confirmar Materias 
    boton_confirmar = tk.Button(ventana, text="Confirmar materias", command=confirmar_materias, bg="#183386", fg="white")
    boton_confirmar.pack(pady=10)
    
    def filtrar_materias(event=None):
        busqueda = entrada_busqueda.get().strip().lower()
        for item in tabla_materias.get_children():
            tabla_materias.delete(item)
        for materia, uc in MATERIAS_CREDITOS.items():
            if busqueda in materia.lower() or busqueda == str(uc):
                tabla_materias.insert("", "end", values=(materia, uc))
    
    entrada_busqueda.bind("<KeyRelease>", filtrar_materias)
    
    # Función para manejar doble clic en tabla de materias
    def seleccionar_materia_doble_clic(event):
        item = tabla_materias.selection()
        if item:
            valores = tabla_materias.item(item[0], "values")
            materia = valores[0]
            uc = int(valores[1])
            respuesta = messagebox.askyesno("Agregar Materia", f"¿Deseas agregar '{materia}' con {uc} UC?")
            if respuesta:
                # Duplicación de lógica, idealmente refactorizar en una función común
                if materia in pila_materias.obtener_contenido():
                    messagebox.showinfo("Duplicado", "Esta materia ya fue agregada.")
                    return
                if esta_en_grupo_excluyente(materia):
                    messagebox.showwarning("Conflicto", f"La materia '{materia}' pertenece a un grupo excluyente y ya tienes una materia de ese grupo inscrita.")
                    return
                creditos_actuales = obtener_creditos_totales()
                if creditos_actuales + uc > MAX_CREDITOS:
                    messagebox.showerror("Límite", f"Agregar '{materia}' excede el límite de {MAX_CREDITOS} UC.")
                    return
                pila_materias.Insertar(materia)
                tabla_seleccionadas.insert("", "end", values=(materia, uc))
                entrada_materia.delete(0, tk.END)
                actualizar_total_uc() # Actualizar el total de UC
    
    # Función para rellenar el campo de entrada al seleccionar una materia
    def seleccionar_materia_clic(event):
        seleccion = tabla_materias.selection()
        if seleccion:
            valores = tabla_materias.item(seleccion[0], 'values')
            entrada_materia.delete(0, tk.END)
            entrada_materia.insert(0, valores[0])
    
    # Configurar ambos eventos: doble clic para agregar y clic para seleccionar
    tabla_materias.bind("<Double-1>", seleccionar_materia_doble_clic)
    tabla_materias.bind("<ButtonRelease-1>", seleccionar_materia_clic)

    # Actualizar el total de UC al iniciar la ventana (si ya hay materias en la pila)
    actualizar_total_uc()

    return ventana