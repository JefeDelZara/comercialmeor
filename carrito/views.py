from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, CarritoItem
from inventario.models import Producto, Categoria
from pedidos.models import Pedido, DetallePedido
from django.contrib import messages
from django.core.mail import send_mail


# Vista para mostrar el carrito
@login_required
def mostrar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        messages.error(request, "No tienes productos en el carrito.")
        return redirect('ver_carrito')

    return render(request, 'carrito/carrito.html', {'carrito': carrito})


# Vista para ver el carrito y modificar la cantidad de productos

@login_required
def ver_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()

    if request.method == "POST":
        # Modificar cantidad del carrito
        for item_id, nueva_cantidad in request.POST.items():
            if item_id.startswith('cantidad_'):
                item_id = item_id.replace('cantidad_', '')
                carrito_item = CarritoItem.objects.get(id=item_id, carrito=carrito)
                nueva_cantidad = int(nueva_cantidad)
                if nueva_cantidad <= 0:
                    carrito_item.delete()
                else:
                    # Verifica que no sobrepase el stock
                    if nueva_cantidad <= carrito_item.producto.stock:
                        carrito_item.cantidad = nueva_cantidad
                        carrito_item.save()
                    else:
                        messages.error(request, "No hay suficiente stock para ese producto.")
                
        return redirect('carrito:ver_carrito')  # Aquí es donde se usa el nombre de la ruta 'ver_carrito'

    return render(request, 'carrito/carrito.html', {'carrito': carrito})


# Vista para agregar productos al carrito
def agregar_al_carrito(request, producto_id):

    # Si el usuario NO está autenticado → mensaje + redirección correcta
    if not request.user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para agregar productos al carrito.")
        return redirect(f"/login/?next=/carrito/agregar_al_carrito/{producto_id}/")

    # --- Lógica normal ---
    producto = get_object_or_404(Producto, pk=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    cantidad_a_agregar = int(request.POST.get('cantidad', 1))

    if cantidad_a_agregar > producto.stock:
        messages.error(request, "No hay suficiente stock para este producto.")
        return redirect('inventario:detalle_producto', id=producto.id)

    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        nueva_cantidad = carrito_item.cantidad + cantidad_a_agregar
        if nueva_cantidad > producto.stock:
            messages.error(request, "La cantidad solicitada supera el stock disponible.")
        else:
            carrito_item.cantidad = nueva_cantidad
            carrito_item.save()
            messages.success(request, "Producto actualizado en el carrito.")
    else:
        carrito_item.cantidad = cantidad_a_agregar
        carrito_item.save()
        messages.success(request, "Producto agregado al carrito.")

    return redirect('inventario:detalle_producto', id=producto.id)



def pedido_exitoso(request):
    return render(request, 'carrito/pedido_exitoso.html')

# Vista para realizar el pedido
from django.core.mail import send_mail
from django.template.loader import render_to_string  # Para renderizar una plantilla HTML
from django.utils.html import strip_tags  # Para asegurarnos de que los correos tengan formato HTML

@login_required
def realizar_pedido(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        messages.error(request, "No tienes productos en el carrito.")
        return redirect('carrito:ver_carrito')

    # Crear el pedido
    pedido = Pedido.objects.create(usuario=request.user, estado='Pendiente')

    total_productos = 0
    subtotal = 0

    # Procesar cada producto en el carrito
    for item in carrito.items.all():
        producto = item.producto
        cantidad = item.cantidad
        
        # Verificar que haya suficiente stock
        if cantidad <= producto.stock:
            producto.stock -= cantidad  # Descontar del stock
            producto.save()
            
            # Crear el detalle del pedido
            detalle = DetallePedido.objects.create(
                pedido=pedido,
                producto=producto,
                cantidad=cantidad
            )

            # Actualizar el total de productos y el subtotal
            total_productos += cantidad
            subtotal += detalle.total_producto  # total_producto puede ser cantidad * precio del producto
        else:
            messages.error(request, f"No hay suficiente stock de {producto.nombre}")
            return redirect('carrito:ver_carrito')

    # Actualizar el pedido con la cantidad total de productos y el subtotal
    pedido.total_productos = total_productos
    pedido.subtotal = subtotal
    pedido.save()

    # Preparar el contenido del correo
    subject = "Nuevo Pedido Realizado"
    message = f"El usuario {request.user.username} ha realizado un pedido."

    # Crear el cuerpo del mensaje en formato HTML
    context = {
        'user': request.user,
        'pedido': pedido,
    }
    html_message = render_to_string('carrito/pedido_confirmacion_email.html', context)
    plain_message = strip_tags(html_message)  # Versión en texto plano para clientes que no soportan HTML

    # Enviar correo con contenido HTML
    send_mail(
        subject,
        plain_message,
        'from@example.com',
        ['matiasaedo12343@gmail.com'],
        html_message=html_message  # Aquí se pasa el cuerpo en HTML
    )

    # Limpiar carrito después de hacer el pedido
    carrito.items.all().delete()
    messages.success(request, "Pedido realizado con éxito.")
    return redirect('carrito:pedido_exitoso')



@login_required
def productos_disponibles(request):
    productos = Producto.objects.filter(stock__gt=0)  # Filtra productos con stock disponible
    return render(request, 'carrito/productos_disponibles.html', {'productos': productos})

def productos_disponibles(request):
    # Obtener todas las categorías
    categorias = Categoria.objects.all()
    
    # Filtrar productos
    productos = Producto.objects.all()

    # Filtrar por categoría si se pasa el parámetro 'categoria'
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Filtrar por nombre si se pasa el parámetro 'search'
    search = request.GET.get('search')
    if search:
        productos = productos.filter(nombre__icontains=search)

    return render(request, 'carrito/productos_disponibles.html', {
        'productos': productos,
        'categorias': categorias,
        'search': search,
    })

def confirmar_pedido(request, pedido_id):
    pedido = Pedido.objects.get(id=pedido_id)
    context = {
        'user': request.user,
        'pedido': pedido
    }
    return render(request, 'carrito/pedido_confirmacion_email.html', context)


@login_required
def reducir_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        messages.info(request, "La cantidad no puede ser menor a 1. Usa el botón de eliminar si deseas quitar el producto.")
    return redirect('carrito:ver_carrito')

@login_required
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)

    # Incrementa la cantidad solo si hay suficiente stock disponible
    if item.producto.stock > item.cantidad:
        item.cantidad += 1
        item.save()
    else:
        from django.contrib import messages
        messages.error(request, f"No hay suficiente stock para {item.producto.nombre}")

    return redirect('carrito:ver_carrito')

@login_required
def eliminar_producto(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id, carrito__usuario=request.user)
    item.delete()
    return redirect('carrito:ver_carrito')

@login_required
def actualizar_carrito(request):
    carrito = Carrito.objects.filter(usuario=request.user).first()
    if carrito:
        carrito.recalcular_totales()  # Ahora se utiliza el método definido
    return redirect('carrito:ver_carrito')


