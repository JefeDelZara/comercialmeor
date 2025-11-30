# core/urls.py
from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('inicio/', views.inicio, name='inicio'), # Esta ruta debe ser 'inicio/'
    path('prueba-correo/', views.prueba_correo, name='prueba_correo'),
    
]
