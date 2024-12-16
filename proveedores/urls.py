# urls.py
from django.urls import path
from . import views

app_name = 'proveedores'

urlpatterns = [
    path('', views.lista_proveedores, name='lista_proveedores'),
    path('proveedor/crear/', views.crear_proveedor, name='crear_proveedor'),
    path('proveedor/editar/<int:pk>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedor/eliminar/<int:pk>/', views.eliminar_proveedor, name='eliminar_proveedor'),
]
