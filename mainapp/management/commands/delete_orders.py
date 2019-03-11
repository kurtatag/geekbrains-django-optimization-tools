from django.core.management.base import BaseCommand
from ordersapp.models import Order


class Command(BaseCommand):
    def handle(self, *args, **options):
        Order.objects.all().delete()
