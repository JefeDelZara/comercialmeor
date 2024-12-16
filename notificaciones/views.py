from django.shortcuts import render
from .models import Notificacion
from django.http import JsonResponse


from .models import Pedido
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User

def ver_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    return render(request, 'notificaciones/ver_notificaciones.html', {'notificaciones': notificaciones})




def marcar_como_leido(request, notificacion_id):
    notificacion = Notificacion.objects.get(id=notificacion_id)
    if notificacion.usuario == request.user:
        notificacion.leido = True
        notificacion.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})




def reporte_pedidos(request):
    # Filtrado por fechas
    fecha_inicio = request.GET.get('fecha_inicio', timezone.now() - timedelta(days=30))
    fecha_fin = request.GET.get('fecha_fin', timezone.now())

    pedidos = Pedido.objects.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])

    return render(request, 'reportes/reporte_pedidos.html', {'pedidos': pedidos})





def lista_notificaciones(request):
    # Obtener todas las notificaciones del usuario
    notificaciones = Notificacion.objects.filter(usuario=request.user).order_by('-fecha_creacion')

    return render(request, 'notificaciones/lista_notificaciones.html', {
        'notificaciones': notificaciones,
    })

# notificaciones/views.py
from django.shortcuts import render
from .models import Notificacion

def mis_notificaciones(request):
    notificaciones = Notificacion.objects.filter(usuario=request.user)
    return render(request, 'notificaciones/mis_notificaciones.html', {'notificaciones': notificaciones})


# views.py
