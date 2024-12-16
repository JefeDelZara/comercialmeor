from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from login.forms import RegistroForm, LoginForm
from firebase_admin import auth,  credentials
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
import firebase_admin







# Vista para el registro de un nuevo usuario
def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guardamos el usuario, incluido el tipo de usuario
            login(request, user)  # Loguear al usuario inmediatamente después de registrarse
            messages.success(request, "¡Te has registrado exitosamente!")
            return redirect('core:inicio')  # Cambia esto por la URL a la que quieras redirigir al usuario
        else:
            messages.error(request, "Error en el registro. Verifica los campos.")
    else:
        form = RegistroForm()
    
    return render(request, 'login/registro.html', {'form': form})

# Vista para iniciar sesión
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Has iniciado sesión correctamente.")
                return redirect('core:inicio')   # Redirige a una página de inicio después del login
            else:
                messages.error(request, "Datos de inicio de sesión incorrectos.")
        else:
            messages.error(request, "Error en el formulario de inicio de sesión.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect('login:login')  # Redirige al login después de cerrar sesión






