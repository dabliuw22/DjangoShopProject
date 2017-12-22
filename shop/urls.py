from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from shop import views

urlpatterns = [
    url(r'^producto/(?P<pk>\d+)$', views.detail_producto, name = 'producto_detail'),
    url(r'^carrito$', views.detail_carrito, name = 'carrito_detail'),
    url(r'^carrito/add/(?P<pk>\d+)$', views.add_carrito, name = 'carrito_add'),
    url(r'^orden/create$', login_required(views.create_orden), name = 'orden_create')
]