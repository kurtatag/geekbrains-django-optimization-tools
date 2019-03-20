from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.detail import View
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string

from .models import Product, ProductCategory

from my_utils import get_data_from_json

product_category_menu_links = get_data_from_json('product_category_menu_links.json')
product_list = get_data_from_json('product_list.json')


def index(request: HttpRequest):
    return render(request, 'mainapp/index.html')


def get_product_category_list():
    if settings.LOW_CACHE:
        key = 'categories_menu'
        categories_menu = cache.get(key)
        if categories_menu is None:
            categories_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, categories_menu)
        return categories_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def products(request: HttpRequest, current_product_category='all'):

    # get managers for products & categories
    # categories = ProductCategory.objects
    products = Product.objects

    # prepare a list of categories for "product category menu"
    product_category_list = ['all'] + [c.name for c in get_product_category_list()]

    # prepare a list of products
    if current_product_category == 'all':
        product_list = products.filter(
            is_active=True,
            category__is_active=True
        )
    else:
        product_list = products.filter(
            is_active=True,
            category__name=current_product_category
        )

    # prepare products paginator
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']
    paginator = Paginator(product_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    # prepare the context for the template
    context = {
        'title': 'products',
        'product_category_list': product_category_list,
        'current_product_category': current_product_category,
        'product_list': products_paginator,
    }

    return render(request, 'mainapp/products.html', context)


def products_ajax(request: HttpRequest, current_product_category='all'):

    # get managers for products & categories
    # categories = ProductCategory.objects
    products = Product.objects

    # prepare a list of categories for "product category menu"
    product_category_list = ['all'] + [c.name for c in get_product_category_list()]

    # prepare a list of products
    if current_product_category == 'all':
        product_list = products.filter(
            is_active=True,
            category__is_active=True
        )
    else:
        product_list = products.filter(
            is_active=True,
            category__name=current_product_category
        )

    # prepare products paginator
    page = 1
    if 'page' in request.GET:
        page = request.GET['page']
    paginator = Paginator(product_list, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    # prepare the context for the template
    context = {
        'product_category_list': product_category_list,
        'current_product_category': current_product_category,
        'product_list': products_paginator,
    }

    result = render_to_string(
        'mainapp/includes/inc_products_list.html',
        context=context,
        request=request)

    return JsonResponse({ 'result' : result})


def product_details(request: HttpRequest, product_id):

    product = get_object_or_404(Product, pk=product_id)

    # prepare a list of related products
    related_products = Product.objects \
                              .filter(category=product.category) \
                              .exclude(pk=product.pk)

    # prepare the context for the template
    context = {
        'title': 'product details',
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'mainapp/product_details.html', context)


def contact(request: HttpRequest):
    context = {
        'title': 'contact',
    }
    return render(request, 'mainapp/contact.html', context)


class ProductPrice(View):
    def get(self, request, product_id):

        price = get_object_or_404(Product, pk=product_id).price

        data = {
            'price': price
        }

        return JsonResponse(data)
