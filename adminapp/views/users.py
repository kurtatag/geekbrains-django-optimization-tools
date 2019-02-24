from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.detail import View, SingleObjectMixin
from django.contrib import messages

from authapp.models import ShopUser
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm


class UserList(ListView):
    model = ShopUser
    context_object_name = 'users'
    template_name = 'adminapp/users/index.html'

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'users'
        return context


class UserCreate(SuccessMessageMixin, CreateView):
    template_name = 'adminapp/users/create.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin:users')

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'new user'
        return context

    def get_success_message(self, cleaned_data):
        return 'User "{}" was successfully created!'.format(self.object)


class UserDetail(DetailView):
    model = ShopUser
    context_object_name = 'user'
    template_name = 'adminapp/users/read.html'

    def get_user_data(self):
        fields_to_show = ['id', 'username', 'email', 'age', 'avatar',
                          'is_superuser', 'is_staff', 'is_active']
        return model_to_dict(self.object, fields_to_show)

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user: {}'.format(self.get_object().username)
        context['user_data'] = self.get_user_data()
        return context


class UserUpdate(SuccessMessageMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/users/update.html'
    form_class = ShopUserEditForm

    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user: {}'.format(self.get_object().username)
        return context

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')

    def get_success_message(self, cleaned_data):
        return 'User "{}" was successfully updated!'.format(self.object)


class UserDelete(SingleObjectMixin, View):
    model = ShopUser

    def get(self, *args, **kwargs):
        user = self.get_object()
        user.is_active = False
        user.save()

        success_message = 'User "{}" was successfully deleted!'
        messages.success(self.request, success_message.format(user))

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))
