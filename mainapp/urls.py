from django.urls import path
from django.views.decorators.cache import cache_page

import mainapp.views as mainapp_views

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp_views.products, name='index'),
    path('<int:product_id>/', mainapp_views.product_details, name='product_details'),
    path('<str:current_product_category>/', cache_page(3600)(mainapp_views.products_ajax), name='category'),
    path('price/<int:product_id>/json/', mainapp_views.ProductPrice.as_view(), name='product_price'),
]
