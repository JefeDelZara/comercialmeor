from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')),
    path('productos/', lambda request: redirect('/inventario/')),  # Redirige a inventario
    path('clientes/', include('clientes.urls')),
    path('', include('core.urls')),
    path('proveedores/', include('proveedores.urls')),
    path('pedidos/', include('pedidos.urls', namespace='pedidos')),
    path('login/', include('login.urls')),
    path('carrito/', include(('carrito.urls', 'carrito'), namespace='carrito')),
    path('facturas/', include('facturas.urls')),
    path('consultas/', include('consultas.urls')),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
