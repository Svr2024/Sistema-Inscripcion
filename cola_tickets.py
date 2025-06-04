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
    ventana.geometry("400x400")
    ventana.resizable(0,0) # Impidiendo redimensión de la ventana
    center_window(ventana, 400, 400)

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

    frame_atras = tk.Frame(ventana)
    frame_atras.pack(anchor="w", side="top", padx=10)

    label_titulo = tk.Label(ventana, text="Taquilla",  bg="#E6EDFF", font=("Arial", 16))
    label_titulo.pack(pady=10)

    tk.Label(ventana, text="Nombre:",  bg="#E6EDFF").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Cédula:",  bg="#E6EDFF").pack()
    entrada_cedula = tk.Entry(ventana)
    entrada_cedula.pack()

    tk.Label(ventana, text="Carrera:",  bg="#E6EDFF").pack()
    select_carrera = ttk.Combobox(ventana, value=carrera_opciones, state="readonly")
    select_carrera.pack()

    tk.Label(ventana, text="Prioridad (1-10):",  bg="#E6EDFF").pack()
    select_prioridad = ttk.Combobox(ventana, values=prioridad_opciones, state="readonly")
    select_prioridad.pack()

    tk.Button(frame_atras, text="← Atrás", command=regresar_a_principal, bg="#183386", fg="white").pack(side=tk.LEFT, pady=10)
    tk.Button(ventana, text="Obtener Ticket", command=añadir_en_cola, bg="#183386", fg="white").pack(pady=10)
    tk.Button(ventana, text="Cerrar Taquilla", command=ordenar_prioridad, bg="#183386", fg="white").pack(pady=10)
    tk.Button(ventana, text="Visualizar Cola", command=ver_cola, bg="#183386", fg="white").pack(pady=10)
    return ventana