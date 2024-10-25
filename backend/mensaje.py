class Mensaje:
    def __init__(self, lugar, fecha, usuario, red_social, contenido):
        self.lugar = lugar
        self.fecha = fecha
        self.usuario = usuario
        self.red_social = red_social
        self.contenido = contenido
        self.sentimiento = 'neutro'

    def analizar_sentimiento(self, diccionario):
        palabras = self.contenido.lower().split()
        positivos = sum(1 for palabra in palabras if palabra in diccionario.sentimientos_positivos)
        negativos = sum(1 for palabra in palabras if palabra in diccionario.sentimientos_negativos)

        if positivos > negativos:
            self.sentimiento = 'positivo'
        elif negativos > positivos:
            self.sentimiento = 'negativo'
        else:
            self.sentimiento = 'neutro'

        return self.sentimiento
