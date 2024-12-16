from dal import autocomplete
from django import forms
from .models import Producto, Categoria

class ProductoForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        empty_label="Seleccione una categoría",
    )

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio_venta', 'precio_compra', 
            'categoria', 'marca', 'stock', 'stock_minimo', 
            'imagen1', 'imagen2', 'imagen3'
        ]



class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'imagen']  # Aquí incluye los campos que quieras mostrar en el formulario
