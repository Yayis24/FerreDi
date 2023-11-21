from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('',views.home,name='home' ),
    path('category/',views.Category,name='category' ),
    path('measurement_unit/',views.Measurement_Unit,name='measurement_unit' ),
    path('inventory/',views.Inventory,name='inventory' ),
    path('products/',views.products,name='products' ),
    path('Sales/',views.Sales,name='Sales' ),
    path('sales_history/',views.SalesHistory,name='sales_history' ),
    path('logout/',views.exit,name='exit' ),

    
]