from django.db import models

class Proveedor(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    productos_suministrados = models.TextField()  # Lista de productos que ofrece el proveedor

    def __str__(self):
        return self.nombre
