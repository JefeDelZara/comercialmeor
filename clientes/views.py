# clientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente
from .forms import ClienteForm, EditarClienteForm
from usuarios.models import Usuario
from django.contrib import messages

def cliente_list(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/cliente_list.html', {
        'clientes': clientes
    })

def crear_cliente(request):
    if request.method == 'POST':
        cliente_form = ClienteForm(request.POST)
        if cliente_form.is_valid():
            email = cliente_form.cleaned_data['email']

            # Verificar si el correo electrónico ya está registrado
            if User.objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
                return render(request, 'clientes/crear_cliente.html', {
                    'cliente_form': cliente_form,
                })
            else:
                # Crear el usuario relacionado primero
                usuario = User.objects.create_user(
                    username=cliente_form.cleaned_data["rut"],  # Usamos el RUT como nombre de usuario
                    email=email,
                    first_name=cliente_form.cleaned_data["nombre"],
                    last_name=cliente_form.cleaned_data["apellido"],
                )
                usuario.set_password("password123")  # Configura una contraseña predeterminada
                usuario.save()

                # Luego creamos el cliente y lo asociamos al usuario
                cliente = cliente_form.save(commit=False)
                cliente.usuario = usuario  # Asociamos el usuario al cliente
                cliente.save()

                messages.success(request, "El cliente ha sido creado exitosamente.")
                return redirect('clientes:cliente_list')  # Redirige a la lista de clientes

    else:
        cliente_form = ClienteForm()

    return render(request, 'clientes/crear_cliente.html', {
        'cliente_form': cliente_form,
    })


def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = EditarClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes:clientes_list')  # Redirige a la lista de clientes
    else:
        form = EditarClienteForm(instance=cliente)

    return render(request, 'clientes/editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)  # Obtiene el cliente o lanza 404

    if request.method == 'POST':
        cliente.delete()  # Elimina el cliente de la base de datos
        return redirect('clientes:clientes_list')  # Redirige a la lista de clientes

    return render(request, 'clientes/eliminar_cliente.html', {'cliente': cliente})

def lista_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/cliente_list.html', {'clientes': clientes})
