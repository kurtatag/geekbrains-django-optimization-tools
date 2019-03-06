from django.http import HttpRequest
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from authapp.forms import (ShopUserLoginForm, ShopUserRegisterForm,
                           ShopUserEditForm, ShopUserProfileEditForm)
from .models import ShopUser


def login(request: HttpRequest):
    title = 'login'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next = request.GET['next'] if 'next' in request.GET.keys() else ''

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', context)


def logout(request: HttpRequest):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request: HttpRequest):
    title = 'register user'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                messages.success(request, 'Confirmation email was successfully sent.')
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                messages.error(request, 'Problem while sending confirmation email.')
                return HttpResponseRedirect(reverse('auth:register'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


@transaction.atomic
def edit(request: HttpRequest):
    title = 'edit user'

    if request.method == 'POST':
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
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )

    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }
    return render(request, 'authapp/edit.html', context)


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


def verify(request: HttpRequest, email: str, activation_key: str):
    context = {
        'title': 'user verification',
    }

    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html', context)
        else:
            messages.error(request, f'Error while activating user {user}.')
            return render(request, 'authapp/verification.html', context)
    except Exception as e:
        messages.error(request, f'Error while activating user:\n{e}\n {e.args}')
        return HttpResponseRedirect(reverse('index'))
