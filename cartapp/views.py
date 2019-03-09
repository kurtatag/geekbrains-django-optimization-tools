from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import JsonResponse
from django.db import transaction

from cartapp.models import Cart
from mainapp.models import Product


@login_required
def cart(request: HttpRequest):
    cart = Cart.objects.filter(user=request.user)

    context = {
        'title': 'cart',
        'cart': cart,
    }
    return render(request, 'cartapp/cart.html', context)


@login_required
def cart_add(request: HttpRequest, pk: int):
    with transaction.atomic():
        product = get_object_or_404(Product, pk=pk)

        cart_product = Cart.objects.filter(user=request.user, product=product).first()

        if not cart_product:
            cart_product = Cart(user=request.user, product=product)

        cart_product.quantity += 1
        cart_product.save()

        product.quantity -= 1
        product.save()

    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product_details', args=[pk]))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_remove(request: HttpRequest, pk: int):
    with transaction.atomic():
        cart_product = get_object_or_404(Cart, pk=pk)
        cart_product.product.quantity += cart_product.quantity
        cart_product.product.save()
        cart_product.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def cart_edit(request: HttpRequest, pk: int, quantity: int):
    with transaction.atomic():
        cart_product = Cart.objects.get(pk=int(pk))
        product = cart_product.product

        quantity_delta = int(quantity) - cart_product.quantity

        cart_product.quantity = int(quantity)
        cart_product.save()

        product.quantity -= quantity_delta
        product.save()

    data = {
        'product_price_total': cart_product.product_price_total,
        'cart_price_total': Cart.cart_price_total(user=request.user),
        'cart_items_total': Cart.cart_items_total(user=request.user)
    }

    return JsonResponse(data)
