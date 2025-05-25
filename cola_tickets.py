import tkinter as tk
from lista_inscripcion import VentanaInscripcion

def VentanaTickets():
   
    ventana = tk.Toplevel()
    ventana.title("Cola de Espera")

    tk.Label(ventana, text="Nombre:").pack()
    entrada_nombre = tk.Entry(ventana)
    entrada_nombre.pack()

    tk.Label(ventana, text="Cédula:").pack()
    entrada_cedula = tk.Entry(ventana)
    entrada_cedula.pack()

    tk.Label(ventana, text="Carrera:").pack()
    entrada_carrera = tk.Entry(ventana)
    entrada_carrera.pack()

    tk.Label(ventana, text="Prioridad (1-10):").pack()
    entrada_prioridad = tk.Entry(ventana)
    entrada_prioridad.pack()

    tk.Button(ventana, text="Obtener Ticket").pack(pady=10)
