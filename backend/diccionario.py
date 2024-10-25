class Diccionario:
    def __init__(self):
        self.sentimientos_positivos = set()
        self.sentimientos_negativos = set()
        self.empresas = {}

    def cargar_diccionario(self, xml_data):
        # Aquí iría el código para cargar los sentimientos y empresas desde el XML
        pass

    def agregar_empresa(self, empresa):
        if empresa.nombre not in self.empresas:
            self.empresas[empresa.nombre] = empresa
