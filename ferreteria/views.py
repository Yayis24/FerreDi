from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from ferreteria.models import Categories, Measurement_Units, Products, Inventories, SaleDetails, Sales
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.db import transaction
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login
from .forms import CustomRegistrationForm
# Create your views here.

def Register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            authenticated_user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
            if authenticated_user:
                login(request, authenticated_user)
                return redirect('login')  # Cambia 'home' con la URL a la que deseas redirigir después del registro
    else:
        form = CustomRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html')
    else:
        print(request.POST['username'])
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print('Credenciales incorrectas')
            return render(request, 'registration/login.html', {'error': 'Credenciales incorrectas.'})
        else:
            return redirect('home')


def home(request):
    return render(request, 'paginas/home.html')


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

def SalesHistory(request):
    data = Sales.objects.all()
    return render(request, 'paginas/sales_history.html', {'data': data})

def sales(request):
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")
    inventories = Inventories.objects.all()
    title = 'Registrar Ventas'
    return render(request, 'paginas/Sales.html', {'datetime': current_datetime, 'inventories': inventories, 'title': title})

def get_inventory_price(request, inventory_id=None):
    try:
        inventory = Inventories.objects.get(pk=inventory_id)
        price = inventory.price
        amount = inventory.amount
        return JsonResponse({'price': price, 'amount': amount})
    except Inventories.DoesNotExist:
        return JsonResponse({'error': 'Inventario no encontrado'}, status=400)
        
def add_sale(request):
    if request.method == 'POST':
        date_time = request.POST.get('date_time')
        total = request.POST.get('total')
        customer = request.POST.get('customer')
        inventory_ids = request.POST.getlist('inventory_id[]')
        amounts = request.POST.getlist('amount[]')
        prices = request.POST.getlist('price[]')

        # Variable de error
        error = None
        
        # Verificar que todas las listas tengan la misma longitud
        if len(inventory_ids) == len(amounts) == len(prices):
            # Iniciar una transacción para evitar cambios parciales en la base de datos
            with transaction.atomic():
                sale = Sales(
                    date_time=date_time,
                    customer=customer,
                    total=total
                )
                sale.save()
                for i in range(len(inventory_ids)):
                    inventory_id = inventory_ids[i]
                    amount = amounts[i]
                    subtotal = prices[i]
                    amount = int(amount)
                    inventory = get_object_or_404(Inventories, id=inventory_id)

                    if inventory.amount < amount:
                        error = 'Cantidad de producto insuficiente'
                        print('Error: ' + error)
                        break  # Salir del bucle si se encuentra un error

                    sale_detail = SaleDetails(
                        amount=amount,
                        subtotal=subtotal,
                        inventory_id=inventory_id,
                        sale_id=sale.id
                    )

                    inventory.amount -= amount
                    inventory.save()
                    sale_detail.save()

                # Verificar si se encontró un error
                if error:
                    # Cancelar la transacción
                    transaction.set_rollback(True)

            if not error:
                # Generar el PDF automáticamente
                pdf = generate_pdf(sale)

                # Configurar la respuesta para descargar el PDF
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="venta.pdf"'
                response.write(pdf)
                return response
            else:
                # Mostrar el mensaje de error si se encontró un error
                inventories = Inventories.objects.all()
                current_datetime = datetime.now().strftime("%Y-%m-%dT%H:%M")
                return render(request, 'paginas/Sales.html', {'error': error, 'inventories': inventories, 'datetime': current_datetime})

        return redirect('Sales')
        # Si los datos del formulario no son válidos, puedes manejar los errores aquí.

    return render(request, 'paginas/Sales.html')

def generate_pdf(sale):
    # Supongamos que tienes una plantilla HTML llamada 'venta_template.html'
    template_path = 'paginas/template_report_pdf.html'
    template = get_template(template_path)
    
    # Supongamos que pasas la venta como contexto a la plantilla
    context = {'sale': sale}
    
    # Renderiza la plantilla con el contexto
    html = template.render(context)
    
    # Crea un objeto BytesIO para guardar el PDF
    pdf_data = BytesIO()
    
    # Convierte el contenido HTML a PDF
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), pdf_data)
    
    return pdf_data.getvalue()

def generate_pdf_report(request):
    # Obtener la opción seleccionada en el formulario del modal
    interval = request.POST.get('interval')

    # Calcular las fechas según la opción seleccionada
    today = datetime.now()
    
    if interval == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=6)
    elif interval == 'monthly':
        start_date = today.replace(day=1)
        end_date = (today.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    elif interval == 'yearly':
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(month=12, day=31)

    # Obtener las ventas dentro del rango de fechas
    # Asumiendo que tienes un modelo de Ventas (Sales) y las fechas están almacenadas en un campo 'date_time'
    sales = Sales.objects.filter(date_time__gte=start_date, date_time__lte=end_date)

    # Crear el contenido HTML del PDF con las ventas
    content = f'''
    <html>
    <head>
    </head>
    <body>
        <div class="invoice-header">
            <h1>Factura de Venta</h1>
        </div>
        <div class="invoice-details">
            <p><strong>Desde:</strong> {start_date} - <strong>Hasta:</strong> {end_date}</p>
            <p><strong>Total:</strong> {sum(sale.total for sale in sales)}</p>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Producto</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
    '''
    
    for sale in sales:
        for detail in sale.saledetails_set.all():
            content += f'''
            <tr>
                <td>{today}</td>
                <td>{detail.inventory.product.name}</td>
                <td>{detail.amount}</td>
                <td>${detail.subtotal}</td>
            </tr>
            '''
    
    content += f'''
                <tr class="total">
                    <td colspan="3"><strong>Total:</strong></td>
                    <td>${sum(sale.total for sale in sales)}</td>
                </tr>
            </tbody>
        </table>
    </body>
    </html>
    '''

    # Generar el PDF con xhtml2pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ventas_{start_date}_{end_date}.pdf'
    buffer = BytesIO()
    pisa.CreatePDF(BytesIO(content.encode('utf-8')), dest=buffer)
    response.write(buffer.getvalue())
    
    return response


def exit(request):
    logout(request)
    return redirect('login')
