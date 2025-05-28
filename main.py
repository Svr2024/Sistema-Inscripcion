import tkinter as tk
from cola_tickets import VentanaTickets
from lista_inscripcion import VentanaInscripcion

def abrir_ventana_inscripcion():
    root.withdraw()  # Oculta la ventana principal

    ventana = VentanaInscripcion(root)  # Le pasa root como master

    def al_cerrar():
        ventana.destroy()
        root.deiconify()  # Vuelve a mostrar la ventana principal

    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)  # Reacciona al cierre de la ventana

root = tk.Tk()
root.title("Sistema de Inscripción")

tk.Label(root, text="Sistema de Inscripción UCLA", font=("Arial", 16)).pack(pady=10)

tk.Button(root, text="Cola de espera", width=30, command=VentanaTickets).pack(pady=5)
tk.Button(root, text="Inscripción de Estudiantes ", width=30, command=abrir_ventana_inscripcion).pack(pady=5)

root.mainloop()
