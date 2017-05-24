# coding=utf-8

from django.contrib.auth.models import User
from app.models import AppUser, AmbulantVendor, Vendor, Category
from app.models import StaticVendor
from app.models import Product


def add_user(data):
    user = User.objects.create_user(data['username'], data['email'], data['password'])
    user.first_name = data['name']
    user.last_name = data['last_name']
    user.save()


def add_app_user(data):
    add_user(data)
    user = User.objects.get(username=data['username'])
    p = AppUser(user=user, photo=data['photo'], user_type=data['type'])
    p.save()


def add_S_vendor(data):
    add_app_user(data)
    user = AppUser.objects.get(user=User.objects.get(username=data['username']))
    p = StaticVendor(user=user, payment=data['payment'], has_stock=data['stack'], state=data['state'],
                     times_favorited=data['fav'], lat=data['lan'], lng=data['lng'], schedule=data['schedule'])
    p.save()


def add_A_vendor(data):
    add_app_user(data)
    user = AppUser.objects.get(user=User.objects.get(username=data['username']))
    p = AmbulantVendor(user=user, payment=data['payment'], has_stock=data['stack'], state=data['state'],
                       times_favorited=data['fav'], lat=data['lan'], lng=data['lng'])
    p.save()


def add_product(data):
    user = Vendor.objects.get(user=AppUser.objects.get(user=User.objects.get(username=data['username'])))
    p = Product(vendor=user, name=data['name'], photo=data['photo'], icon=data['icon'],
                description=data['des'], stock=data['stock'], price=data['price'])
    p.save()
    cat = [Category.objects.get(name=i) for i in data['category']]
    p.category.add(*cat)


def add_category(cat):
    p = Category(name=cat)
    p.save()


def test():
    User.objects.create_superuser('buyer', 'bal@123.ck', '1234')
    user = User.objects.get(username='buyer')
    p = AppUser(user=user, photo=None, user_type='C')
    p.save()

    add_category('Almuerzos')
    add_category('Snack')
    data1 = {
        'username': 'vendor',
        'email': 'test@prueba.cl',
        'password': '1234',
        'name': 'Juan',
        'last_name': 'Perex',
        'photo': None,
        'type': 'VF',
        'payment': 'efectivo, tarjeta',
        'stack': True,
        'state': 'A',
        'fav': 42,
        'lan': 0.0,
        'lng': 0.0,
        'schedule': '12:00-13:00'
    }
    add_S_vendor(data1)

    product_1 = {
        'username': 'vendor',
        'name': 'Pizza',
        'photo': '../static/img/pepperoni1.jpg',
        'icon': '../static/img/pizza.png',
        'category': ['Almuerzos'],
        'des': 'Deliciosa pizza hecha con masa casera, viene disponible en 3 tipos:',
        'stock':20,
        'price': 1300
    }
    product_2 = {
        'username': 'vendor',
        'name': 'Menú de arroz',
        'photo': '../static/img/pollo1.jpg',
        'icon': '../static/img/rice.png',
        'category': ['Almuerzos'],
        'des': 'Almuerzo de arroz con pollo arvejado.',
        'stock': 40,
        'price': 2500
    }
    product_3 = {
        'username': 'vendor',
        'name': 'Jugo',
        'photo': '../static/img/jugo1.jpg',
        'icon': '../static/img/juice.png',
        'category': ['Snack'],
        'des': 'Jugo en caja sabor durazno.',
        'stock': 40,
        'price': 300
    }

    add_product(product_1)
    add_product(product_2)
    add_product(product_3)