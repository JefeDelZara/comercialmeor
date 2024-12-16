from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'direccion', 'telefono', 'email', 'rut', 'observaciones']

    usuario = forms.CharField(max_length=100, label="Nombre")  # Campo Nombre, basado en el usuario
    telefono = forms.CharField(max_length=20, label="Número de teléfono")
    direccion = forms.CharField(widget=forms.Textarea, label="Dirección")
    rut = forms.CharField(max_length=12, label="RUT")
    observaciones = forms.CharField(widget=forms.Textarea, required=False, label="Observaciones")



class EditarClienteForm(forms.ModelForm):
    # Campos para editar el cliente
    nombre = forms.CharField(max_length=30, label="Nombre")
    apellido = forms.CharField(max_length=30, label="Apellido")
    rut = forms.CharField(max_length=12, label="RUT")
    telefono = forms.CharField(max_length=20, label="Teléfono")
    direccion = forms.CharField(widget=forms.Textarea, label="Dirección")
    observaciones = forms.CharField(widget=forms.Textarea, required=False, label="Observaciones")

    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'direccion', 'observaciones']  # Incluye los campos que quieres editar

    def __init__(self, *args, **kwargs):
        # Este es el código que permite pasar el usuario a la instancia del formulario
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Guardamos los cambios en el cliente
        cliente = super().save(commit=False)
        
        if commit:
            cliente.save()
        return cliente
