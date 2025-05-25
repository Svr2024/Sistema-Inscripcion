class NodoPila:
    def __init__(self, valor=None):
        self.info = valor  # Valor del nodo
        self.ap = None     # Referencia al siguiente nodo (para simular el puntero)


class Pila:
    def __init__(self):
        self.Tope = None 

    def Vacia(self):
        #Verifica si la pila esta vacia
        return self.Tope is None

    def Llena(self):
        #Simula la comprobacion de memoria
        try:
           
            nuevo = NodoPila()
            return False  # Si se creo correctamente entonces la pila no esta llena
        except MemoryError:
            return True  # Si ocurre un error de memoria se considera que la pila esta llena

    def Insertar(self, valor):
        #Inserta un valor en la pila
        if not self.Llena():
            nuevo = NodoPila(valor)  # crear un nuevo nodo
            nuevo.ap = self.Tope  # el puntero 'ap' apunta al nodo anterior simulando puntero
            self.Tope = nuevo  # el nuevo nodo pasa a ser el Tope de la pila
            return True
        return False

    def MostrarContenido(self):
        if self.Vacia():
            print("La Pila está vacía.")
        else:
            p = self.Tope
            print("Contenido de la Pila:")
            while p is not None:
                print(p.info)
                p = p.ap
                
    def Remover(self):
        #Remueve el valor del Tope de la pila y lo devuelve
        if not self.Vacia():
            viejo = self.Tope  # el nodo actual del Tope
            valor = viejo.info  # recuperamos el valor del nodo
            self.Tope = viejo.ap  # el Tope pasa al siguiente nodo simulando desapilar
            return valor
        return None 

    def ObtTope(self):
        #Obtiene el nodo en el Tope de la pila
        return self.Tope

    def AsigTope(self, nodo):
        #Asigna un nuevo nodo al Tope de la pila
        self.Tope = nodo

    def ObtInfo(self, nodo):
        #Obtiene la informacion almacenada en el nodo
        return nodo.info

    def AsigInfo(self, nodo, valor):
        #Asigna un nuevo valor al nodo
        nodo.info = valor

    def obtener_contenido(self):
        """Devuelve una lista de los datos de los nodos de la pila, desde el tope hasta el fondo."""
        contenido = []
        actual = self.Tope  # Usa el nombre correcto del atributo
        while actual:
            contenido.append(actual.info)
            actual = actual.ap  # Usa el nombre correcto del enlace entre nodos
        return contenido