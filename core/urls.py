# core/urls.py
from django.urls import path
from . import views
app_name = 'core'
urlpatterns = [
    path('inicio/', views.inicio, name='inicio'), # Esta ruta debe ser 'inicio/'
    path('prueba-correo/', views.prueba_correo, name='prueba_correo'),
    
]
