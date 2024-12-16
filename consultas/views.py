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
        
        # Enviar correo con los datos ingresados
        subject = f"Consulta de {nombre_apellido} - {tipo_consulta}"
        message = f"Tipo de consulta: {tipo_consulta}\n\nRut Empresa: {rut_empresa}\nNombre: {nombre_apellido}\nE-mail: {email}\nTeléfono: {telefono}\nMensaje:\n{mensaje}"
        recipient_email = 'matiasaedo12343@gmail.com'
        
        try:
            send_mail(
                subject,
                message,
                'from@example.com',  # Cambia con tu correo
                [recipient_email],
                fail_silently=False,
            )
            # Si el correo se envía con éxito, muestra un mensaje de éxito
            messages.success(request, "Tu consulta ha sido enviada con éxito.")
        except Exception as e:
            # Si ocurre un error, muestra un mensaje de error
            messages.error(request, "Hubo un problema, intenta de nuevo.")
        
        return redirect('consultas:formulario')  # Redirige al formulario o a una página de confirmación
    
    return render(request, 'consultas/consulta.html')