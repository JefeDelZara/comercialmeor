from django import forms
from usuarios.models import Usuario
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Contraseña'
        }),
        label="Contraseña"
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirmar contraseña'
        }),
        label="Confirmar contraseña"
    )

    # Eliminamos la opción ADMIN por seguridad
    tipo_usuario = forms.ChoiceField(
        choices=[('CLIENTE', 'Cliente')],
        label="Tipo de usuario",
        widget=forms.Select(attrs={
            'placeholder': 'Tipo de usuario'
        })
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'tipo_usuario']

        labels = {
            'username': "Nombre de usuario",
            'email': "Correo electrónico",
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Nombre de usuario'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Correo electrónico'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')

        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Encriptar contraseña
        user.set_password(self.cleaned_data['password1'])

        # Forzar que SIEMPRE sea cliente (seguridad extra)
        user.tipo_usuario = 'CLIENTE'

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nombre de usuario",
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Nombre de usuario"
        })
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            "placeholder": "Contraseña"
        })
    )
