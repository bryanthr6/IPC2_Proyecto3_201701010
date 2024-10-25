class Empresa:
    def __init__(self, nombre):
        self.nombre = nombre
        self.servicios = {}
        self.total_mensajes = 0
        self.positivos = 0
        self.negativos = 0
        self.neutros = 0

    def agregar_servicio(self, servicio):
        if servicio not in self.servicios:
            self.servicios[servicio] = {'total': 0, 'positivos': 0, 'negativos': 0, 'neutros': 0}

    def actualizar_estadisticas(self, servicio, sentimiento):
        self.total_mensajes += 1
        self.servicios[servicio]['total'] += 1

        if sentimiento == 'positivo':
            self.positivos += 1
            self.servicios[servicio]['positivos'] += 1
        elif sentimiento == 'negativo':
            self.negativos += 1
            self.servicios[servicio]['negativos'] += 1
        else:
            self.neutros += 1
            self.servicios[servicio]['neutros'] += 1
