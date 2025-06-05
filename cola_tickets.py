import tkinter as tk
from tkinter import ttk
from colas import Cola
from Estudiante import Estudiante
from lista_inscripcion import VentanaInscripcion
from grafica_tickets import crear_grafica
from tkinter import messagebox
from dbJson import Db_json


def center_window(win, width=None, height=None):
    win.update_idletasks()
    if width is None or height is None:
        win_width = win.winfo_width()
        win_height = win.winfo_height()
        if win_width == 1 or win_height == 1:  
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


def VentanaTickets(master=None):
    ventana = tk.Toplevel(master)
    ventana.title("Cola de Espera")
    ventana.configure(bg="#E6EDFF")
    ventana.geometry("500x400")
    ventana.resizable(0,0) # Impidiendo redimensión de la ventana
    center_window(ventana, 500, 400)
    ventana.configure(bg="#CCD1D1")

    label_style = {"bg": "#CCD1D1", "font": ("Arial", 10), "width": 15, "anchor": "w"}
    entry_style = {"width": 25, "font": ("Arial", 10), "borderwidth": 1, "relief": "solid"}
    combobox_style = {"width": 23, "font": ("Arial", 10)}
    button_style = {"width": 15}
    
    # Configurar estilos para los widgets ttk
    estilo = ttk.Style()
    estilo.theme_use('clam')

    # Crear estilo para los botones ttk
    estilo = ttk.Style()
    estilo.configure('TButton', 
                   font=('Arial', 10, 'bold'),
                   background="#183386",
                   foreground="white",
                   padding=10,
                   borderwidth=1)
    
    estilo.configure("TCombobox", fieldbackground="#FFFFFF", background="#FFFFFF", font=("Arial", 10))



    estilo.map('TButton',
              background=[('active', "#183386")],
              foreground=[('active', 'white')])

    # Crear una instancia de Cola
    cola = Cola()

    # Asegurar permanencia de datos ya existentes 
    try:
        estudiantes_guardados = Db_json.cargar_estudiantes_json("estudiantes.json")
        for est in estudiantes_guardados:
            cola.Insertar(est)
    except FileNotFoundError:
        print("No se encontró archivo de estudiantes previos. Se creará uno nuevo al cerrar taquilla.")


    def añadir_en_cola():
        cedula = entrada_cedula.get()
        nombre = entrada_nombre.get()
        carrera = select_carrera.get()
        prioridad = select_prioridad.get()

        if cedula and nombre and carrera and prioridad:
            estudiante = Estudiante(cedula, nombre, carrera, int(prioridad))
            if cola.Insertar(estudiante):
                print(f"Ticket creado para {nombre} ({cedula}) en {carrera} con prioridad {prioridad}.")
                tk.messagebox.showinfo("Éxito", f"Ticket creado para {nombre} ({cedula}) en {carrera} con prioridad {prioridad}.")
                #guardar_en_archivo(estudiante)
                cola.MostrarContenido()
                limpiar_entradas()
            else:
                print("¡La cola está llena (memoria llena)!")
                tk.messagebox.showerror("Error", "¡La cola está llena (memoria llena)!")
        else:
            print("Por favor, complete todos los campos.")
            messagebox.showwarning("Campos incompletos", "Por favor, complete todos los campos.")


    def limpiar_entradas():
        entrada_cedula.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        select_carrera.set('')
        select_prioridad.set('')

    def ver_cola():
        crear_grafica(cola)

    def regresar_a_principal():
     ventana.destroy()
     if master is not None:
        master.deiconify()


    def ordenar_prioridad():
        if not cola.Vacia():
            i = 1
            cola_ordenada = Cola()
            while i <= 10:
                p = cola.Frente
                while p is not None:
                    if (p.info.prioridad == i):
                        cola_ordenada.Insertar(p.info)
                    p = p.prox
                i += 1
            cola_ordenada.MostrarContenido()
            Db_json.guardar_estudiantes_json(cola_ordenada.transformar_array(), "estudiantes.json")
            tk.messagebox.showinfo("Info", "Se ha reordenado por prioridad")
            ventana.destroy()
            VentanaInscripcion()
        else:
            print("La cola está vacía, no se puede ordenar.")
            tk.messagebox.showinfo("Info", "La cola está vacía, no se puede ordenar.")

    prioridad_opciones = [str(i) for i in range(1, 11)]
    carrera_opciones = ["Ingeniería Informática",
                        "Análisis de Sistemas",
                        "Ingeniería en Producción",
                        "Ingeniería en Telemática",
                        "Licenciatura en Matemáticas",
                        "Licenciatura en Física"]

    frame_principal = tk.Frame(ventana, bg="#CCD1D1")
    frame_principal.pack(pady=20)

    frame_atras = tk.Frame(frame_principal, bg="#CCD1D1")
    frame_atras.pack(anchor="w", pady=(0, 20))

    label_titulo = tk.Label(frame_principal, text="Taquilla", font=("Arial", 16, "bold"), bg="#CCD1D1")
    label_titulo.pack(pady=(0, 20))

    # Frame para campos de entrada
    frame_campos = tk.Frame(frame_principal, bg="#CCD1D1")
    frame_campos.pack()

    tk.Label(frame_campos, text="Nombre:", **label_style).grid(row=0, column=0, sticky="w", pady=8)
    entrada_nombre = tk.Entry(frame_campos, **entry_style)
    entrada_nombre.grid(row=0, column=1, pady=8, padx=10)

    tk.Label(frame_campos, text="Cédula:", **label_style).grid(row=1, column=0, sticky="w", pady=8)
    entrada_cedula = tk.Entry(frame_campos, **entry_style)
    entrada_cedula.grid(row=1, column=1, pady=8, padx=10)

    tk.Label(frame_campos, text="Carrera:", **label_style).grid(row=2, column=0, sticky="w", pady=8)
    select_carrera = ttk.Combobox(frame_campos, values=carrera_opciones, state="readonly", **combobox_style)
    select_carrera.grid(row=2, column=1, pady=8, padx=10)

    tk.Label(frame_campos, text="Prioridad (1-10):", **label_style).grid(row=3, column=0, sticky="w", pady=8)
    select_prioridad = ttk.Combobox(frame_campos, values=prioridad_opciones, state="readonly", **combobox_style)
    select_prioridad.grid(row=3, column=1, pady=8, padx=10)

    # Frame para botones principales
    frame_botones = tk.Frame(frame_principal, bg="#CCD1D1")
    frame_botones.pack(pady= (30, 10))

    ttk.Button(frame_atras, text="← Atrás", command=regresar_a_principal).pack(side=tk.LEFT)

    # Botones principales
    ttk.Button(frame_botones, text="Obtener Ticket", command=añadir_en_cola, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
    ttk.Button(frame_botones, text="Cerrar Taquilla", command=ordenar_prioridad, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
    ttk.Button(frame_botones, text="Visualizar Cola", command=ver_cola, **button_style).pack(side=tk.LEFT, padx=10, pady=5)
    return ventana