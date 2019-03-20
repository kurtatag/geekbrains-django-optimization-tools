from django.db import models
from django.conf import settings
from django.db import transaction
from django.utils.functional import cached_property

from mainapp.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=0)
    add_datetime = models.DateTimeField(verbose_name='time', auto_now_add=True)

    @cached_property
    def get_items_cached(self):
        return self.user.cart.select_related()

    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_price_total, _items)))

    @classmethod
    def cart_items_total(cls, user):
        cart_products = cls.objects.filter(user=user)

        quantity_total = 0
        for cart_product in cart_products:
            quantity_total += cart_product.quantity

        return quantity_total

    @classmethod
    def cart_price_total(cls, user):
        cart_products = cls.objects.filter(user=user)

        price_total = 0
        for cart_product in cart_products:
            price_total += cart_product.product.price * cart_product.quantity

        return price_total

    @property
    def product_price_total(self):
        return self.quantity * self.product.price

    @classmethod
    def get_cart_items(cls, user):
        return cls.objects.filter(user=user)

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                quantity_delta = self.quantity - Cart.objects.get(pk=self.pk).quantity
            else:
                quantity_delta = self.quantity

            self.product.quantity -= quantity_delta
            self.product.save()
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.product.quantity += self.quantity
            self.product.save()
            super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.quantity} items"
