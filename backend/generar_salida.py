import xml.etree.ElementTree as ET
from xml.dom import minidom
from datetime import datetime

def generar_salida_xml(mensajes, empresas, archivo_salida):
    """Genera el archivo XML con la respuesta analizada."""
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    root = ET.Element("lista_respuestas")
    respuesta = ET.SubElement(root, "respuesta")

    # Fecha
    ET.SubElement(respuesta, "fecha").text = fecha_actual

    # Resumen de mensajes
    total_mensajes = len(mensajes)
    positivos = sum(1 for mensaje in mensajes if mensaje.sentimiento == 'positivo')
    negativos = sum(1 for mensaje in mensajes if mensaje.sentimiento == 'negativo')
    neutros = total_mensajes - positivos - negativos

    mensajes_elem = ET.SubElement(respuesta, "mensajes")
    ET.SubElement(mensajes_elem, "total").text = str(total_mensajes)
    ET.SubElement(mensajes_elem, "positivos").text = str(positivos)
    ET.SubElement(mensajes_elem, "negativos").text = str(negativos)
    ET.SubElement(mensajes_elem, "neutros").text = str(neutros)

    # Análisis de empresas
    analisis = ET.SubElement(respuesta, "analisis")
    for empresa_nombre, empresa_data in empresas.items():
        empresa_elem = ET.SubElement(analisis, "empresa", nombre=empresa_nombre)

        # Mensajes por empresa
        mensajes_empresa = ET.SubElement(empresa_elem, "mensajes")
        ET.SubElement(mensajes_empresa, "total").text = str(empresa_data['total_mensajes'])
        ET.SubElement(mensajes_empresa, "positivos").text = str(empresa_data['positivos'])
        ET.SubElement(mensajes_empresa, "negativos").text = str(empresa_data['negativos'])
        ET.SubElement(mensajes_empresa, "neutros").text = str(empresa_data['neutros'])

        # Análisis de servicios
        servicios_elem = ET.SubElement(empresa_elem, "servicios")
        for servicio_nombre, servicio_data in empresa_data['servicios'].items():
            servicio_elem = ET.SubElement(servicios_elem, "servicio", nombre=servicio_nombre)
            ET.SubElement(servicio_elem, "total").text = str(servicio_data['total'])
            ET.SubElement(servicio_elem, "positivos").text = str(servicio_data['positivos'])
            ET.SubElement(servicio_elem, "negativos").text = str(servicio_data['negativos'])
            ET.SubElement(servicio_elem, "neutros").text = str(servicio_data['neutros'])

    # Guardar el archivo XML
    xml_str = ET.tostring(root, encoding="utf-8")
    dom = minidom.parseString(xml_str)
    pretty_xml_as_str = dom.toprettyxml(indent="  ")

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(pretty_xml_as_str)
    print(f"Archivo de salida '{archivo_salida}' generado exitosamente.")
