from django.http import HttpRequest
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import (ShopUserLoginForm, ShopUserRegisterForm,
                           ShopUserEditForm)
from django.contrib import auth
from django.urls import reverse

from my_utils import get_data_from_json

site_navigation_links = get_data_from_json('site_navigation_links.json')


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
        'site_navigation_links': site_navigation_links,
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
            register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'site_navigation_links': site_navigation_links,
        'register_form': register_form
    }
    return render(request, 'authapp/register.html', context)


def edit(request: HttpRequest):
    title = 'edit user'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES,
                                         instance=request.user)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserRegisterForm(instance=request.user)

    context = {
        'title': title,
        'site_navigation_links': site_navigation_links,
        'edit_form': edit_form
    }
    return render(request, 'authapp/edit.html', context)
