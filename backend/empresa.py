class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = []
        self.total_mensajes = 0
        self.mensajes_positivos = 0
        self.mensajes_negativos = 0
        self.mensajes_neutros = 0