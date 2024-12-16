# views.py en la app "pedidos"
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Pedido, DetallePedido
from .forms import CrearPedidoForm, EditarEstadoPedidoForm
from django.contrib import messages
from inventario.models import Producto
from django.db import IntegrityError


def lista_pedidos(request):
    if request.user.is_staff:
        pedidos = Pedido.objects.all()  # Los administradores ven todos los pedidos
    else:
        pedidos = Pedido.objects.filter(usuario=request.user)  # Los usuarios ven solo sus propios pedidos

    return render(request, 'pedidos/lista_pedidos.html', {'pedidos': pedidos})

@login_required
def crear_pedido(request):
    if request.method == 'POST':
        # Obtener el carrito desde la sesión
        carrito = request.session.get('carrito', [])
        
        if not carrito:
            # Si el carrito está vacío, redirigir al carrito
            messages.error(request, "Tu carrito está vacío.")
            return redirect('carrito')

        # Crear el pedido
        try:
            pedido = Pedido.objects.create(usuario=request.user)

            total_productos = 0
            subtotal = 0

            # Crear los detalles del pedido
            for item in carrito:
                try:
                    producto = Producto.objects.get(id=item['producto_id'])  # Obtener producto por ID
                except Producto.DoesNotExist:
                    messages.error(request, f"El producto con ID {item['producto_id']} no existe.")
                    return redirect('carrito')  # Redirige si hay un error con un producto

                cantidad = item['cantidad']

                # Crear el detalle del pedido
                detalle = DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=cantidad
                )

                total_productos += cantidad
                subtotal += detalle.total_producto  # Total por producto (cantidad * precio)

            # Actualizar el pedido con la cantidad total de productos y el subtotal
            pedido.total_productos = total_productos
            pedido.subtotal = subtotal
            pedido.save()

            # Vaciar el carrito
            request.session['carrito'] = []

            # Redirigir al detalle del pedido
            messages.success(request, "Pedido realizado exitosamente.")
            return redirect('pedidos:detalle_pedido', pedido_id=pedido.id)

        except IntegrityError as e:
            # Manejo de errores de base de datos (ej. problemas de integridad)
            messages.error(request, "Hubo un error al procesar tu pedido. Intenta nuevamente.")
            return redirect('carrito')

    return render(request, 'pedidos/crear_pedido.html')


@login_required
def detalle_pedido(request, pedido_id):
    # Obtener el pedido con los detalles asociados
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)

    return render(request, 'pedidos/detalle_pedido.html', {'pedido': pedido})

@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        pedido.estado = nuevo_estado
        pedido.save()
        messages.success(request, "El estado del pedido ha sido actualizado.")
        return redirect('pedidos:lista_pedidos')

    return render(request, 'pedidos/editar_pedido.html', {'pedido': pedido})

@login_required
def procesar_pago(request):
    if request.method == 'POST':
        # Lógica de pago (simulada aquí por una validación simple)
        pago_exitoso = True  # Aquí simulas que el pago es exitoso

        if pago_exitoso:
            # Aquí se crean los pedidos si el pago es exitoso
            productos_seleccionados = [{'producto_id': 1, 'cantidad': 2}, {'producto_id': 2, 'cantidad': 1}]  # Ejemplo

            # Crear un pedido
            pedido = Pedido.objects.create(usuario=request.user, estado='pendiente')

            # Crear los detalles del pedido
            for item in productos_seleccionados:
                producto = Producto.objects.get(id=item['producto_id'])
                DetallePedido.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidad=item['cantidad']
                )

            # Confirmar que el pedido se ha creado
            print(f"Pedido creado con ID {pedido.id}")

            # Redirigir al usuario a la página de confirmación
            return redirect('pedidos:confirmacion_pedido', pedido_id=pedido.id)

        else:
            # Si el pago no es exitoso, manejar el error aquí
            messages.error(request, "Hubo un error al procesar el pago.")
            return redirect('inventario:productos')

    return render(request, 'pagos/procesar_pago.html')




def ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'pedidos/ver_pedido.html', {'pedido': pedido})


def eliminar_pedido(request, pedido_id):
    if request.method == 'POST' and request.user.is_staff:
        pedido = get_object_or_404(Pedido, id=pedido_id)
        pedido.delete()  # Elimina el pedido
        return redirect('pedidos:lista_pedidos')  # Redirige a la lista de pedidos
    return redirect('pedidos:lista_pedidos') 