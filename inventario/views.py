# inventario/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria
from .forms import ProductoForm, CategoriaForm
from django.contrib import messages
from dal import autocomplete
from django.views.generic import CreateView
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.db.models import F
import logging


from django.db.models import F

from django.db.models import F

def producto_list(request):
    # Obtener el término de búsqueda ingresado
    query = request.GET.get('buscar', '')

    # Obtener el filtro de categoría seleccionado
    categoria_id = request.GET.get('categoria')

    # Obtener la opción de ordenamiento seleccionada
    ordenar = request.GET.get('ordenar')

    # Verificar si se debe incluir productos agotados
    mostrar_agotados = request.GET.get('agotado') == 'true'

    # Verificar si se debe mostrar productos con bajo stock
    mostrar_bajo_stock = request.GET.get('bajo_stock') == 'true'

    # Verificar si se ha activado o desactivado la alerta de stock
    if 'alertas_stock' in request.GET:
        # Guardar la preferencia en la sesión
        request.session['alertas_stock'] = request.GET['alertas_stock']

    # Obtener el valor de las alertas de stock desde la sesión (por defecto "false" si no se ha configurado)
    alertas_stock = request.session.get('alertas_stock', 'false')

    # Filtrar los productos
    productos = Producto.objects.all().select_related('categoria')  # Optimización con select_related

    # Aplicar búsqueda por nombre si hay un término de búsqueda
    if query:
        productos = productos.filter(nombre__icontains=query)

    # Filtrar por categoría si se ha seleccionado una
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Filtrar productos agotados si la casilla está marcada
    if not mostrar_agotados:
        productos = productos.filter(stock__gt=0)

    # Filtrar productos con bajo stock si la opción está activada
    if mostrar_bajo_stock:
        productos = productos.filter(stock__lte=F('stock_minimo'))

    # Ordenar los productos si se ha seleccionado una opción
    if ordenar == 'mayor_stock':
        productos = productos.order_by('-stock')
    elif ordenar == 'menor_stock':
        productos = productos.order_by('stock')

    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()

    # Pasar los datos a la plantilla
    return render(request, 'inventario/productos.html', {
        'productos': productos,
        'categorias': categorias,
        'request': request,
        'alertas_stock': alertas_stock,  # Pasar el valor de las alertas de stock
    })







def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Pasa request.FILES también
        if form.is_valid():
            producto = form.save()  # Guarda el producto
            verificar_stock_bajo(request)  # Llama a la función para verificar el stock bajo
            return redirect('inventario:producto_list')  # Asegúrate de redirigir correctamente a la lista de productos
    else:
        form = ProductoForm()

    categoria_form = CategoriaForm()
    categorias = Categoria.objects.all()

    return render(request, 'inventario/crear_producto.html', {
        'form': form,
        'categoria_form': categoria_form,
        'categorias': categorias,
    })




def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Asegúrate de pasar 'request.FILES' para manejar los archivos cargados (imágenes)
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            producto = form.save()  # Guarda el producto editado
            verificar_stock_bajo(request)  # Llama a la función para verificar el stock bajo
            return redirect('inventario:producto_list')  # Redirige a la lista de productos
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'inventario/editar_producto.html', {'form': form, 'producto': producto})




def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('inventario:producto_list')  # Usa el prefijo si tienes app_name
    return render(request, 'inventario/eliminar_producto.html', {'producto': producto})


from django.http import JsonResponse


class CategoriaAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Si el usuario está autenticado, mostramos las categorías
        if not self.request.user.is_authenticated:
            return Categoria.objects.none()

        # Filtrar las categorías basadas en la búsqueda del usuario
        qs = Categoria.objects.all()

        if self.q:
            qs = qs.filter(nombre__icontains=self.q)  # Filtrar por el nombre de la categoría

        return qs



def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)  # Asegúrate de pasar request.FILES para cargar imágenes
        if form.is_valid():
            form.save()
            return redirect('inventario:crear_producto')  # Redirige a la URL de crear producto
    else:
        form = CategoriaForm()

    return render(request, 'inventario/crear_categoria.html', {'form': form})

def eliminar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        return redirect('inventario:producto_list')  # Redirige a la lista de productos o la página que desees

    return render(request, 'inventario/eliminar_categoria.html', {'categoria': categoria})


def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'inventario/detalle_producto.html', {'producto': producto})





logger = logging.getLogger(__name__)



from .models import Producto, Categoria

def verificar_stock_bajo(request):
    productos_con_stock_bajo = Producto.objects.filter(stock__lte=F('stock_minimo'))
    

    if productos_con_stock_bajo.exists():
        asunto = "Alerta: Productos con Bajo Stock"
        mensaje = "Los siguientes productos tienen stock bajo:\n"
        for producto in productos_con_stock_bajo:
            mensaje += f"- {producto.nombre}: {producto.stock} unidades disponibles.\n"

        send_mail(
            asunto,
            mensaje,
            settings.EMAIL_HOST_USER,
            ['matiasaedo12343@gmail.com'],  # Cambia por el correo de destino
            fail_silently=False,
        )

    return render(
        request,
        'inventario/productos.html',
        {
            'productos': productos_con_stock_bajo,
            
        }
    )



def enviar_alerta_stock_bajo_html(producto):
    subject = f"Alerta: Stock Bajo de {producto.nombre}"
    message = render_to_string('core/stock_bajo_email.html', {'producto': producto})
    recipient_list = ['matiasaedo12343@gmail.com']

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, html_message=message)

from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Producto

def generar_reporte_pdf(request):
    # Crear una respuesta Http con el tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_productos.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)

    # Definir las coordenadas iniciales para el texto
    x = 100
    y = 750

    # Agregar título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(x, y, "Reporte de Productos")
    y -= 30

    # Agregar encabezados de columna
    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Nombre")
    p.drawString(x + 200, y, "Cantidad")
    p.drawString(x + 300, y, "Precio")
    y -= 20

    # Agregar productos
    p.setFont("Helvetica", 10)
    productos = Producto.objects.all()
    for producto in productos:
        color = (1, 0, 0) if producto.stock <= producto.stock_minimo else (0, 0, 0)  # Rojo si hay bajo stock
        p.setFillColorRGB(*color)
        p.drawString(x, y, producto.nombre)
        p.drawString(x + 200, y, str(producto.stock))
        p.drawString(x + 300, y, f"${producto.precio_venta}")
        y -= 15

    # Guardar el PDF y devolverlo
    p.showPage()
    p.save()

    return response
