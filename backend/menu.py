from cargar import cargar_mensajes
from diccionario import Diccionario
from generar_salida import generar_salida_xml

def mostrar_menu():
    print("1. Cargar mensajes")
    print("2. Generar archivo de salida XML")
    print("3. Salir")

def main():
    diccionario = Diccionario()
    mensajes = []
    empresas = {}  # Diccionario para almacenar estadísticas de empresas y servicios

    while True:
        mostrar_menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            ruta_xml = input("Ingresa la ruta del archivo XML: ")
            mensajes = cargar_mensajes(ruta_xml)
            print(f"Se cargaron {len(mensajes)} mensajes.")

            # Inicializar estadísticas de empresas
            for mensaje in mensajes:
                mensaje.analizar_sentimiento(diccionario)
                # Aquí se deben actualizar las estadísticas en 'empresas' de acuerdo con el contenido del mensaje

        elif opcion == "2":
            if mensajes:
                ruta_salida = input("Ingresa la ruta de salida para el archivo XML: ")
                generar_salida_xml(mensajes, empresas, archivo_salida=ruta_salida)
            else:
                print("No hay mensajes cargados. Carga mensajes primero.")

        elif opcion == "3":
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()
