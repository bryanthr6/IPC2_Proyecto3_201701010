from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.conf import settings
import json
# Create your views here.

def index(request):
    return render(request, 'index.html')

def ver_grafica(request):
    return render(request, 'grafica.html')

def datos_estudiante(request):
    return render(request, 'ayuda.html')

def ver_procesados(request):
    processed_data = ""
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]
        try:
            # Enviar el archivo al endpoint mensaje_prueba de Flask
            response = requests.post(
                f'http://localhost:5000/mensaje_prueba', 
                files={"file": file}
            )

            # Verificar si la respuesta fue exitosa
            if response.status_code == 200:
                # Guardar la respuesta XML para mostrarla en el frontend
                processed_data = response.text
            else:
                processed_data = "Error en el procesamiento del archivo."

        except requests.exceptions.RequestException as e:
            processed_data = f"Error de conexión: {e}"

    return render(request, 'verprocesados.html', {'processed_data': processed_data})

def peticiones(request):
    contenido_archivo = ""
    resultado_analisis = ""
    salida_xml = ""
    mensaje_limpieza = ""

    if request.method == "POST":
        # Manejar la carga del archivo
        if 'cargar' in request.POST and 'file' in request.FILES:
            file = request.FILES['file']
            response = requests.post(
                f'http://localhost:5000/cargar', 
                files={'file': file}
            )
            contenido_archivo = response.text if response.status_code == 200 else "Error al cargar el archivo."

        # Manejar el procesamiento
        elif 'procesar' in request.POST:
            response = requests.post(f'http://localhost:5000/analizar')
            resultado_analisis = response.text if response.status_code == 200 else "Error al procesar el archivo."

        # Manejar la generación de salida
        elif 'generar_salida' in request.POST:
            response = requests.post(f'http://localhost:5000/generar_respuesta', json={})
            salida_xml = response.text if response.status_code == 200 else "Error al generar la salida."

        # Manejar la limpieza de datos
        elif 'limpiar' in request.POST:
            response = requests.delete(f'http://localhost:5000/limpiar')
            if response.status_code == 200:
                mensaje_limpieza = response.json().get("message", "Datos limpiados exitosamente")
            else:
                mensaje_limpieza = "Error al intentar limpiar los datos."

    return render(request, 'peticiones.html', {
        'contenido_archivo': contenido_archivo,
        'resultado_analisis': resultado_analisis,
        'salida_xml': salida_xml,
        'mensaje_limpieza': mensaje_limpieza
    })