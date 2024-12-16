# forms.py en la app "pedidos"
from django import forms
from .models import Pedido, DetallePedido, Producto

class CrearPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['usuario']  # Usuario será automáticamente el que lo hace en la vista.

    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Seleccionar productos"
    )

class EditarEstadoPedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['estado']
