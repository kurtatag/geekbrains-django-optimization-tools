from mainapp.models import ProductCategory, Product

# delete all products & categories from db
Product.objects.all().delete()
ProductCategory.objects.all().delete()

# add categories to db
for name in ['home', 'office', 'furniture', 'modern', 'classic']:
    ProductCategory(name=name).save()


# for each category add 3 products
# it is so complicated because I have only 6 images for all my products
counter = 0
for category in ProductCategory.objects.all():
    for _ in range(3):
        Product(
            name=f'Product {counter + 1}',
            short_description='Seat and back with upholstery made of cold cure foam',
            description='Seat and back with upholstery made of cold cure foam. ' * 5,
            image=f'products_images/product-{counter % 6 + 1}.jpg',
            price=100,
            quantity=100,
            category=category
        ).save()
        counter += 1


# to run a script on a unix cli just do the following:
# $ python manage.py shell < my_script.py
