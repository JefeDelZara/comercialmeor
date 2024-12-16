from django.urls import path
from . import views

app_name = 'pedidos'

urlpatterns = [
    path('lista/', views.lista_pedidos, name='lista_pedidos'),
    path('crear/', views.crear_pedido, name='crear_pedido'),
    path('<int:pedido_id>/detalle/', views.detalle_pedido, name='detalle_pedido'),
    path('<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('procesar_pago/', views.procesar_pago, name='procesar_pago'),
    path('pedidos/ver/<int:pedido_id>/', views.ver_pedido, name='ver_pedido'),
    path('pedidos/eliminar/<int:pedido_id>/', views.eliminar_pedido, name='eliminar_pedido'),
]
    

