import tkinter as tk
from tkinter import ttk
from colas import Cola


def crear_grafica(cola):
    ventana = tk.Tk()
    ventana.title("Visualización de Cola - Estudiantes")
    ventana.geometry("800x300")
    ventana.resizable(0, 0)
    ventana.configure(bg="#CCD1D1")  # Fondo gris claro

    # Frame para el canvas y scrollbar
    frame_canvas = tk.Frame(ventana, bg="#CCD1D1")
    frame_canvas.pack(side=tk.TOP)

    scrollbar_horizontal = tk.Scrollbar(frame_canvas, orient=tk.HORIZONTAL)
    scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

    # Canvas para dibujar la cola
    canvas = tk.Canvas(frame_canvas, width=750, height=250, bg="#FFFFFF", xscrollcommand=scrollbar_horizontal.set)
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    scrollbar_horizontal.config(command=canvas.xview)
    # Función para dibujar la cola en el canvas
    def dibujar_cola(cola):
        canvas.delete("all")  # Limpiar el canvas antes de redibujar

        if cola.Vacia():
            canvas.create_text(375, 80, text="[La cola está vacía]", font=("Arial", 14))
            canvas.create_rectangle(320, 130, 430, 190, fill="lightblue")
            canvas.create_line(410, 130, 410, 190, fill="black")
            return

        x = 100  # Posición inicial en X
        y = 150  # Posición fija en Y
        separacion = 130  # Espacio entre nodos

        p = cola.Frente
        while p is not None:
            canvas.create_text(375, 40, text="[Espacio en memoria]", font=("Arial", 14))
            # Dibujar nodo (círculo + texto)
            canvas.create_rectangle(x, y-30, x+110, y+30, fill="lightblue")
            canvas.create_text(x+45, y, text=str(p.info.cedula), font=("Arial", 12))
            canvas.create_line(x+90, y-30, x+90, y+30, fill="black")  # Línea vertical

            # Dibujar flecha si hay un nodo siguiente
            if p.prox is not None:
                canvas.create_line(x+110, y, x+separacion, y, arrow=tk.LAST)

            # Resaltar Frente (rojo) y Final (verde)
            if p == cola.Frente:
                canvas.create_text(x+40, y-50, text="Frente", fill="red", font=("Arial", 10, "bold"))
            if p == cola.Final:
                canvas.create_text(x+40, y+50, text="Final", fill="green", font=("Arial", 10, "bold"))
                canvas.create_line(x+110, y-30, x+90, y+30, fill="black")

            x += separacion
            p = p.prox
            canvas.config(scrollregion=canvas.bbox("all"))
    # Mostrar cola inicial
    dibujar_cola(cola)
    ventana.mainloop()