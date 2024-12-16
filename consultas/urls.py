from django.urls import path
from . import views

app_name = 'consultas'

urlpatterns = [
    path('', views.formulario_consulta, name='formulario'),
]
