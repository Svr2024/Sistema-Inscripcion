import tkinter as tk
from PIL import Image, ImageTk  # Importe Pillow para poder manipular imágenes, como su tamaño
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

def abrir_ventana_tickets():
    root.withdraw() 
    ventana = VentanaTickets(root)  
    def al_cerrar():
        ventana.destroy()
        root.deiconify()  
    ventana.protocol("WM_DELETE_WINDOW", al_cerrar)

def abrir_ventana_materias():
    root.withdraw()  
    ventana = VentanaMaterias(root) 
    def al_cerrar():
        ventana.destroy()
        root.deiconify()  
    ventana.protocol("WM_DELETE_WINDOW", al_cerrar) 
    
root = tk.Tk()
root.title("Sistema de Inscripción")


# root.geometry("800x600")


root.configure(bg="white")

# Centrar ventana en la pantalla y ajustarla al 90% del espacio disponible en pantalla
# root.update_idletasks()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# width = int(screen_width * 0.9)
# height = int(screen_height * 0.9)
# x = (screen_width // 2) - (width // 2)
# y = (screen_height // 2) - (height // 2)
# root.geometry(f"{width}x{height}+{x}+{y}")
# Maximizar ventana por defecto on Windows
root.state("zoomed")

frame = tk.Frame(root, bg="white")
frame.pack(expand=True)

imagen_pil = Image.open("logo.png")    
imagen_pil = imagen_pil.resize((80, 80), Image.Resampling.LANCZOS)  
imagen_logo = ImageTk.PhotoImage(imagen_pil) 

label_imagen = tk.Label(frame, image=imagen_logo, bg="white")
label_imagen.pack(pady=(20, 10))

tk.Label(frame, text="Sistema de Inscripción UCLA", font=("Arial", 16), bg="white").pack(pady=10)

color_boton = "#183386"  # Azul rey
color_texto = "white"

tk.Button(frame, text="Cola de espera", width=30, bg=color_boton, fg=color_texto, command=abrir_ventana_tickets).pack(pady=5)
tk.Button(frame, text="Inscripción de Estudiantes ", width=30, bg=color_boton, fg=color_texto, command=abrir_ventana_inscripcion).pack(pady=5)


root.mainloop()
