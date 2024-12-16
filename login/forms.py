from django import forms
from usuarios.models import Usuario 
from django.contrib.auth.forms import AuthenticationForm  # Asegúrate de importar el modelo Usuario

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)  # Campo para la contraseña
    tipo_usuario = forms.ChoiceField(choices=[('CLIENTE', 'Cliente'), ('ADMIN', 'Administrador')])  # Cambiar a mayúsculas

    class Meta:
        model = Usuario  # Especifica que usarás el modelo Usuario
        fields = ['username', 'email', 'password', 'tipo_usuario']  # Agregamos tipo_usuario a los campos del formulario

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Encripta la contraseña
        user.tipo_usuario = self.cleaned_data['tipo_usuario']  # Asignamos el tipo de usuario seleccionado
        if commit:
            user.save()  # Guarda el usuario
        return user




class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario", max_length=100)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
