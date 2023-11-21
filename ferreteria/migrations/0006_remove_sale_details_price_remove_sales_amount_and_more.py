# Generated by Django 4.2.3 on 2023-11-21 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0005_alter_products_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale_details',
            name='price',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='amount',
        ),
        migrations.AddField(
            model_name='sales',
            name='date_time',
            field=models.DateTimeField(null=True),
        ),
    ]