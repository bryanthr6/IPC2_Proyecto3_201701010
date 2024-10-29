from flask import Flask, request, jsonify, Response
import xml.etree.ElementTree as ET
from collections import defaultdict
import re
from datetime import datetime

app = Flask(__name__)

# Diccionario de sentimientos y lista de mensajes
sentiments_dict = {'positivos': [], 'negativos': []}
messages_list = []
empresas_analizadas = defaultdict(lambda: {'positivos': 0, 'negativos': 0, 'servicios': defaultdict(lambda: {'positivos': 0, 'negativos': 0})})
palabras_positivas = ["bueno", "excelente", "cool", "satisfecho"]
palabras_negativas = ["malo", "pésimo", "triste", "molesto", "decepcionado", "enojo"]


# Ruta para la prueba de mensaje individual
@app.route('/mensaje_prueba', methods=['POST'])
def mensaje_prueba():
    # Parsear el XML recibido en la solicitud
    try:
        mensaje_xml = ET.fromstring(request.data)
        texto_mensaje = mensaje_xml.text

        # Extraer datos usando expresiones regulares
        fecha = re.search(r"\d{2}/\d{2}/\d{4}", texto_mensaje).group()
        usuario = re.search(r"Usuario: ([^\s]+)", texto_mensaje).group(1)
        red_social = re.search(r"Red social: ([^\s]+)", texto_mensaje).group(1)

        # Analizar sentimiento del mensaje
        palabras = texto_mensaje.lower().split()
        positivas = sum(1 for palabra in palabras if palabra in palabras_positivas)
        negativas = sum(1 for palabra in palabras if palabra in palabras_negativas)
        
        # Determinar el sentimiento general
        total_palabras = positivas + negativas
        sentimiento_positivo = round((positivas / total_palabras) * 100, 2) if total_palabras else 0
        sentimiento_negativo = round((negativas / total_palabras) * 100, 2) if total_palabras else 0
        sentimiento = "positivo" if sentimiento_positivo > sentimiento_negativo else "negativo"

        # Crear respuesta XML
        respuesta = ET.Element("respuesta")
        ET.SubElement(respuesta, "fecha").text = fecha
        ET.SubElement(respuesta, "red_social").text = red_social
        ET.SubElement(respuesta, "usuario").text = usuario
        ET.SubElement(respuesta, "palabras_positivas").text = str(positivas)
        ET.SubElement(respuesta, "palabras_negativas").text = str(negativas)
        ET.SubElement(respuesta, "sentimiento_positivo").text = f"{sentimiento_positivo}%"
        ET.SubElement(respuesta, "sentimiento_negativo").text = f"{sentimiento_negativo}%"
        ET.SubElement(respuesta, "sentimiento_analizado").text = sentimiento

        # Devolver la respuesta XML
        respuesta_xml = ET.tostring(respuesta, encoding='unicode')
        return Response(respuesta_xml, mimetype='application/xml')

    except Exception as e:
        return {"error": "Error procesando el mensaje XML", "detalle": str(e)}, 400


# Variables globales para almacenar datos de diccionario y mensajes
diccionario = {"positivos": [], "negativos": [], "empresas": {}}
mensajes = []


# 1. Endpoint para cargar el XML
@app.route('/cargar', methods=['POST'])
def cargar():
    global diccionario, mensajes
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Parsear el XML y extraer el diccionario y la lista de mensajes
    tree = ET.parse(file)
    root = tree.getroot()

    # Resetear las variables globales
    diccionario = {"positivos": [], "negativos": [], "empresas": {}}
    mensajes = []

    # Procesar sentimientos
    for palabra in root.find('.//sentimientos_positivos'):
        diccionario["positivos"].append(palabra.text.strip().lower())
    for palabra in root.find('.//sentimientos_negativos'):
        diccionario["negativos"].append(palabra.text.strip().lower())

    # Procesar empresas y servicios
    for empresa in root.findall('.//empresa'):
        nombre_empresa = empresa.find('nombre').text.strip().lower()
        servicios = {}
        for servicio in empresa.find('servicios'):
            nombre_servicio = servicio.attrib['nombre'].strip().lower()
            alias = [a.text.strip().lower() for a in servicio.findall('alias')]
            servicios[nombre_servicio] = alias
        diccionario["empresas"][nombre_empresa] = servicios

    # Procesar mensajes
    for mensaje in root.findall('.//mensaje'):
        mensajes.append(mensaje.text.strip())

    return jsonify({"message": "Archivo cargado y procesado exitosamente"}), 200


# 2. Endpoint para analizar mensajes
@app.route('/analizar', methods=['POST'])
def analizar():
    resultados = {"positivos": 0, "negativos": 0, "neutros": 0, "empresas": {}}

    def normalizar_texto(texto):
        # Quitar tildes y convertir a minúsculas
        texto = texto.lower()
        texto = re.sub(r'[áàäâ]', 'a', texto)
        texto = re.sub(r'[éèëê]', 'e', texto)
        texto = re.sub(r'[íìïî]', 'i', texto)
        texto = re.sub(r'[óòöô]', 'o', texto)
        texto = re.sub(r'[úùüû]', 'u', texto)
        return texto

    for mensaje in mensajes:
        mensaje_normalizado = normalizar_texto(mensaje)
        palabras = mensaje_normalizado.split()
        positivos = sum(1 for palabra in palabras if palabra in diccionario["positivos"])
        negativos = sum(1 for palabra in palabras if palabra in diccionario["negativos"])

        # Clasificar sentimiento del mensaje
        if positivos > negativos:
            sentimiento = "positivo"
            resultados["positivos"] += 1
        elif negativos > positivos:
            sentimiento = "negativo"
            resultados["negativos"] += 1
        else:
            sentimiento = "neutro"
            resultados["neutros"] += 1

        # Verificar menciones de empresas y servicios
        for empresa, servicios in diccionario["empresas"].items():
            if empresa not in resultados["empresas"]:
                resultados["empresas"][empresa] = {
                    "total": 0,
                    "positivos": 0,
                    "negativos": 0,
                    "neutros": 0,
                    "servicios": {}
                }
            
            # Incrementar el total de mensajes para la empresa
            resultados["empresas"][empresa]["total"] += 1

            # Incrementar el conteo del sentimiento correspondiente
            if sentimiento not in resultados["empresas"][empresa]:
                # Aseguramos que la clave del sentimiento exista
                resultados["empresas"][empresa][sentimiento] = 0
            
            resultados["empresas"][empresa][sentimiento] += 1

            for servicio, alias in servicios.items():
                if servicio not in resultados["empresas"][empresa]["servicios"]:
                    resultados["empresas"][empresa]["servicios"][servicio] = {
                        "total": 0,
                        "positivos": 0,
                        "negativos": 0,
                        "neutros": 0
                    }

                # Aumentamos el total de mensajes para el servicio
                resultados["empresas"][empresa]["servicios"][servicio]["total"] += 1
                
                # Incrementar el conteo del sentimiento para el servicio
                if sentimiento not in resultados["empresas"][empresa]["servicios"][servicio]:
                    # Aseguramos que la clave del sentimiento exista
                    resultados["empresas"][empresa]["servicios"][servicio][sentimiento] = 0

                resultados["empresas"][empresa]["servicios"][servicio][sentimiento] += 1

    return jsonify(resultados), 200


@app.route('/generar_respuesta', methods=['POST'])
def generar_respuesta():
    fecha = datetime.now().strftime("%d/%m/%Y")
    resultados = request.get_json()

    lista_respuestas = ET.Element("lista_respuestas")
    respuesta = ET.SubElement(lista_respuestas, "respuesta")
    ET.SubElement(respuesta, "fecha").text = fecha

    mensajes = ET.SubElement(respuesta, "mensajes")

    # Sumar los valores enteros para el total
    total_mensajes = resultados["positivos"] + resultados["negativos"] + resultados["neutros"]
    ET.SubElement(mensajes, "total").text = str(total_mensajes)

    ET.SubElement(mensajes, "positivos").text = str(resultados["positivos"])
    ET.SubElement(mensajes, "negativos").text = str(resultados["negativos"])
    ET.SubElement(mensajes, "neutros").text = str(resultados["neutros"])

    analisis = ET.SubElement(respuesta, "analisis")
    for empresa, datos in resultados["empresas"].items():
        empresa_elem = ET.SubElement(analisis, "empresa", nombre=empresa)
        empresa_mensajes = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(empresa_mensajes, "total").text = str(datos["total"])
        ET.SubElement(empresa_mensajes, "positivos").text = str(datos["positivos"])
        ET.SubElement(empresa_mensajes, "negativos").text = str(datos["negativos"])
        ET.SubElement(empresa_mensajes, "neutros").text = str(datos["neutros"])

        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for servicio, sdatos in datos["servicios"].items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=servicio)
            servicio_mensajes = ET.SubElement(servicio_elem, "mensajes")
            ET.SubElement(servicio_mensajes, "total").text = str(sdatos["total"])
            ET.SubElement(servicio_mensajes, "positivos").text = str(sdatos["positivos"])
            ET.SubElement(servicio_mensajes, "negativos").text = str(sdatos["negativos"])
            ET.SubElement(servicio_mensajes, "neutros").text = str(sdatos["neutros"])

    xml_response = ET.tostring(lista_respuestas, encoding="utf-8", method="xml")
    return Response(xml_response, mimetype="application/xml")

@app.route('/resumen_fecha', methods=['POST'])
def resumen_fecha():
    request_data = request.get_json()
    fecha = request_data.get("fecha")
    empresa = request_data.get("empresa")  # Puede ser 'todas' o el nombre de la empresa

    total_mensajes = 0
    total_positivos = 0
    total_negativos = 0
    total_neutros = 0

    # Suponiendo que tienes una estructura donde se almacenan los mensajes y sus fechas y sentimientos
    for mensaje in mensajes:  # O tu estructura que contiene todos los mensajes
        # Asegúrate de que cada mensaje tenga una fecha y un sentimiento, ajusta según sea necesario
        mensaje_fecha = mensaje["fecha"]  # Debes tener esta estructura
        mensaje_sentimiento = mensaje["sentimiento"]  # Debes tener esta estructura

        if mensaje_fecha == fecha and (empresa == "todas" or mensaje["empresa"] == empresa):
            total_mensajes += 1
            if mensaje_sentimiento == "positivo":
                total_positivos += 1
            elif mensaje_sentimiento == "negativo":
                total_negativos += 1
            elif mensaje_sentimiento == "neutro":
                total_neutros += 1

    resultado = {
        "total_mensajes": total_mensajes,
        "total_positivos": total_positivos,
        "total_negativos": total_negativos,
        "total_neutros": total_neutros
    }

    return jsonify(resultado), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
