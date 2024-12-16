from django.urls import path
from . import views

app_name = 'factura'

urlpatterns = [
    # Otros endpoints de la app
    path('generar_factura/<int:pedido_id>/', views.generar_factura, name='generar_factura'),
]
