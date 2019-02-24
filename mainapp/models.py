from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='Name', max_length=64, unique=True)
    description = models.TextField(verbose_name='Description', blank=True)
    is_active = models.BooleanField(verbose_name='Is Active', default=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(verbose_name='Name', max_length=128)
    short_description = models.CharField(verbose_name='Short Description', max_length=60, blank=True)
    description = models.TextField(verbose_name='Description', blank=True)
    image = models.ImageField(upload_to='products_images', blank=True)
    price = models.DecimalField(verbose_name='Price', max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='Quantity', default=0)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    is_active = models.BooleanField(verbose_name='Is Active', default=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
