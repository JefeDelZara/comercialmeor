from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from .models import Pedido

def generar_factura(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    # Crear respuesta PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{pedido.id}.pdf"'

    # PDF con márgenes
    pdf = SimpleDocTemplate(response, pagesize=letter,
                            rightMargin=40, leftMargin=40,
                            topMargin=60, bottomMargin=40)

    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph(f"<b>Factura - Pedido #{pedido.id}</b>", styles["Title"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 20))

    # Datos del usuario
    cliente_info = f"""
    <b>Cliente:</b> {pedido.usuario.username}<br/>
    <b>Correo:</b> {pedido.usuario.email}<br/>
    """
    elementos.append(Paragraph(cliente_info, styles["Normal"]))
    elementos.append(Spacer(1, 20))

    # Tabla de productos
    data = [["Producto", "Cantidad", "Precio Total"]]

    total = 0
    for detalle in pedido.detallepedido_set.all():
        data.append([
            detalle.producto.nombre,
            str(detalle.cantidad),
            f"${detalle.total_producto}"
        ])
        total += detalle.total_producto

    # Agregar total
    data.append(["", "<b>Subtotal</b>", f"<b>${total}</b>"])

    tabla = Table(data, colWidths=[260, 80, 100])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8e8")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.6, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 30))

    # Mensaje final
    elementos.append(Paragraph("Gracias por su compra.", styles["Normal"]))

    # Construir PDF
    pdf.build(elementos)

    return response
