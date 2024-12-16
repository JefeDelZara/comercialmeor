from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('realizar-pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('productos/', views.productos_disponibles, name='productos_disponibles'), 
    path('pedido-exitoso/', views.pedido_exitoso, name='pedido_exitoso'),  # Asegúrate de que esté aquí
    path('reducir-cantidad/<int:item_id>/', views.reducir_cantidad, name='reducir_cantidad'),
    path('aumentar-cantidad/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('eliminar-producto/<int:item_id>/', views.eliminar_producto, name='eliminar_producto'), 
    path('actualizar-carrito/', views.actualizar_carrito, name='actualizar_carrito'),
 # Agrega este
  # Agrega este

    
]