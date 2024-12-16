# Generated by Django 5.1.3 on 2024-12-13 06:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carrito', '0001_initial'),
        ('inventario', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='carrito',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='carrito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='carrito.carrito'),
        ),
        migrations.AddField(
            model_name='carritoitem',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto'),
        ),
    ]
