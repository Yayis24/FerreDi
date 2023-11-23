from django.urls import path
from . import views


urlpatterns = [
    path('',views.user_login,name='login' ),
    path('register/', views.Register, name='register'),
    path('home/',views.home,name='home' ),
    path('category/',views.Category,name='category' ),
    path('measurement_unit/',views.Measurement_Unit,name='measurement_unit' ),
    path('inventory/',views.Inventory,name='inventory' ),
    path('products/',views.products,name='products' ),
    path('Sales/',views.sales,name='Sales' ),
    path('sales/<int:inventory_id>', views.get_inventory_price, name='get_inventory_price'),   
    path('sales/add_sale', views.add_sale, name='add_sale'),   
    path('sales_history/',views.SalesHistory,name='sales_history' ),
    path('generate_pdf_report', views.generate_pdf_report, name='generate_pdf_report'),
    path('logout/',views.exit,name='exit' ),

    
]