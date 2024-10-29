from datetime import datetime

class Mensaje:
    def __init__(self, fecha, usuario, red_social, contenido):
        self.fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M")
        self.usuario = usuario
        self.red_social = red_social
        self.contenido = contenido