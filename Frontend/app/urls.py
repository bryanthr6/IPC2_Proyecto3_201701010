from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='inicio'),
    path('estadisticas/', views.ver_grafica, name='estadisticas'),
    path('ayuda/', views.datos_estudiante, name='ayuda'),
    path('procesados/', views.ver_procesados, name='ver_procesados'),  # Nueva URL para ver procesados
]