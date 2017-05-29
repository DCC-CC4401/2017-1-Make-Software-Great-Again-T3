from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from Software_Project import settings

'''
    User:
    The primary attributes of the default user are:
        username
        password
        email
        first_name
        last_name
'''

# User extension to add usertype
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField()
    user_type_dicc = (('C', 'Comprador'), ('VF', 'Vendedor Fijo'), ('VA', 'Vendedor Ambulante'))
    user_type = models.CharField(max_length=2, choices=user_type_dicc)

class PaymentMethod(models.Model):
    name = models.CharField(max_length=30)

# Abstract base class for both vendor types
class Vendor(models.Model):
    payment = models.ManyToManyField(PaymentMethod)
    has_stock = models.BooleanField()
    state_dicc = (('A', 'Active'), ('I', 'Inactive'))
    state = models.CharField(max_length=1, choices=state_dicc)
    # stats
    times_favorited = models.IntegerField()
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    lat = models.DecimalField(max_digits=10, decimal_places=2)
    lng = models.DecimalField(max_digits=10, decimal_places=2)

    def payment_str(self):
        temp = []
        for i in self.payment.values():
            temp.append(i['name'])
        return ' '.join(temp)


class AmbulantVendor(Vendor):
    pass


class StaticVendor(Vendor):
    t_start = models.TimeField()
    t_finish = models.TimeField()

    def schedule(self):
        return self.t_start.strftime('%H:%M') + '-' + self.t_finish.strftime('%H:%M')


class Buyer(models.Model):
    user = models.OneToOneField(AppUser, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Vendor)


class Category(models.Model):
    name = models.CharField(max_length=30)


# Icons are saved to avoid saving the same image many times.
class ProductIcon(models.Model):
    name = models.CharField(max_length=30)
    icon = models.ImageField()


class Product(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField()
    # Foreign key as "equivalent" to ManyToOne for icon->product
    icon = models.ForeignKey(ProductIcon)
    category = models.ManyToManyField(Category)
    description = models.CharField(max_length=200)
    stock = models.IntegerField()
    price = models.IntegerField()

    def category_str(self):
        temp = []
        for i in self.category.values():
            temp.append(i['name'])
        return ' '.join(temp)


class Statistics(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    stat_file = models.FileField()
