# models.py en la app "pedidos"
from django.db import models
from django.utils.timezone import now
from usuarios.models import Usuario
from inventario.models import Producto

class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_camino', 'En camino'),
        ('entregado', 'Entregado'),
    ]

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(default=now)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def total_productos(self):
        return sum(detalle.cantidad for detalle in self.detallepedido_set.all())

    def subtotal(self):
        return sum(detalle.total_producto for detalle in self.detallepedido_set.all())

    def __str__(self):
        return f"Pedido {self.id} - {self.usuario}"

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name="detallepedido_set", on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    # Usar @property para total_producto
    @property
    def total_producto(self):
        return self.cantidad * self.producto.precio_venta

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"

