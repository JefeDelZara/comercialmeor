from django.contrib import admin
from .models import Usuario

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')  # Campos a mostrar
    search_fields = ('username', 'email')  # Campos por los que se puede buscar
    list_filter = ('is_staff', 'is_active')  # Filtros para la lista

admin.site.register(Usuario, UsuarioAdmin)