# Generated by Django 4.2.3 on 2023-11-21 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ferreteria', '0008_saledetails_delete_sale_details'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SaleDetails',
            new_name='Sale_Details',
        ),
    ]