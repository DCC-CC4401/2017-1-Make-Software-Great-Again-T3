"""Software_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from Software_Project import settings
from app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^app/', include('app.urls')),
    url(r'^ajax/like/$', views.like, name='like'),
    url(r'^ajax/check_in/$', views.check_in, name='check_in'),
    url(r'^ajax/delete_product/$', views.delete_product, name='del_p'),
    url(r'^ajax/delete_account/$', views.delete_account, name='del_a'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
