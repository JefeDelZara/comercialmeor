# notificaciones/models.py

from django.conf import settings
from django.db import models

class Notificacion(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Pedido(models.Model):
    # Definición del modelo Pedido si es necesario
    pass