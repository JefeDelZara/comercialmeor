from django.contrib import admin
from .models import Cliente

# Registro del modelo Cliente en el panel de administración
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'direccion', 'telefono', 'email')  # Campos a mostrar en la lista
    search_fields = ('usuario__username', 'direccion', 'telefono')  # Búsqueda por estos campos
    list_filter = ('usuario',)  # Filtro por usuario

admin.site.register(Cliente, ClienteAdmin)
