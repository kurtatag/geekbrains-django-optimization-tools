from django.urls import path

import ordersapp.views as ordersapp_views

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp_views.OrderList.as_view(), name='orders_list'),
    path('forming/complete/<int:pk>/', ordersapp_views.order_forming_complete, name='order_forming_complete'),
    path('create/', ordersapp_views.OrderItemsCreate.as_view(), name='order_create'),
    path('read/<int:pk>/', ordersapp_views.OrderRead.as_view(), name='order_read'),
    path('update/<int:pk>/', ordersapp_views.OrderItemsUpdate.as_view(), name='order_update'),
    path('delete/<int:pk>/', ordersapp_views.OrderDelete.as_view(), name='order_delete'),
]
