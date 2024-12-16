from django.db import models
from usuarios.models import Usuario



class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)  # Campo para el nombre
    apellido = models.CharField(max_length=100)  # Campo para el apellido
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    rut = models.CharField(max_length=12, unique=True)  # Campo obligatorio para el RUT
    observaciones = models.TextField(null=True, blank=True)  # Campo opcional para observaciones

    def __str__(self):
        return self.usuario.username

