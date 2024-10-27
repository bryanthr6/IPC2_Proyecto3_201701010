from django.shortcuts import render
import requests

# Create your views here.

def index(request):
    return render(request, 'index.html')

def ver_grafica(request):
    return render(request, 'grafica.html')

def datos_estudiante(request):
    return render(request, 'ayuda.html')

def ver_procesados(request):
    return render(request, 'verprocesados.html' )