from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import datetime

# Create your views here.

from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


def index(req):
    return render(req, 'app/index.html', {})


def login(req):
    return render(req, 'app/login.html')


def signup(req):
    return render(req, 'app/signup.html', {})


def seller_profile_page(req):
    return render(req, 'app/vendedor-profile-page.html', {})


def products_administration(req):
    return render(req, 'app/gestion-productos.html', {})
