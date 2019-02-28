from cartapp.models import Cart

from my_utils import get_data_from_json


def navigation(request):
    site_navigation_links = get_data_from_json('site_navigation_links.json')

    return {
        'site_navigation_links': site_navigation_links,
    }


def cart(request):
    cart_info = {
        'items_total': 0,
        'price_total': 0
    }

    if request.user.is_authenticated:
        cart_info['items_total'] = Cart.cart_items_total(user=request.user)
        cart_info['price_total'] = Cart.cart_price_total(user=request.user)

    return {
        'cart_info': cart_info,
    }
