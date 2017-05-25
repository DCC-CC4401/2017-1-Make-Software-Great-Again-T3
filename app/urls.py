from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^home', views.home, name='home'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^productos$', views.products_administration, name='products_administration'),
    url(r'^edit_account$', views.edit_account, name='edit_account')
]
