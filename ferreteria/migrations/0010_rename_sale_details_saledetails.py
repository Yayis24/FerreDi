# Generated by Django 4.2.3 on 2023-11-21 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0009_rename_saledetails_sale_details'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Sale_Details',
            new_name='SaleDetails',
        ),
    ]
