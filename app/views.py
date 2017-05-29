import datetime
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from app.Forms import LoginForm, EditVendorForm, EditProductForm, AddProductForm
from app.models import AppUser, StaticVendor, Product, Vendor, Buyer, PaymentMethod, ProductIcon, Category


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
    from app.utils import add_product
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        app_user = AppUser.objects.get(user=user)
        # Only vendors can add products
        if app_user.user_type != 'C':
            try:

                # Check form
                form = AddProductForm(request.POST, request.FILES)
                if request.method == 'POST' and form.is_valid():
                    name = form.cleaned_data['name']
                    price = form.cleaned_data['price']
                    stock = form.cleaned_data['stock']
                    icon = request.POST.get('icon-button')
                    if icon is None:
                        # Set default
                        icon = 'bread'
                    category = None
                    description = form.cleaned_data['des']
                    photo = None
                    if form.cleaned_data['photo'] is not None:
                        photo = form.cleaned_data['photo']
                    data = {
                        'username': request.user.username,
                        'name': name, 'price': price,
                        'stock': stock, 'des': description,
                        'icon': icon, 'photo': photo,
                        'category': ['Almuerzos']
                    }
                    add_product(data)
                    return HttpResponseRedirect(reverse('home'))
                else:
                    categories = []
                    raw_cat = Category.objects.all()
                    print "categories"
                    for cat in raw_cat:
                        tmp = {
                            'name': cat.name,
                        }
                        categories.append(tmp)
                    return render(request, 'app/gestion-productos.html', {'form':form,'categories': categories})

            except:
                print "exception: product save failed"
                return HttpResponseRedirect(reverse('home'))

    else:
        return HttpResponseRedirect(reverse('index'))


def home(request):
    if request.user.is_authenticated():
        username = request.user.username
        app_user = AppUser.objects.get(user=request.user)
        # print app_user[0].user_type, type(app_user[0].user_type)
        if app_user.user_type == u'C':
            return render(request, 'app/home.html', {'user': username})
        else:
            vendor = Vendor.objects.get(user=app_user)
            update(vendor)
            products = []
            raw_products = Product.objects.filter(vendor=vendor)
            for i, p in enumerate(raw_products):
                print p.icon.icon.url
                tmp = {
                    'icon': p.icon.icon.url[13:],
                    'name': p.name,
                    'id': 'modal' + str(i),
                    'image': p.photo,
                    'category': p.category_str(),
                    'stock': p.stock,
                    'desc': p.description,
                    'price': p.price,
                    'pid': p.id
                }
                products.append(tmp)

            data = {
                'user': username,
                'image': app_user.photo,
                'name': app_user.user.first_name,
                'is_static': True if vendor.user.user_type == 'VF' else False,
                'last_name': app_user.user.last_name,
                'state': 'Activo' if vendor.state == 'A' else 'Inactivo',
                'is_active': True if vendor.state == 'A' else False,
                'payment': vendor.payment_str(),
                'fav': vendor.times_favorited,
                'schedule': StaticVendor.objects.get(
                    user=vendor.user).schedule() if vendor.user.user_type == 'VF' else "",
                'type': 'Vendedor Fijo' if vendor.user.user_type == 'VF' else 'Vendedor Ambulante',
                'products': products
            }
            return render(request, 'app/vendedor-profile-page.html', data)
    else:
        return HttpResponseRedirect('login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def edit_account(request):
    choices = []
    for i in PaymentMethod.objects.all().values():
        choices.append((i['name'], i['name']))

    if request.user.is_authenticated():
        form = EditVendorForm(request.POST, request.FILES)
        form.fields['payment'].choices = choices
        user = User.objects.get(username=request.user.username)
        app_user = AppUser.objects.get(user=user)

        if app_user.user_type == u'C':
            return HttpResponseRedirect(reverse('home'))

        if form.is_valid() and request.method == 'POST':
            user.first_name = request.POST['name']
            user.last_name = request.POST['last_name']
            if form.cleaned_data['photo'] is not None:
                app_user.photo = form.cleaned_data['photo']
                app_user.save()
            vendor = Vendor.objects.get(user=app_user)
            if app_user.user_type == 'VF':
                svendor = StaticVendor.objects.get(user=app_user)
                svendor.t_start = form.cleaned_data['t_init']
                svendor.t_finish = form.cleaned_data['t_finish']
                svendor.save()

            pay = form.cleaned_data['payment']
            vendor.payment.clear()
            for i in pay:
                vendor.payment.add(PaymentMethod.objects.get(name=i))
            vendor.save()
            user.save()
            return HttpResponseRedirect('home')
        else:
            t_init = None
            t_finish = None
            if app_user.user_type == 'VF':
                ven = StaticVendor.objects.get(user=app_user)
                t_init = ven.t_start
                t_finish = ven.t_finish
            vendor = Vendor.objects.get(user=app_user)
            pay = vendor.payment.values()
            payment = {}
            for i in pay:
                payment[i['name']] = i['name']

            form = EditVendorForm(initial={'name': request.user.first_name, 'last_name': request.user.last_name,
                                           'payment': payment, 't_init': t_init,
                                           't_finish': t_finish
                                           })
            form.fields['payment'].choices = choices
        data = {'form': form, 'image': app_user.photo, 'is_static': True if app_user.user_type == 'VF' else False,
                'is_active': True if vendor.state == 'A' else False}
        return render(request, 'app/edit_account.html', data)
    else:
        return HttpResponseRedirect(reverse('index'))


def stock(request):
    if request.user.is_authenticated():
        username = request.user.username
        app_user = AppUser.objects.get(user=request.user)
        # print app_user[0].user_type, type(app_user[0].user_type)
        if app_user.user_type == u'C':
            return render(request, 'app/home.html', {'user': username})
        else:
            vendor = Vendor.objects.get(user=app_user)
            products = []
            raw_products = Product.objects.filter(vendor=vendor)
            for i, p in enumerate(raw_products):
                tmp = {
                    'icon': p.icon.icon.url[13:],
                    'name': p.name,
                    'id': 'modal' + str(i),
                    'image': p.photo,
                    'category': p.category_str(),
                    'stock': p.stock,
                    'desc': p.description,
                    'price': p.price,
                    'pid': p.id
                }
                products.append(tmp)

            data = {
                'user': username,
                'is_active': True if vendor.state == 'A' else False,
                'image': app_user.photo,
                'is_static': True if app_user.user_type == 'VF' else False,
                'products': products
            }
            return render(request, 'app/stock.html', data)
    else:
        return HttpResponseRedirect('login.html')


def edit_products(request, pid):
    if request.user.is_authenticated():
        user = User.objects.get(username=request.user.username)
        app_user = AppUser.objects.get(user=user)

        if app_user.user_type != 'C':
            vendor = Vendor.objects.get(user=app_user)
            products = Product.objects.filter(vendor=vendor)
            try:
                product = products.get(id=pid)
                form = EditProductForm(request.POST, request.FILES)
                if request.method == 'POST' and form.is_valid():
                    product.name = form.cleaned_data['name']
                    product.price = form.cleaned_data['price']
                    product.stock = form.cleaned_data['stock']
                    product.description = form.cleaned_data['des']
                    if form.cleaned_data['photo'] is not None:
                        product.photo = form.cleaned_data['photo']
                    product.save()
                    return HttpResponseRedirect(reverse('home'))
                else:
                    form = EditProductForm(initial={'name': product.name, 'price': product.price,
                                                    'stock': product.stock, 'des': product.description})
                    data = {'form': form, 'photo': product.photo, 'image': app_user.photo,
                            'is_active': True if vendor.state == 'A' else False}
                    return render(request, 'app/edit_product.html', data)
            except:
                return HttpResponseRedirect(reverse('home'))

    else:
        return HttpResponseRedirect(reverse('index'))


def vendor_c(request, pid):
    data = {'is_fav': False, 'id': pid, 'is_active': False}
    try:
        vendor = Vendor.objects.get(id=pid)
        update(vendor)
        if request.user.is_authenticated():
            user = AppUser.objects.get(user=request.user)
            data['auth'] = True
            data['user'] = request.user.username
            data['u_image'] = user.photo
            if user.user_type == 'C':
                buyer = Buyer.objects.get(user=user)
                if buyer.favorites.filter(user=vendor.user).values().count() != 0:
                    data['is_fav'] = True
            else:
                data['is_active'] = True if Vendor.objects.get(user=user).state == 'A' else False,
        else:
            data['auth'] = False

        products = []
        raw_products = Product.objects.filter(vendor=vendor)
        for i, p in enumerate(raw_products):
            tmp = {
                'icon': p.icon.icon.url[13:],
                'name': p.name,
                'id': 'modal' + str(i),
                'image': p.photo,
                'category': p.category_str(),
                'stock': p.stock,
                'desc': p.description,
                'price': p.price,
            }
            products.append(tmp)
        data['image'] = vendor.user.photo
        data['name'] = vendor.user.user.first_name
        data['last_name'] = vendor.user.user.last_name
        data['state'] = 'Activo' if vendor.state == 'A' else 'Inactivo'
        data['payment'] = vendor.payment_str()
        data['fav'] = vendor.times_favorited
        data['schedule'] = StaticVendor.objects.get(user=vendor.user).schedule if vendor.user.user_type == 'VF' else ""
        data['is_ambulant'] = True if vendor.user.user_type == 'VA' else False
        data['type'] = 'Vendedor Fijo' if vendor.user.user_type == 'VF' else 'Vendedor Ambulante'
        data['products'] = products

        return render(request, 'app/vendor_info.html', data)
    except:
        return HttpResponseRedirect(404)


def update(ven):
    t = datetime.datetime.now().time()
    if ven.user.user_type == 'VF':
        vendor = StaticVendor.objects.get(user=ven.user)
        now = datetime.time(hour=t.hour, minute=t.minute)
        if vendor.t_start <= now <= vendor.t_finish and vendor.state == 'I':
            vendor.state = 'A'
        if not vendor.t_start <= now <= vendor.t_finish and vendor.state == 'A':
            vendor.state = 'I'
        vendor.save()


def like(request):
    print "aqui"
    data = {'is_fav_now': False}
    pid = request.POST.get('id', None)
    vendor = Vendor.objects.get(id=pid)
    if request.user.is_authenticated():

        if Buyer.objects.filter(user=AppUser.objects.get(user=request.user)).values().count() != 0:
            buyer = Buyer.objects.get(user=AppUser.objects.get(user=request.user))
            if buyer.favorites.filter(user=vendor.user).values().count() != 0:
                buyer.favorites.remove(vendor)
                vendor.times_favorited -= 1
                data['is_fav_now'] = False
            else:
                buyer.favorites.add(vendor)
                vendor.times_favorited += 1
                data['is_fav_now'] = True
            buyer.save()
            vendor.save()
    data['favorites'] = vendor.times_favorited
    return JsonResponse(data)


def check_in(request):
    print("check in")

    user = AppUser.objects.get(user=request.user)
    vendor = Vendor.objects.get(user=user)

    vendor.state = 'A' if vendor.state == 'I' else 'I'
    vendor.save()

    return JsonResponse({
       'is_active': vendor.state == 'A'
    })


def stats(request):
    return render(request, 'app/stats.html')
