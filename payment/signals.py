from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from shop import models

def payment_notification(sender, **kwargs):
    obj = sender
    if obj.payment_status == ST_PP_COMPLETED:
        orden = get_object_or_404(models.Orden, id = obj.invoice)
        orden.servida = True
        orden.save()
        for item in orden.get_detalles_orden():
            producto = item.producto
            producto.set_stock(item.cantidad)
            producto.save()

valid_ipn_received.connect(payment_notification)