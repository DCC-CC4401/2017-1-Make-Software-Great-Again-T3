from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

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
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    photo = models.ImageField()
    user_type = (('C','Comprador'),('VF','Vendedor Fijo'),('VA','Vendedor Ambulante'))

# Abstract base class for both vendor types
class Vendor(models.Model):
    payment = models.CharField(max_length=100)
    has_stock = models.BooleanField()
    state = (('A','Active'),('I','Inactive'))
    #stats
    times_favorited = models.IntegerField()
    user = models.OneToOneField(AppUser, on_delete = models.CASCADE)
    ubication = models.CharField(max_length=200)

class AmbulantVendor(Vendor):
    pass

class StaticVendor(Vendor):
    schedule = models.CharField(max_length=200)

class Buyer(models.Model):
    user = models.OneToOneField(AppUser, on_delete = models.CASCADE)
    #favorites_ambulant = models.ManyToManyField(AmbulantVendor)
    #favorites_static = models.ManyToManyField(StaticVendor)
    favorites = models.ManyToManyField(Vendor)

class Product(models.Model):

    # Work around for Abstract Class foreign keys.
    # It may be changed for a Generic foreign key.
    #ambulant_vendor = models.ForeignKey(AmbulantVendor, on_delete = models.CASCADE)
    #static_vendor = models.ForeignKey(StaticVendor, on_delete = models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    photo = models.ImageField()
    category = (('Ve','Vegetariana'),('Va','Vegana'),('S','Snack'))
    description = models.CharField(max_length=200)
    stock = models.IntegerField()
    price = models.IntegerField()

class Statistics(models.Model):
    # Work around for Abstract Class foreign keys.
    # It may be changed for a Generic foreign key.
#    ambulant_vendor = models.ForeignKey(AmbulantVendor, on_delete = models.CASCADE)
 #   static_vendor = models.ForeignKey(StaticVendor, on_delete = models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete = models.CASCADE)  
    stat_file = models.FileField()
