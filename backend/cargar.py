import xml.etree.ElementTree as ET
from mensaje import Mensaje

def cargar_mensajes(ruta_xml):
    mensajes = []
    tree = ET.parse(ruta_xml)
    root = tree.getroot()

    for elem in root.findall('.//mensaje'):
        lugar_fecha = elem.text.split('Usuario:')[0].strip().replace('Lugar y fecha: ', '')
        lugar, fecha = lugar_fecha.split(',')
        usuario = elem.text.split('Usuario:')[1].split('Red social:')[0].strip()
        red_social = elem.text.split('Red social:')[1].split()[0].strip()
        contenido = ' '.join(elem.text.split()[6:])
        
        mensaje = Mensaje(lugar.strip(), fecha.strip(), usuario, red_social, contenido.strip())
        mensajes.append(mensaje)

    return mensajes
