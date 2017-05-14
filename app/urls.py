from django.conf.urls import url

from app import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^signup$', views.signup, name='signup'),
    url(r'^vendedor$', views.seller_profile_page, name='seller_profile_page'),
    url(r'^productos$', views.products_administration, name='products_administration'),
]