from django.contrib import admin
from .models import Proveedor

# Registro del modelo Proveedor en el panel de administración
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono', 'email')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'telefono', 'email')  # Búsqueda por estos campos
    list_filter = ('nombre',)  # Filtro por nombre

admin.site.register(Proveedor, ProveedorAdmin)