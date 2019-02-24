from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.detail import View, SingleObjectMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mainapp.models import Product, ProductCategory
from adminapp.forms import ProductEditForm


class ProductList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'adminapp/products/index.html'
    paginate_by = 2

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    @staticmethod
    def get_category_list():
        categories = ProductCategory.objects.filter(is_active=True)
        return ['all'] + [c.name for c in categories]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'products'
        context['categories'] = ProductList.get_category_list()
        return context


class ProductCreate(SuccessMessageMixin, CreateView):
    template_name = 'adminapp/products/create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admin:products')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'new product'
        return context

    def get_success_message(self, cleaned_data):
        return 'Product "{}" was successfully created!'.format(self.object)


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'adminapp/products/read.html'

    def get_product_data(self):
        fields_to_show = ['id', 'name', 'short_description',
                          'description', 'image']
        return model_to_dict(self.object, fields_to_show)

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'product: {}'.format(self.get_object().name)
        context['product_data'] = self.get_product_data()
        return context


class ProductListByCategory(View):

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, category):

        if category == 'all':
            products = Product.objects.all()
        else:
            category_object = get_object_or_404(ProductCategory, name=category)
            products = category_object.products.all()

        page = 1
        if 'page' in self.request.GET:
            page = self.request.GET['page']

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        data = {
            'products': [],
            'page_info': {
                'has_other_pages': products_paginator.has_other_pages(),
                'has_previous': products_paginator.has_previous(),
                'has_next': products_paginator.has_next(),
                'page_range': list(products_paginator.paginator.page_range),
                'page_number': products_paginator.number,
            }
        }

        for product in products_paginator:
            product_info = {
                'product_id': product.id,
                'product_name': product.name,
                'is_active': product.is_active
            }
            data['products'].append(product_info)

        return JsonResponse(data)


class ProductUpdate(SuccessMessageMixin, UpdateView):
    model = Product
    template_name = 'adminapp/products/update.html'
    form_class = ProductEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'product: {}'.format(self.get_object().name)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_success_message(self, cleaned_data):
        return 'Product "{}" was successfully updated!'.format(self.object)


class ProductDelete(SingleObjectMixin, View):
    model = Product

    def get(self, *args, **kwargs):
        product = self.get_object()
        product.is_active = False
        product.save()

        success_message = 'Product "{}" was successfully deleted!'
        messages.success(self.request, success_message.format(product))

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
