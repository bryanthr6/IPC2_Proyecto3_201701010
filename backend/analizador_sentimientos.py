import re

class AnalizadorSentimiento:
    def __init__(self, diccionario_positivo, diccionario_negativo):
        self.diccionario_positivo = diccionario_positivo
        self.diccionario_negativo = diccionario_negativo

    def analizar(self, mensaje):
        mensaje = mensaje.lower()  # Ignorar mayúsculas/minúsculas
        palabras_positivas = sum(1 for palabra in self.diccionario_positivo if palabra in mensaje)
        palabras_negativas = sum(1 for palabra in self.diccionario_negativo if palabra in mensaje)

        if palabras_positivas > palabras_negativas:
            return "positivo"
        elif palabras_negativas > palabras_positivas:
            return "negativo"
        else:
            return "neutro"
