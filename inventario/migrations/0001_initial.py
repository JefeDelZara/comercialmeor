# Generated by Django 5.1.3 on 2024-12-13 06:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='categorias/')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('marca', models.CharField(max_length=100)),
                ('stock', models.IntegerField()),
                ('stock_minimo', models.IntegerField(default=10)),
                ('imagen1', models.ImageField(upload_to='productos/')),
                ('imagen2', models.ImageField(blank=True, upload_to='productos/')),
                ('imagen3', models.ImageField(blank=True, upload_to='productos/')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.categoria')),
            ],
        ),
    ]
