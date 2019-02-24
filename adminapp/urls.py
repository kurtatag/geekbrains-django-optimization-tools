from django.urls import path

from adminapp.views import users, categories, products

app_name = 'adminapp'

urlpatterns = [
    path('', categories.CategoryList.as_view(), name='index'),

    # users
    path('users/', users.UserList.as_view(), name='users'),
    path('users/create/', users.UserCreate.as_view(), name='user_create'),
    path('users/read/<int:pk>/', users.UserDetail.as_view(), name='user_read'),
    path('users/update/<int:pk>/', users.UserUpdate.as_view(), name='user_update'),
    path('users/delete/<int:pk>/', users.UserDelete.as_view(), name='user_delete'),

    # products
    path('products/', products.ProductList.as_view(), name='products'),
    path('products/create/', products.ProductCreate.as_view(), name='product_create'),
    path('products/read/<int:pk>/', products.ProductDetail.as_view(), name='product_read'),
    path('products/list/<str:category>/', products.ProductListByCategory.as_view(), name='products_by_category'),
    path('products/update/<int:pk>/', products.ProductUpdate.as_view(), name='product_update'),
    path('products/delete/<int:pk>/', products.ProductDelete.as_view(), name='product_delete'),

    # categories
    path('categories/', categories.CategoryList.as_view(), name='categories'),
    path('categories/create/', categories.CategoryCreate.as_view(), name='category_create'),
    path('categories/read/<int:pk>/', categories.CategoryDetail.as_view(), name='category_read'),
    path('categories/update/<int:pk>/', categories.CategoryUpdate.as_view(), name='category_update'),
    path('categories/delete/<int:pk>/', categories.CategoryDelete.as_view(), name='category_delete'),
]
