from django.db import models
from inventario.models import Producto
from usuarios.models import Usuario

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)
    modificado_en = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.total() for item in self.items.all())

    def recalcular_totales(self):
        # Método para recalcular el total del carrito
        self.total_items = sum(item.cantidad for item in self.items.all())
        self.subtotal = sum(item.total() for item in self.items.all())
        self.save()

    def __str__(self):
        return f"Carrito de {self.usuario.username}"



class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name="items", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def total(self):
        return max(0, self.cantidad * self.producto.precio_venta)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
