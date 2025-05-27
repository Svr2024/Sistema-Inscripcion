import tkinter as tk
from tkinter import ttk
from colas import Cola
from Estudiante import Estudiante
from lista_inscripcion import VentanaInscripcion

def VentanaTickets():
    ventana = tk.Toplevel()
    ventana.title("Cola de Espera")
    ventana.geometry("400x400")
    ventana.resizable(0,0) # Impidiendo redimensión de la ventana

    # Crear una instancia de Cola
    cola = Cola()

    def añadir_en_cola():
        # Aquí se puede implementar la lógica para crear una cola de tickets
        cedula = entrada_cedula.get()
        nombre = entrada_nombre.get()
        carrera = select_carrera.get()
        prioridad = select_prioridad.get()
        #prioridad = int(select_prioridad.get())
        if (cedula and nombre and carrera and prioridad):
            if cola.Insertar(Estudiante(cedula, nombre, carrera, int(prioridad))):
                print(f"Ticket creado para {nombre} ({cedula}) en {carrera} con prioridad {prioridad}.")
                limpiar_entradas()
        else:
            print("Por favor, complete todos los campos.")

    def limpiar_entradas():
        entrada_cedula.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        select_carrera.set('')
        select_prioridad.set('')

    prioridad_opciones = [str(i) for i in range(1, 11)]
    carrera_opciones = ["Ingeniería Informática",
                        "Análisis de Sistemas",
                        "Ingeniería en Producción",
                        "Ingeniería en Telemática",
                        "Licenciatura en Matemáticas",
                        "Licenciatura en Física"]

    label_titulo = tk.Label(ventana, text="Taquilla", font=("Arial", 16))
    label_titulo.pack(pady=10)

    tk.Label(ventana, text="Nombre:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Cédula:").pack()
    entrada_cedula = tk.Entry(ventana)
    entrada_cedula.pack()

    tk.Label(ventana, text="Carrera:").pack()
    select_carrera = ttk.Combobox(ventana, value=carrera_opciones, state="readonly")
    select_carrera.pack()

    tk.Label(ventana, text="Prioridad (1-10):").pack()
    select_prioridad = ttk.Combobox(ventana, values=prioridad_opciones, state="readonly")
    select_prioridad.pack()

    tk.Button(ventana, text="Obtener Ticket", command=añadir_en_cola).pack(pady=10)
    tk.Button(ventana, text="Cerrar Taquilla").pack(pady=10)
