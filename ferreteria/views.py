from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ferreteria.models import Categories, Measurement_Units, Products, Inventories, Sale_Details, Sales
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def home(request):
    return render(request, 'paginas/home.html')

@login_required

@csrf_exempt
def Category(request):
    if request.method == 'POST':
        if 'edit_id' in request.POST:
            # Manejar la edición de la categoría existente
            edit_id = request.POST.get('edit_id')
            category_to_edit = Categories.objects.get(id=edit_id)
            category_to_edit.name = request.POST.get('edit_nombre')
            category_to_edit.save()
        elif 'delete_id' in request.POST:
            # Manejar la eliminación de la categoría existente
            delete_id = request.POST.get('delete_id')
            Categories.objects.get(id=delete_id).delete()
        else:
            # Manejar la creación de una nueva categoría
            name = request.POST.get('nombre')
            Categories.objects.create(name=name)
        return redirect('category')

    if request.method == 'GET':
        # Mostrar la página de categorías
        edit_id = request.GET.get('edit_id')
        if edit_id:
            category_to_edit = Categories.objects.get(id=edit_id)
            return render(request, 'paginas/category.html', {'categories': Categories.objects.all(), 'edit_id': edit_id, 'category_to_edit': category_to_edit})

    categories = Categories.objects.all()
    return render(request, 'paginas/category.html', {'categories': categories})

@csrf_exempt
def Measurement_Unit(request):
    if request.method == 'POST':
        if 'edit_id' in request.POST:
            # Manejar la edición de la categoría existente
            edit_id = request.POST.get('edit_id')
            measurement_unit_to_edit = Measurement_Units.objects.get(id=edit_id)
            measurement_unit_to_edit.name = request.POST.get('edit_nombre')
            measurement_unit_to_edit.abbreviation = request.POST.get('edit_abreviacion')
            measurement_unit_to_edit.save()
        elif 'delete_id' in request.POST:
            # Manejar la eliminación de la categoría existente
            delete_id = request.POST.get('delete_id')
            Measurement_Units.objects.get(id=delete_id).delete()
        else:
            # Manejar la creación de una nueva categoría
            name = request.POST.get('nombre')
            abbreviation = request.POST.get('abreviacion')
            Measurement_Units.objects.create(name=name, abbreviation=abbreviation)

        return redirect('measurement_unit')

    if request.method == 'GET':
        # Mostrar la página de categorías
        edit_id = request.GET.get('edit_id')
        if edit_id:
            measurement_unit_to_edit = Measurement_Units.objects.get(id=edit_id)
            return render(request, 'paginas/measurement_unit.html', {'measurement_units': Measurement_Units.objects.all(), 'edit_id': edit_id, 'measurement_unity_to_edit': measurement_unit_to_edit})

    measurement_units = Measurement_Units.objects.all()
    return render(request, 'paginas/measurement_unit.html', {'measurement_units': measurement_units})

@csrf_exempt
def products(request):
    if request.method == 'POST':
        if 'edit_id' in request.POST:
            # Manejar la edición del producto existente
            edit_id = request.POST.get('edit_id')
            product_to_edit = Products.objects.get(id=edit_id)
            product_to_edit.name = request.POST.get('edit_nombre')
            product_to_edit.description = request.POST.get('edit_descripcion')
            if product_to_edit.description == '':
                product_to_edit.description = None
            product_to_edit.price = request.POST.get('edit_precio')
            product_to_edit.category = Categories.objects.get(id=request.POST.get('edit_categoria'))
            product_to_edit.measurement_unit = Measurement_Units.objects.get(id=request.POST.get('edit_unidad_medida'))
            product_to_edit.save()
        elif 'delete_id' in request.POST:
            # Manejar la eliminación del producto existente
            delete_id = request.POST.get('delete_id')
            Products.objects.get(id=delete_id).delete()
        else:
            # Manejar la creación de un nuevo producto
            name = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            precio = request.POST.get('precio')
            categoria = Categories.objects.get(id=request.POST.get('categoria'))
            unidad_medida = Measurement_Units.objects.get(id=request.POST.get('unidad_medida'))
            if descripcion == '':
                descripcion = None
            products = Products.objects.create(name=name, description=descripcion, price=precio, category=categoria, measurement_unit=unidad_medida)
        return redirect('products')

    if request.method == 'GET':
        # Mostrar la página de productos
        edit_id = request.GET.get('edit_id')
        if edit_id:
            product_to_edit = Products.objects.get(id=edit_id)
            return render(request, 'paginas/products.html', {'products': Products.objects.all(), 'edit_id': edit_id, 'product_to_edit': product_to_edit})

    products = Products.objects.all()
    measurement_units = Measurement_Units.objects.all()
    categories = Categories.objects.all()

    return render(request, 'paginas/products.html', {'products': products, 'measurement_units': measurement_units, 'categories':categories})

@csrf_exempt
def Inventory(request):
    if request.method == 'POST':
        if 'edit_id' in request.POST:
            # Manejar la edición del inventario existente
            edit_id = request.POST.get('edit_id')
            inventory_to_edit = Inventories.objects.get(id=edit_id)
            inventory_to_edit.product = Products.objects.get(id=request.POST.get('edit_product'))
            inventory_to_edit.amount = request.POST.get('edit_cantidad')
            inventory_to_edit.price = request.POST.get('edit_precio')
            inventory_to_edit.save()
        elif 'delete_id' in request.POST:
            # Manejar la eliminación del inventario existente
            delete_id = request.POST.get('delete_id')
            Inventories.objects.get(id=delete_id).delete()
        else:
            # Manejar la creación de un nuevo inventario
            product = Products.objects.get(id=request.POST.get('producto'))
            amount = request.POST.get('cantidad')
            price = request.POST.get('precio')
            Inventories.objects.create(product=product, amount=amount, price=price)

        return redirect('inventory')

    if request.method == 'GET':
        # Mostrar la página de inventarios
        edit_id = request.GET.get('edit_id')
        if edit_id:
            inventory_to_edit = Inventories.objects.get(id=edit_id)
            products = Products.objects.all()
            return render(request, 'paginas/inventory.html', {'inventories': Inventories.objects.all(), 'edit_id': edit_id, 'inventory_to_edit': inventory_to_edit, 'products': products})

    inventories = Inventories.objects.all()
    products = Products.objects.all()
    return render(request, 'paginas/inventory.html', {'inventories': inventories, 'products': products})

def Sales(request):
    return render(request, 'paginas/Sales.html')

def SalesHistory(request):
    return render(request, 'paginas/sales_history.html')

def exit(request):
    logout(request)
    return redirect('home')
