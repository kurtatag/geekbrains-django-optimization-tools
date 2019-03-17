from django.db import models
from django.db import transaction
from django.conf import settings

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCESS = 'STP'
    PROCESSED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCELLED = 'CND'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'forming'),
        (SENT_TO_PROCESS, 'sent to process'),
        (PROCESSED, 'processed'),
        (PAID, 'paid'),
        (READY, 'ready'),
        (CANCELLED, 'cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Created', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Updated', auto_now=True)
    status = models.CharField(
        verbose_name='Status',
        max_length=3,
        choices=ORDER_STATUS_CHOICES,
        default=FORMING
    )
    is_active = models.BooleanField(verbose_name='Is Active', db_index=True, default=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'Order: {self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return len(items)

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    # we overwrite parent method
    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='orderitems',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Product',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Quantity',
        default=0
    )

    def get_product_cost(self):
        return self.product.price * self.quantity

    # overwrite parent method
    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.pk:
                quantity_delta = self.quantity - OrderItem.objects.get(pk=self.pk).quantity
            else:
                quantity_delta = self.quantity

            self.product.quantity -= quantity_delta
            self.product.save()
            super().save(*args, **kwargs)
