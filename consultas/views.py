from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

def formulario_consulta(request):
    if request.method == 'POST':
        tipo_consulta = request.POST.get('tipo_consulta')
        rut_empresa = request.POST.get('rut_empresa')
        nombre_apellido = request.POST.get('nombre_apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')

        subject = f"Consulta de {nombre_apellido} - {tipo_consulta}"
        message = (
            f"Tipo de consulta: {tipo_consulta}\n\n"
            f"Rut Empresa: {rut_empresa}\n"
            f"Nombre: {nombre_apellido}\n"
            f"E-mail: {email}\n"
            f"Teléfono: {telefono}\n"
            f"Mensaje:\n{mensaje}"
        )

        try:
            send_mail(
                subject,
                message,
                'from@example.com',
                ['matiasaedo12343@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, "Tu consulta ha sido enviada con éxito.", extra_tags='consultas')
        except:
            messages.error(request, "Hubo un problema, intenta de nuevo.", extra_tags='consultas')

        return redirect(request.path)  # ← MÁS SIMPLE

    return render(request, 'consultas/consulta.html')
