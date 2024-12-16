# inventario/models.py

from django.db import models

class Categoria(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Nombre único para cada categoría
    descripcion = models.TextField(blank=True, null=True)  # Descripción opcional de la categoría
    imagen = models.ImageField(upload_to='categorias/', null=True, blank=True)  # Imagen de la categoría

    def __str__(self):
        return self.nombre

class Marca(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    marca = models.CharField(max_length=100)
    stock = models.IntegerField()
    stock_minimo = models.IntegerField(default=10)  # Nivel mínimo para bajo stock
    imagen1 = models.ImageField(upload_to='productos/')
    imagen2 = models.ImageField(upload_to='productos/', blank=True)
    imagen3 = models.ImageField(upload_to='productos/', blank=True)

    def __str__(self):
        return self.nombre

    def is_bajo_stock(self):
        """Devuelve True si el stock está por debajo del nivel mínimo."""
        return self.stock <= self.stock_minimo
