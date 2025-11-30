from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Pedido
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas

def generar_factura(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Crear la respuesta HTTP con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{pedido.id}.pdf"'

    # Crear un objeto de PDF
    pdf = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Medidas de la página (ancho, alto)

    # Título de la factura
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(200, height - 40, f"Factura - Pedido #{pedido.id}")

    # Detalles del usuario
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, height - 80, f"Nombre de usuario: {pedido.usuario.username}")
    pdf.drawString(30, height - 100, f"Correo: {pedido.usuario.email}")

    # Verificar si el teléfono está disponible en el usuario, si no, poner "No disponible"


    # Detalles de los productos en el pedido
    y_position = height - 160
    pdf.drawString(30, y_position, "Productos:")
    y_position -= 20
    pdf.setFont("Helvetica", 10)

    total = 0
    for detalle in pedido.detallepedido_set.all():
        producto = detalle.producto
        cantidad = detalle.cantidad
        precio_total = detalle.total_producto
        total += precio_total
        pdf.drawString(30, y_position, f"{producto.nombre} (x{cantidad}) - ${precio_total}")
        y_position -= 20

    # Subtotal
    y_position -= 20
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(30, y_position, f"Subtotal: ${total}")

    # Mensaje final
    y_position -= 40
    pdf.setFont("Helvetica", 12)
    pdf.drawString(30, y_position, "Gracias por preferirnos.")

    # Finalizar la creación del PDF
    pdf.showPage()
    pdf.save()

    return response
