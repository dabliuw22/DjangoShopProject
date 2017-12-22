from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, DetailView
from shop import models
from shop import forms
from shop.carrito import Carrito
from shop.tasks import send_email
# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(Index, self).get_context_data(**kwargs)
        context['productos'] = models.Producto.objects.all().order_by('nombre')
        return context

@require_GET
def detail_producto(request, pk):
    producto = get_object_or_404(models.Producto, id = pk)
    form = forms.CarritoForm()
    return render(request, 'producto/detail.html', {'producto': producto, 'form': form})

# ----------- Carrito ------------
@require_POST
def add_carrito(request, pk):
    carrito = Carrito(request)
    producto = get_object_or_404(models.Producto, pk = pk)
    form = forms.CarritoForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        carrito.add(producto = producto, cantidad = data['cantidad'],
                    update_cantidad = data['update_cantidad'])
    return redirect('index')


def remove_carrito(request, id_producto):
    carrito = Carrito(request)
    producto = get_object_or_404(models.Producto, id = id_producto)
    carrito.remove(producto)
    return redirect('shop:carrito_detail')

@require_GET
def detail_carrito(request):
    carrito = Carrito(request)
    for item in carrito:
        item['update_cantidad_form'] = forms.CarritoForm(initial = {'cantidad': item['cantidad'],
                                                                    'update_cantidad': True})
    return render(request, 'carrito/detail.html', {'carrito': carrito})
# ----------- Fin Carrito ------------

# ----------- Ordenes -----------
def create_orden(request):
    carrito = Carrito(request)
    if request.method == 'POST':
        form = forms.OrdenForm(request.POST)
        if form.is_valid():
            orden = form.save(commit = False)
            orden.usuario = request.user
            orden.save()
            for item in carrito:
                detalle = models.DetalleOrden(orden = orden, producto = item['producto'],
                                                   cantidad = int(item['cantidad']))
                detalle.save()
            carrito.clear()
            send_email.delay(orden.id)
            request.session['orden_id'] = orden.id
            return redirect('payment:process')
    else:
        form = forms.OrdenForm()
    return render(request, 'orden/create.html', {'form': form})

# ----------- Fin Ordenes -----------

# ----------- Pagos ------------

# ----------- Fin Pagos ------------