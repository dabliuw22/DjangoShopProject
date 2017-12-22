"""ShopProject URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout

from shop import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name = 'index'),
    url(r'^accounts/login/$', login, {'template_name': 'login.html'}, name = 'login'),
    url(r'^logout/$', logout, name = 'logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^paypal/', include('paypal.standard.ipn.urls', namespace = 'paypal')),
    url(r'^', include('shop.urls', namespace = 'shop')),
    url(r'^payment/', include('payment.urls', namespace = 'payment'))
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
