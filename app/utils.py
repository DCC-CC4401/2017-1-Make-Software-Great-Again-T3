# coding=utf-8

from django.contrib.auth.models import User
from app.models import AppUser, AmbulantVendor, Vendor, Category, PaymentMethod, Buyer, Statistics
from app.models import StaticVendor, Product, ProductIcon
import datetime


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

    t_start = datetime.datetime.strptime(data['schedule'][0], '%H:%M').time()
    t_finish = datetime.datetime.strptime(data['schedule'][1], '%H:%M').time()
    p = StaticVendor(user=user, has_stock=data['stack'], state=data['state'],
                     times_favorited=data['fav'], lat=data['lan'], lng=data['lng'],
                     t_start=t_start, t_finish=t_finish)
    p.save()
    for i in data['payment']:
        p.payment.add(PaymentMethod.objects.get(name=i))
    p.save()


def add_A_vendor(data):
    add_app_user(data)
    user = AppUser.objects.get(user=User.objects.get(username=data['username']))
    p = AmbulantVendor(user=user, has_stock=data['stack'], state=data['state'],
                       times_favorited=data['fav'], lat=data['lan'], lng=data['lng'])
    p.save()
    for i in data['payment']:
        p.payment.add(PaymentMethod.objects.get(name=i))
    p.save()


def add_product(data):
    user = Vendor.objects.get(user=AppUser.objects.get(user=User.objects.get(username=data['username'])))
    icon = ProductIcon.objects.get(name=data['icon'])
    p = Product(vendor=user, name=data['name'], photo=data['photo'], icon=icon,
                description=data['des'], stock=data['stock'], price=data['price'])
    p.save()
    for i in data['category']:
        p.category.add(Category.objects.get(name=i))
    p.save()


def add_category(cat):
    p = Category(name=cat)
    p.save()


def add_product_icon(data):
    p_icon = ProductIcon(name=data['name'], icon=data['icon'])
    p_icon.save()


def add_payment(pay):
    p = PaymentMethod(name=pay)
    p.save()


def add_buyer(data):
    add_app_user(data)
    user = AppUser.objects.get(user=User.objects.get(username=data['username']))
    p = Buyer.objects.create(user=user)
    p.save()


def add_stat(data):
    user = AppUser.objects.get(user=User.objects.get(username=data['username']))
    vendor = Vendor.objects.get(user=user)
    products = Product.objects.filter(vendor=vendor).filter(name=data['product_name'])
    if products.count() != 0:
        product = Product.objects.filter(vendor=vendor).filter(name=data['product_name']).first()
        p = Statistics.objects.create(vendor=vendor, date=data['date'], amount=data['amount'], product=product)
        p.save()


def test():
    User.objects.create_superuser(username='admin', email='bal@123.ck', password='1234')

    add_category('Almuerzos')
    add_category('Snack')
    add_category('Postres')

    # Add all the original icons
    icon_dict_list = [
        {'name': 'bread', 'icon': 'static/img/bread.png'},
        {'name': 'breakfast', 'icon': 'static/img/breakfast.png'},
        {'name': 'burger', 'icon': 'static/img/burger.png'},
        {'name': 'chicken', 'icon': 'static/img/chicken.png'},
        {'name': 'chicken2', 'icon': 'static/img/chicken2.png'},
        {'name': 'chocolate', 'icon': 'static/img/chocolate.png'},
        {'name': 'coke', 'icon': 'static/img/coke.png'},
        {'name': 'cupcake', 'icon': 'static/img/cupcake.png'},
        {'name': 'donut', 'icon': 'static/img/donut.png'},
        {'name': 'jelly', 'icon': 'static/img/jelly.png'},
        {'name': 'fish', 'icon': 'static/img/fish.png'},
        {'name': 'fries', 'icon': 'static/img/fries.png'},
        {'name': 'hot-dog', 'icon': 'static/img/hot-dog.png'},
        {'name': 'icecream', 'icon': 'static/img/icecream.png'},
        {'name': 'juice', 'icon': 'static/img/juice.png'},
        {'name': 'lettuce', 'icon': 'static/img/lettuce.png'},
        {'name': 'pizza', 'icon': 'static/img/pizza.png'},
        {'name': 'spaguetti', 'icon': 'static/img/spaguetti.png'},
        {'name': 'rice', 'icon': 'static/img/rice.png'}
    ]
    for idata in icon_dict_list:
        add_product_icon(idata)

    add_payment('tarjeta')
    add_payment('efectivo')
    add_payment('junaeb')

    data1 = {
        'username': 'vendor1',
        'email': 'test@prueba.cl',
        'password': '1234',
        'name': 'Daniel',
        'last_name': 'Aguirre',
        'photo': None,
        'type': 'VF',
        'payment': ['efectivo', 'tarjeta'],
        'stack': True,
        'state': 'A',
        'fav': 42,
        'lan': 0.0,
        'lng': 0.0,
        'schedule': ['12:00', '13:00']
    }
    add_S_vendor(data1)

    data2 = {
        'username': 'buyer',
        'email': 'test@prueba.cl',
        'password': '1234',
        'name': 'Robinson',
        'last_name': 'Castro',
        'photo': None,
        'type': 'C',
    }
    add_buyer(data2)
    buyer = Buyer.objects.get(user=AppUser.objects.get(user=User.objects.get(username=data2['username'])))
    buyer.favorites.add(Vendor.objects.get(user=
                                           AppUser.objects.get(user=User.objects.get(username=data1['username']))))
    buyer.save()

    data3 = {
        'username': 'vendor2',
        'email': 'test@prueba.cl',
        'password': '1234',
        'name': 'Andres',
        'last_name': 'Olivares',
        'photo': None,
        'type': 'VA',
        'payment': ['efectivo'],
        'stack': True,
        'state': 'I',
        'fav': 42,
        'lan': 0.0,
        'lng': 0.0,
    }
    add_A_vendor(data3)

    product_1 = {
        'username': 'vendor1',
        'name': 'Pizza',
        'photo': None,
        'icon': 'pizza',
        'category': ['Almuerzos'],
        'des': 'Deliciosa pizza hecha con masa casera, viene disponible en 3 tipos:',
        'stock': 20,
        'price': 1300
    }
    product_2 = {
        'username': 'vendor2',
        'name': 'Menú de arroz',
        'photo': None,
        'icon': 'rice',
        'category': ['Almuerzos'],
        'des': 'Almuerzo de arroz con pollo arvejado.',
        'stock': 40,
        'price': 2500
    }
    product_3 = {
        'username': 'vendor1',
        'name': 'Jugo',
        'photo': None,
        'icon': 'juice',
        'category': ['Snack'],
        'des': 'Jugo en caja sabor durazno.',
        'stock': 40,
        'price': 300
    }

    add_product(product_1)
    add_product(product_2)
    add_product(product_3)

    stat1 = {
        'username': 'vendor1',
        'product_name': 'Pizza',
        'date': datetime.datetime(year=2017, month=5, day=26, hour=13, minute=42, second=40),
        'amount': 1300
    }
    stat2 = {
        'username': 'vendor1',
        'product_name': 'Pizza',
        'date': datetime.datetime(year=2017, month=5, day=26, hour=12, minute=42, second=40),
        'amount': 1300
    }
    stat3 = {
        'username': 'vendor1',
        'product_name': 'Pizza',
        'date': datetime.datetime(year=2017, month=5, day=25, hour=13, minute=42, second=40),
        'amount': 1300
    }
    stat4 = {
        'username': 'vendor1',
        'product_name': 'Jugo',
        'date': datetime.datetime(year=2017, month=5, day=25, hour=12, minute=42, second=40),
        'amount': 400
    }

    add_stat(stat1)
    add_stat(stat2)
    add_stat(stat3)
    add_stat(stat4)
