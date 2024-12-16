from django.urls import path
from . import views
from .views import CategoriaAutocomplete, verificar_stock_bajo
from dal import autocomplete
from .models import Marca, Categoria

app_name = 'inventario'

urlpatterns = [
    path('', views.producto_list, name='producto_list'),  
    path('categoria-autocomplete/', CategoriaAutocomplete.as_view(), name='categoria-autocomplete'),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),  
    path('marca-autocomplete/', autocomplete.Select2QuerySetView.as_view(model=Marca), name='marca-autocomplete'),
    path('crear_categoria/', views.crear_categoria, name='crear_categoria'),
    path('eliminar_categoria/<int:pk>/', views.eliminar_categoria, name='eliminar_categoria'),
    path('productos/', views.producto_list, name='productos'),
    path('producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('verificar_stock_bajo/', verificar_stock_bajo, name='verificar_stock_bajo'),
    path('reporte_productos/', views.generar_reporte_pdf, name='reporte_productos'),

]
