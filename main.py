import tkinter as tk
from cola_tickets import VentanaTickets
from lista_inscripcion import VentanaInscripcion

def abrir_ventana_inscripcion():
    root.withdraw()  

    ventana = VentanaInscripcion(root) 

    def al_cerrar():
        ventana.destroy()
        root.deiconify()  

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar) 

root = tk.Tk()
root.title("Sistema de Inscripción")

tk.Label(root, text="Sistema de Inscripción UCLA", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Cola de espera", width=30, command=VentanaTickets).pack(pady=5)
tk.Button(root, text="Inscripción de Estudiantes ", width=30, command=abrir_ventana_inscripcion).pack(pady=5)

root.mainloop()
