from django.urls import path

import mainapp.views as mainapp_views

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp_views.products, name='index'),
    path('<int:product_id>/', mainapp_views.product_details, name='product_details'),
    path('<str:current_product_category>/', mainapp_views.products, name='category'),
]
