from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from payment import views

urlpatterns = [
    url(r'^process$', login_required(views.payment_process), name = 'process'),
    url(r'^done$', views.payment_done, name = 'done'),
    url(r'^canceled$', views.payment_canceled, name = 'canceled')
]
