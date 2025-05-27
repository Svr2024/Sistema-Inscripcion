import tkinter as tk
from cola_tickets import VentanaTickets
from lista_inscripcion import VentanaInscripcion
from pila_materias import VentanaMaterias


root = tk.Tk()
root.title("Sistema de Inscripción")

tk.Label(root, text="Sistema de Inscripción UCLA", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Cola de espera", width=30, command=VentanaTickets).pack(pady=5)
tk.Button(root, text="Inscripción de Estudiantes ", width=30, command=VentanaInscripcion).pack(pady=5)
tk.Button(root, text="Materias", width=30, command=VentanaMaterias).pack(pady=5)

root.mainloop()
