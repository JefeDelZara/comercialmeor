import re
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

def validar_rut(rut):
    return bool(re.match(r'^\d{7,8}-[\dkK]$', rut))

def validar_email(email):
    return bool(re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email))

def validar_telefono(tel):
    return bool(re.match(r'^\d{9}$', tel))


def formulario_consulta(request):
    context = {}

    if request.method == 'POST':
        tipo_consulta = request.POST.get('tipo_consulta', '').strip()
        rut_empresa = request.POST.get('rut_empresa', '').strip()

        # NUEVO: Se obtiene nombre y apellido por separado
        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()

        nombre_apellido = f"{nombre} {apellido}"

        email = request.POST.get('email', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()

        context = {
            'tipo_consulta': tipo_consulta,
            'rut_empresa': rut_empresa,
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
            'telefono': telefono,
            'mensaje': mensaje,
        }

        errores = False

        # Validaciones
        if tipo_consulta == "":
            messages.error(request, "Debes seleccionar un tipo de consulta.", extra_tags='consultas')
            errores = True

        if not validar_rut(rut_empresa):
            messages.error(request, "El RUT debe tener el formato 12345678-9", extra_tags='consultas')
            errores = True

        if len(nombre) < 2 or not nombre.isalpha():
            messages.error(request, "El nombre debe tener mínimo 2 letras y solo contener letras.", extra_tags='consultas')
            errores = True

        if len(apellido) < 2 or not apellido.isalpha():
            messages.error(request, "El apellido debe tener mínimo 2 letras y solo contener letras.", extra_tags='consultas')
            errores = True

        if not validar_email(email):
            messages.error(request, "El correo electrónico no es válido.", extra_tags='consultas')
            errores = True

        if not validar_telefono(telefono):
            messages.error(request, "El teléfono debe tener exactamente 9 dígitos.", extra_tags='consultas')
            errores = True

        if len(mensaje) < 5:
            messages.error(request, "El mensaje debe tener mínimo 5 caracteres.", extra_tags='consultas')
            errores = True

        # Si hay errores, recargar con mensajes
        if errores:
            return render(request, 'consultas/consulta.html', context)

        # ENVIAR CORREO
        try:
            subject = f"Consulta de {nombre_apellido} - {tipo_consulta}"
            contenido = (
                f"Tipo de consulta: {tipo_consulta}\n\n"
                f"Rut Empresa: {rut_empresa}\n"
                f"Nombre: {nombre_apellido}\n"
                f"E-mail: {email}\n"
                f"Teléfono: {telefono}\n"
                f"Mensaje:\n{mensaje}"
            )

            send_mail(
                subject,
                contenido,
                'from@example.com',
                ['matiasaedo12343@gmail.com'],
                fail_silently=False,
            )

            messages.success(request, "Tu mensaje se ha sido enviado correctamente, nos pondremos en contacto con usted lo más rápidamente posible.", extra_tags='consultas')
            return redirect('consultas:formulario')

        except Exception as e:
            print("ERROR MAIL:", e)
            messages.error(request, "Hubo un problema al enviar el correo.", extra_tags='consultas')

    return render(request, 'consultas/consulta.html', context)
