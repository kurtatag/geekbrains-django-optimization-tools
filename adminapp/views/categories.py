from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.detail import View, SingleObjectMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator

from mainapp.models import ProductCategory
from adminapp.forms import ProductCategoryEditForm


class CategoryList(ListView):
    model = ProductCategory
    context_object_name = 'categories'
    template_name = 'adminapp/categories/index.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'categories'
        return context


class CategoryCreate(SuccessMessageMixin, CreateView):
    template_name = 'adminapp/categories/create.html'
    form_class = ProductCategoryEditForm
    success_url = reverse_lazy('admin:categories')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'new category'
        return context

    def get_success_message(self, cleaned_data):
        return 'Category "{}" was successfully created!'.format(self.object)


class CategoryDetail(DetailView):
    model = ProductCategory
    context_object_name = 'category'
    template_name = 'adminapp/categories/read.html'

    def get_products_in_category(self):
        return self.get_object().products.all()[:5]

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'category: {}'.format(self.get_object().name)
        context['products'] = self.get_products_in_category()
        return context


class CategoryUpdate(SuccessMessageMixin, UpdateView):
    model = ProductCategory
    template_name = 'adminapp/categories/update.html'
    form_class = ProductCategoryEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'category: {}'.format(self.get_object().name)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_success_message(self, cleaned_data):
        return 'Category "{}" was successfully updated!'.format(self.object)


class CategoryDelete(SingleObjectMixin, View):
    model = ProductCategory

    def get(self, *args, **kwargs):
        category = self.get_object()
        category.is_active = False
        category.save()

        success_message = 'Category "{}" was successfully deleted!'
        messages.success(self.request, success_message.format(category))

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
