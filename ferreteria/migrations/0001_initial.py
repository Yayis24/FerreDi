# Generated by Django 4.2.3 on 2023-10-12 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('precio_inicial', models.IntegerField()),
                ('precio_venta', models.IntegerField()),
                ('cantidad_disponible', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='ferreteria.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('cliente', models.CharField(max_length=100)),
                ('fecha', models.DateField()),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ferreteria.producto')),
            ],
        ),
        migrations.AddField(
            model_name='inventario',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inventarios', to='ferreteria.producto'),
        ),
    ]
