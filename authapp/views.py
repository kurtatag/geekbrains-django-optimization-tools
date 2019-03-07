from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from authapp.forms import (ShopUserLoginForm, ShopUserRegisterForm,
                           ShopUserEditForm, ShopUserProfileEditForm)
from .models import ShopUser


class Login(LoginView):
    template_name = 'authapp/login.html'
    form = ShopUserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'login'
        return context


class Logout(LogoutView):
    next_page = '/auth/login/'


class Register(FormView):
    template_name = 'authapp/register.html'
    form_class = ShopUserRegisterForm

    def form_valid(self, form):
        user = form.save()
        if send_verify_mail(user):
            messages.success(self.request, 'Confirmation email was successfully sent.')
            return HttpResponseRedirect(reverse('auth:login'))
        else:
            messages.error(self.request, 'Problem while sending confirmation email.')
            return HttpResponseRedirect(reverse('auth:register'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'register user'
        return context


class EditUser(TemplateView):

    def get(self, request, *args, **kwargs):
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )

        context = {
            'title': 'edit user',
            'edit_form': edit_form,
            'profile_form': profile_form,
        }
        return render(request, 'authapp/edit.html', context)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        edit_form = ShopUserEditForm(request.POST, request.FILES,
                                     instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST,
                                               instance=request.user.shopuserprofile)

        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            messages.success(request, 'User info was successfully updated!')
            return HttpResponseRedirect(reverse('auth:edit'))
        else:
            messages.error(request, 'User info was not updated.')


class Verify(TemplateView):
    template_name = 'authapp/verification.html'

    def get(self, *args, **kwargs):
        request = self.request
        email = self.kwargs['email']
        activation_key = self.kwargs['activation_key']
        try:
            user = ShopUser.objects.get(email=email)
            if user.activation_key == activation_key and not user.is_activation_key_expired():
                user.is_active = True
                user.save()
                auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return render(request, 'authapp/verification.html', self.get_context_data())
            else:
                messages.error(request, f'Error while activating user {user}.')
                return render(request, 'authapp/verification.html', self.get_context_data())
        except Exception as e:
            messages.error(request, f'Error while activating user:\n{e}\n {e.args}')
            return HttpResponseRedirect(reverse('index'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'user verification'
        return context


def send_verify_mail(user):
    verify_link = reverse(
        'auth:verify',
        args=[user.email, user.activation_key]
    )

    title = f'Account confirmation for user {user.username}'

    message = f'Hello {user.username},\n' \
              f'To confirm your email please click this link:\n' \
              f'{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(
        title,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False
    )
