from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from app.models import AppUser, StaticVendor, AmbulantVendor, Product
from django.views.static import serve

from app.Forms import LoginForm, EditVendorForm


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


def products_administration(request):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        app_user = AppUser.objects.get(user=user)
        return render(request, 'app/gestion-productos.html', {'image': app_user.photo})
    else:
        return HttpResponseRedirect(reverse('index'))


def home(request):
    if request.user.is_authenticated():
        username = request.user.username
        app_user = AppUser.objects.filter(user=request.user)
        # print app_user[0].user_type, type(app_user[0].user_type)
        if app_user[0].user_type == u'C':
            return render(request, 'app/home.html', {'user': username})
        elif app_user[0].user_type == u'VF':
            vendor = StaticVendor.objects.filter(user=app_user)[0]

            products = []
            raw_products = Product.objects.filter(vendor=vendor)
            for i, p in enumerate(raw_products):
                tmp = {
                    'icon': p.icon,
                    'name': p.name,
                    'id': 'modal' + str(i),
                    'image': p.photo,
                    'category': p.category_str(),
                    'stock': p.stock,
                    'desc': p.description,
                    'price': p.price
                }
                products.append(tmp)

            data = {
                'user': username,
                'image': app_user[0].photo,
                'name': app_user[0].user.first_name,
                'last_name': app_user[0].user.last_name,
                'state': 'Activo' if vendor.state == 'A' else 'Inactivo',
                'payment': vendor.payment,
                'fav': vendor.times_favorited,
                'schedule': vendor.schedule,
                'type': 'Vendedor Fijo',
                'products': products
            }
            return render(request, 'app/vendedor-profile-page.html', data)
        else:
            vendor = AmbulantVendor.objects.filter(user=app_user)[0]
            products = []
            raw_products = Product.objects.filter(vendor=vendor)
            for i, p in enumerate(raw_products):
                tmp = {
                    'icon': p.icon,
                    'name': p.name,
                    'id': 'modal' + str(i),
                    'image': p.photo,
                    'category': p.category_str(),
                    'stock': p.stock,
                    'desc': p.description,
                    'price': p.price
                }
                products.append(tmp)

            data = {
                'user': username,
                'image': app_user[0].photo,
                'name': app_user[0].user.first_name,
                'last_name': app_user[0].user.last_name,
                'state': 'Activo' if vendor.state == 'A' else 'Inactivo',
                'payment': vendor.payment,
                'fav': vendor.times_favorited,
                'schedule': "",
                'type': 'Vendedor Fijo',
                'products': products
            }
            return render(request, 'app/vendedor-profile-page.html', data)
    else:
        return HttpResponseRedirect('app/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit_account(request):
    if request.user.is_authenticated():
        form = EditVendorForm(request.POST, request.FILES)
        user = User.objects.get(username=request.user.username)
        app_user = AppUser.objects.get(user=user)

        if form.is_valid() and request.method == 'POST':
            user.first_name = request.POST['name']
            user.last_name = request.POST['last_name']
            if request.FILES is not None:
                app_user.photo = form.cleaned_data['photo']
                app_user.save()
            user.save()
            return HttpResponseRedirect('home.html')
        else:
            form = EditVendorForm(initial={'name': request.user.first_name, 'last_name': request.user.last_name})
        data = {'form': form, 'photo': app_user.photo}
        return render(request, 'app/edit_account.html', data)
    else:
        return HttpResponseRedirect(reverse('index'))
