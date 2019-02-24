from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse

from cartapp.models import Cart
from mainapp.models import Product
from my_utils import get_data_from_json

site_navigation_links = get_data_from_json('site_navigation_links.json')


@login_required
def cart(request: HttpRequest):
    cart = Cart.objects.filter(user=request.user)

    # prepare cart info to be displayed on the site navigation menu
    cart_info = {
        'items_total': 0,
        'price_total': 0
    }

    if request.user.is_authenticated:
        cart_info['items_total'] = Cart.cart_items_total(user=request.user)
        cart_info['price_total'] = Cart.cart_price_total(user=request.user)

    context = {
        'title': 'cart',
        'site_navigation_links': site_navigation_links,
        'cart': cart,
        'cart_info': cart_info,
    }
    return render(request, 'cartapp/cart.html', context)


@login_required
def cart_add(request: HttpRequest, pk: int):
    product = get_object_or_404(Product, pk=pk)

    cart = Cart.objects.filter(user=request.user, product=product).first()

    if not cart:
        cart = Cart(user=request.user, product=product)

    cart.quantity += 1
    cart.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product_details', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_remove(request: HttpRequest, pk: int):

    cart_product = get_object_or_404(Cart, pk=pk)
    cart_product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_edit(request: HttpRequest, pk: int, quantity: int):
    cart_product = Cart.objects.get(pk=int(pk))
    cart_product.quantity = int(quantity)
    cart_product.save()

    data = {
        'product_price_total': cart_product.product_price_total,
        'cart_price_total': Cart.cart_price_total(user=request.user),
        'cart_items_total': Cart.cart_items_total(user=request.user)
    }

    return JsonResponse(data)
