from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from login.forms import RegistroForm, LoginForm
from django.contrib.auth import get_user_model
import traceback

User = get_user_model()

def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                # create user but don't auto-login yet
                user = form.save(commit=False)
                # ensure password field present
                pwd = form.cleaned_data.get('password1') or form.cleaned_data.get('password')
                if not pwd:
                    messages.error(request, "No se recibió contraseña en cleaned_data.")
                    return render(request, 'login/registro.html', {'form': form})

                user.set_password(pwd)
                user.save()
                messages.success(request, "¡Tu cuenta ha sido creada con éxito!")
                return redirect('login:login')

            except Exception as e:
                # log traceback to console
                print("ERROR al guardar usuario:", e)
                traceback.print_exc()
                messages.error(request, f"Error al guardar usuario: {e}")
                # fallthrough: render form with errors shown
        else:
            # form invalido -> mostrar errores en consola y mensajes
            print("FORM INVALID:", form.errors.as_json())
            for field, errs in form.errors.items():
                for err in errs:
                    messages.error(request, f"{field}: {err}")
            # also non-field errors
            if form.non_field_errors():
                messages.error(request, f"No field errors: {form.non_field_errors()}")
    else:
        form = RegistroForm()

    return render(request, 'login/registro.html', {
        'form': form,
    })



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
                return redirect('core:inicio')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})


# Vista para cerrar sesión
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect('login:login')
