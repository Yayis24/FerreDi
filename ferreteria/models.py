from django.db import models
from django.forms import forms


class Categories(models.Model):
    name = models.CharField(max_length=250)

class Measurement_Units(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=100)

class Products(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='products')
    measurement_unit = models.ForeignKey(Measurement_Units, on_delete=models.CASCADE, related_name='products')

class Inventories(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='inventories')
    amount = models.PositiveIntegerField()
    price = models.IntegerField()

class Sales(models.Model):
    amount = models.PositiveIntegerField()
    customer = models.CharField(max_length=100)
    total = models.IntegerField()

class Sale_Details(models.Model):
    amount = models.PositiveIntegerField()
    price = models.IntegerField()
    subtotal = models.IntegerField()
    inventory = models.ForeignKey(Inventories, on_delete=models.CASCADE, related_name='sale_details') 
    sale = models.ForeignKey(Sales, on_delete=models.CASCADE, related_name='sale_details')
