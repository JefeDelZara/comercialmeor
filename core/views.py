# core/views.py
from django.shortcuts import render, redirect
from inventario.models import Producto, Categoria
from pedidos.models import Pedido, DetallePedido
from django.db.models import F, Q
from django.templatetags.static import static
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from itertools import zip_longest

from django.templatetags.static import static  # Importar static para usar en la vista

def inicio(request):
    # Obtener los últimos tres pedidos, ordenados por fecha
    ultimos_pedidos = Pedido.objects.all().order_by('-fecha_hora')[:4]
    
    # Obtener las categorías (si las necesitas para mostrar en la misma página)
    categorias = Categoria.objects.all()
    
    # Obtener productos asociados a los últimos pedidos, priorizando bajo stock
    productos_ids = DetallePedido.objects.filter(
        pedido__in=ultimos_pedidos  # Relación con los últimos pedidos
    ).values_list('producto_id', flat=True)

    # Consulta de productos con stock bajo o en pedidos recientes
    ultimos_movimientos = Producto.objects.filter(
        Q(id__in=productos_ids) |  # Productos asociados a los últimos pedidos
        Q(stock__lte=F('stock_minimo')) | Q(stock_minimo__isnull=True)  # Productos con stock bajo o sin stock mínimo
    ).order_by('stock', '-id')[:9]  # Priorizar bajo stock primero, luego por ID descendente

    # Obtener el último producto agregado al inventario
    ultimo_producto = Producto.objects.order_by('-id')[:6]

    # Preparar los productos con imagen predeterminada si no tienen imagen
    for producto in ultimos_movimientos:
        if not producto.imagen1:
            producto.imagen1_url = static('images/default.jpg')  # Ruta de la imagen predeterminada
        else:
            producto.imagen1_url = producto.imagen1.url  # Usar la URL de la imagen del producto

    for producto in ultimo_producto:
        if not producto.imagen1:
            producto.imagen1_url = static('images/default.jpg')  # Ruta de la imagen predeterminada
        else:
            producto.imagen1_url = producto.imagen1.url  # Usar la URL de la imagen del producto

    # Dividir los productos en grupos de 3
    grupos_productos = list(zip_longest(*[ultimos_movimientos[i::3] for i in range(3)]))

    return render(request, 'core/inicio.html', {
        'ultimos_pedidos': ultimos_pedidos,
        'categorias': categorias,
        'ultimos_movimientos': ultimos_movimientos,
        'ultimo_producto': ultimo_producto,  # Pasar el último producto agregado
        'grupos_productos': grupos_productos,  # Pasar los grupos de productos
    })


def productos(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all()

    # Filtrar productos según la categoría si se pasa un parámetro 'categoria' en la URL
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id)
    else:
        productos = Producto.objects.all()

    return render(request, 'core/productos.html', {
        'productos': productos,
        'categorias': categorias,
    })






def prueba_correo(request):
    send_mail(
        'Prueba de correo de stock bajo',
        'Este es un mensaje de prueba para verificar el envío de correo de stock bajo.',
        settings.EMAIL_HOST_USER,
        ['matiasaedo12343@gmail.com'],
        fail_silently=False,
    )
    return render(request, 'prueba_correo.html')



def enviar_consulta(request):
    if request.method == 'POST':
        tipo_consulta = request.POST.get('tipo_consulta')
        rut_empresa = request.POST.get('rut_empresa')
        nombre_apellido = request.POST.get('nombre_apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')
        
        # Enviar correo con los datos ingresados
        subject = f"Consulta de {nombre_apellido} - {tipo_consulta}"
        message = f"Tipo de consulta: {tipo_consulta}\n\nRut Empresa: {rut_empresa}\nNombre: {nombre_apellido}\nE-mail: {email}\nTeléfono: {telefono}\nMensaje:\n{mensaje}"
        recipient_email = 'matiasaedo12343@gmail.com'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [recipient_email],
            fail_silently=False,
        )
        
        messages.success(request, "Tu consulta ha sido enviada con éxito.")
        return redirect('consulta:formulario')  # Redirige al formulario o a una página de confirmación
    
    return render(request, 'consulta/consulta.html')



