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
        cart = Cart.objects.get(user=request.user)
        cart_info['items_total'] = cart.get_total_quantity()
        cart_info['price_total'] = cart.get_total_cost()

    return {
        'cart_info': cart_info,
    }
