import tkinter as tk
from cola_tickets import VentanaTickets
from lista_inscripcion import VentanaInscripcion
from pila_materias import VentanaMaterias

def abrir_ventana_inscripcion():
    root.withdraw()  

    ventana = VentanaInscripcion(root) 

    def al_cerrar():
        ventana.destroy()
        root.deiconify()  

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar) 

root = tk.Tk()
root.title("Sistema de Inscripción")

# Establecer tamaño inicial de la ventana
root.geometry("800x600")

# Crear un marco para centrar los widgets
frame = tk.Frame(root)
frame.pack(expand=True)

tk.Label(frame, text="Sistema de Inscripción UCLA", font=("Arial", 16)).pack(pady=10)

tk.Button(frame, text="Cola de espera", width=30, command=VentanaTickets).pack(pady=5)
tk.Button(frame, text="Inscripción de Estudiantes ", width=30, command=VentanaInscripcion).pack(pady=5)
tk.Button(frame, text="Materias", width=30, command=VentanaMaterias).pack(pady=5)

root.mainloop()
