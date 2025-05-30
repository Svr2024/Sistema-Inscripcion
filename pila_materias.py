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
    ventana.geometry("750x450")
    center_window(ventana, 750, 450)

    pila_materias = Pila()  # Crear pila para materias seleccionadas

    frame_entrada = tk.Frame(ventana)
    frame_entrada.pack(pady=10)

    tk.Label(frame_entrada, text="Materia:").pack(side=tk.LEFT)
    entrada_materia = tk.Entry(frame_entrada, width=40)
    entrada_materia.pack(side=tk.LEFT, padx=5)

    # Botón Agregar
    boton_agregar = tk.Button(frame_entrada, text="Agregar")
    boton_agregar.pack(side=tk.LEFT, padx=10)

    frame_tablas = tk.Frame(ventana)
    frame_tablas.pack(pady=10, fill="both", expand=True)
        # === Filtro de búsqueda de materias disponibles ===
    frame_busqueda = tk.Frame(frame_tablas)
    frame_busqueda.pack(side="left", fill="x", padx=10)

    tk.Label(frame_busqueda, text="Buscar Materia Disponible:").pack(anchor="w")
    entrada_busqueda = tk.Entry(frame_busqueda, width=30)
    entrada_busqueda.pack(anchor="w", pady=(0, 5))
    


    # Scroll para tabla de materias disponibles
    scrollbar_materias = tk.Scrollbar(frame_busqueda)
    scrollbar_materias.pack(side="right", fill="y")

    tabla_materias = ttk.Treeview(frame_busqueda, columns=("materia", "uc"), show="headings", height=10, yscrollcommand=scrollbar_materias.set)
    tabla_materias.heading("materia", text="Materia")
    tabla_materias.heading("uc", text="UC")
    tabla_materias.column("materia", width=200)
    tabla_materias.column("uc", width=50)
    tabla_materias.pack(side="left", fill="y")
   


    scrollbar_materias.config(command=tabla_materias.yview)

    # Scroll para tabla de materias seleccionadas
    frame_seleccionadas = tk.Frame(frame_tablas)
    frame_seleccionadas.pack(side="right", padx=10)

    scrollbar_seleccionadas = tk.Scrollbar(frame_seleccionadas)
    scrollbar_seleccionadas.pack(side="right", fill="y")

    tabla_seleccionadas = ttk.Treeview(frame_seleccionadas, columns=("materia", "uc"), show="headings", height=10, yscrollcommand=scrollbar_seleccionadas.set)
    tabla_seleccionadas.heading("materia", text="Materia Seleccionada")
    tabla_seleccionadas.heading("uc", text="UC")
    tabla_seleccionadas.column("materia", width=200)
    tabla_seleccionadas.column("uc", width=50)
    tabla_seleccionadas.pack(side="left", fill="y")

    scrollbar_seleccionadas.config(command=tabla_seleccionadas.yview)

    # Llenar tabla de materias disponibles
    for materia, uc in MATERIAS_CREDITOS.items():
        tabla_materias.insert("", "end", values=(materia, uc))
        
    # Diccionario normalizado para búsqueda insensible a mayúsculas/minúsculas
    materias_normalizadas = {materia.lower(): materia for materia in MATERIAS_CREDITOS}
    
    def obtener_creditos_totales():
        total = 0
        for item in tabla_seleccionadas.get_children():
            uc = int(tabla_seleccionadas.item(item, "values")[1])
            total += uc
        return total

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
        
        if materia_input == "":
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
            messagebox.showwarning("Conflicto", f"La materia '{materia}' pertenece a un grupo excluyente.")
            return
            
        creditos_actuales = obtener_creditos_totales()
        uc = MATERIAS_CREDITOS[materia]
        if creditos_actuales + uc > MAX_CREDITOS:
            messagebox.showerror("Límite", f"Agregar '{materia}' excede el límite de {MAX_CREDITOS} UC.")
            return

        # Agregar a pila y tabla seleccionada
        pila_materias.Insertar(materia)
        tabla_seleccionadas.insert("", "end", values=(materia, uc))
        entrada_materia.delete(0, tk.END)

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
            messagebox.showerror("Error", "Ha ocurrido un error inesperado.")

    # Botón Confirmar Materias 
    boton_confirmar = tk.Button(ventana, text="Confirmar materias", command=confirmar_materias)
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
                if materia in pila_materias.obtener_contenido():
                    messagebox.showinfo("Duplicado", "Esta materia ya fue agregada.")
                    return
                if esta_en_grupo_excluyente(materia):
                    messagebox.showwarning("Conflicto", f"La materia '{materia}' pertenece a un grupo excluyente.")
                    return
                creditos_actuales = obtener_creditos_totales()
                if creditos_actuales + uc > MAX_CREDITOS:
                    messagebox.showerror("Límite", f"Agregar '{materia}' excede el límite de {MAX_CREDITOS} UC.")
                    return
                pila_materias.Insertar(materia)
                tabla_seleccionadas.insert("", "end", values=(materia, uc))
    
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


    ventana.mainloop()
