# -*- coding: utf-8 -*-
from celery import shared_task
from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from shop.models import Orden, DetalleOrden

@shared_task
def send_email(orden_id):
    orden = Orden.objects.get(id = orden_id)
    asunto = 'Orden N. {}'.format(orden.id)
    html = render_to_string('mail/mail_order.html',
                            {'orden': orden, 'productos': orden.get_detalles_orden()})
    msg = EmailMultiAlternatives(subject = asunto, to = [orden.usuario.email, settings.EMAIL_HOST_USER])
    msg.attach_alternative(html, 'text/html')
    msg.send()
