from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app.models import AppUser

from app.Forms import LoginForm


def index(req):
    return render(req, 'app/index.html', {})


def login(request):
    form = LoginForm(request.POST)
    if form.is_valid() and request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        # app_user = AppUser.objects.filter(user=user)
        # print username, password, user
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('home.html')
            else:
                return render(request, 'app/login.html', {
                    'login_message': 'The user has been removed', 'form': form, })
        else:
            return render(request, 'app/login.html', {
                'login_message': 'Enter the username and password correctly', 'form': form, })
    else:
        form = LoginForm()
    return render(request, 'app/login.html', {
        'form': form,
    })


def signup(req):
    return render(req, 'app/signup.html', {})


def seller_profile_page(req):
    return render(req, 'app/vendedor-profile-page.html', {})


def products_administration(req):
    return render(req, 'app/gestion-productos.html', {})


def home(request):
    if request.user.is_authenticated():
        username = request.user.username
        app_user = AppUser.objects.filter(user=request.user)
        # print app_user[0].user_type, type(app_user[0].user_type)
        if app_user[0].user_type == u'C':
            return render(request, 'app/home.html', {'user': username})
        else:
            return render(request, 'app/vendedor-profile-page.html', {'user': username})
    else:
        return HttpResponseRedirect('app/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
