from django.shortcuts import render, get_object_or_404, reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from shop import models
from paypal.standard.forms import PayPalPaymentsForm

# Create your views here.
def payment_process(request):
    orden_id = request.session.get('orden_id')
    orden = get_object_or_404(models.Orden, pk = orden_id)
    host = request.get_host()

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': str(orden.get_total()),
        'item_name': 'Order {}'.format(orden.id),
        'invoice': str(orden.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host, reverse('paypal:paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('payment:done')),
        'cancel_return': 'http://{}{}'.format(host, reverse('payment:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, "payment/process.html", {"form": form, "orden": orden})

@csrf_exempt
def payment_done(request):
    return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment/canceled.html')