from django.urls import path

import cartapp.views as cartapp_views

app_name = 'cartapp'

urlpatterns = [
    path('', cartapp_views.cart, name='view'),
    path('add/<int:pk>/', cartapp_views.cart_add, name='add'),
    path('remove/<int:pk>/', cartapp_views.cart_remove, name='remove'),
    path('edit/<int:pk>/<int:quantity>/', cartapp_views.cart_edit, name='edit'),
]