# admin.py
from django.contrib import admin
from .models import Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1  # Muestra un campo adicional para agregar detalles

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'estado', 'fecha_hora', 'total_productos', 'subtotal')
    list_filter = ('estado', 'fecha_hora')
    search_fields = ('usuario__username', 'usuario__email')  # Permite búsqueda por nombre de usuario o correo electrónico
    list_editable = ('estado',)  # Permite editar el estado directamente desde la lista
    inlines = [DetallePedidoInline]  # Permite editar los detalles del pedido directamente desde el formulario de pedido
    
    def total_productos(self, obj):
        return obj.total_productos()
    total_productos.short_description = 'Total Productos'

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = 'Subtotal'

admin.site.register(Pedido, PedidoAdmin)
admin.site.register(DetallePedido)
